import os, sqlite3
from abc import  *
from bs4 import BeautifulSoup
import requests, rsa, re

programName = "donggukEclassHelper"

#학기목록, 강의목록, 과제목록, 공지사항목록, 학습자료실 목록에 사용
class ListBase(metaclass=ABCMeta):

    @abstractmethod
    def __init(self):
        pass

    @abstractmethod
    def __getLocalList(self):
        pass

    @abstractmethod
    def __getRemoteList(self):
        pass

    @abstractmethod
    def __updateLocalList(self):
        pass


class User():
    __Instance = None
    __studentNumber = None
    __name = None
    __session = None
    __campus = "서울캠퍼스"

    def __init__(self):
        if self.__Instance is not None:
            raise ValueError("instance already exist!")
        else:  # constructor
            self.__session = requests.Session()

    @classmethod
    def getInstance(cls):
        if cls.__Instance is None:
            cls.__Instance = User()
        return cls.__Instance

    def getInfo(self,t):
        if t is "studentNumber":
            return self.__studentNumber
        elif t is "campus":
            return self.__campus
        elif t is "name":
            return self.__name
        else:
            return "oops!"

    def login(self, studentNumber, password):
        id = str(studentNumber).encode()
        pw = str(password).encode()
        url = "https://eclass.dongguk.edu/User.do"
        params = {'cmd': 'getRsaPublicKey'}
        response = self.__session.get(url, params=params)
        result = response.json()

        # n,e 설정 후 Public Key 초기화
        n = int(result['pubKey1'], 16)  # pubKey1, 256 length(hex)
        e = int(result['pubKey2'], 16)  # pubKey2, 10001(hex) 65537(int)
        pubKey = rsa.PublicKey(n, e)  # Public Key setting
        idCrypto = rsa.encrypt(id, pubKey)
        pwCrypto = rsa.encrypt(pw, pubKey)
        params = {'userDTO.paramUserId': idCrypto.hex(),
                  'userDTO.paramPassword': pwCrypto.hex(),
                  'cmd': 'loginUser',
                  'userDTO.outsiderYn': 'N'}
        self.__session.post(url, data=params)
        response = self.__session.get("https://eclass.dongguk.edu/Main.do?cmd=viewHome")

        # 로그인 성공 여부 체크
        if response.text.find(str(studentNumber)) == -1:
            return False
        else:
            exp = r"(?<="+str(studentNumber)+"\().+(?=\))"
            m = re.search(exp,response.text)
            self.__studentNumber = str(studentNumber)
            self.__name = m.group()
            return True

    def sessionPost(self, url, params):
        return self.__session.post(url,data=params)

    def sessionGet(self, url):
        return  self.__session.get(url)

class Data():
    __Instance = None
    __dataPath = os.environ['LOCALAPPDATA'] + "\\" + programName
    __documentPath = os.environ['HOMEDRIVE']+os.environ['HOMEPATH'] + "\\Documents\\" + programName
    __dbConnection = None
    __cursor = None

    def __init__(self):
        if self.__Instance is not None:
            raise ValueError("instance already exist!")
        else:
            self.__init()

    def __del__(self):
        self.__dbConnection.close()

    @classmethod
    def getInstance(cls):
        if cls.__Instance is None:
            cls.__Instance = Data()
        return cls.__Instance

    def __firstCheck(self):
        isFirst = os.path.exists(self.__dataPath)
        if isFirst is False:
            return True
        else:
            return False

    #sqlite query testing : https://sqliteonline.com/
    def __firstInit(self):
        # 프로그램을 처음 설치 후 실행했을때. 디렉토리와 데이터베이스&테이블을 생성.
        os.mkdir(self.__dataPath)
        os.mkdir(self.__documentPath)

        # 데이터베이스 생성 및 테이블 정의
        # sqlite 자료형 : INTEGER, REAL, TEXT, BLOB, NULL
        # https://wikidocs.net/12454, http://lovedb.tistory.com/348 참조
        self.__dbConnection = sqlite3.connect(self.__dataPath + "\\" + programName + ".db")
        self.__cursor = self.__dbConnection.cursor()
        # Account <학번, 이름>
        self.__cursor.execute('''create table `Account` (
                                `studentNumber` INTEGER NOT NULL PRIMARY KEY,
                                `name` TEXT );
                                ''')
        # Semester <학번, 학기코드, 학기이름>
        self.__cursor.execute('''create table `Semester` (
                                        `studentNumber` INTEGER,
                                        `semesterCode` TEXT,
                                        `semesterName` TEXT,
                                        PRIMARY KEY (studentNumber,semesterCode, semesterName) );
                                        ''')
        # Lecture <강의코드, 교수님성함, 교수님연락처, 교수님메일, 학수번호, 분반, 수강생수, 학점, 성적비중, 한줄메모, 수업날짜, 폴더경로>
        self.__cursor.execute('''create table `Lecture` (
                                `studentNumber` INTEGER,
                                `semester` TEXT,
                                `lectureCode` TEXT NOT NULL,
                                `lectureName` TEXT, 
                                `academicNumber` TEXT,
                                `classNumber` INTEGER,
                                `totalStudentNumber` INTEGER,
                                `grades` INTEGER,
                                `dateTime` TEXT,
                                `professorName` TEXT,
                                `professorContact` TEXT,
                                `professorMail` TEXT,
                                `assistant1Name` TEXT,
                                `assistant1Contact` TEXT,
                                `assistant1Mail` TEXT,
                                `assistant2Name` TEXT,
                                `assistant2Contact` TEXT,
                                `assistant2Mail` TEXT,
                                `scoreRatio` TEXT,
                                `memo` TEXT,
                                `directory` TEXT,
                                PRIMARY KEY (lectureCode,studentNumber,semester));''')
        """
        # CourseList <강의코드, 학번>
        self.__cursor.execute('''create table `CourseList` (
                                `lectureCode` TEXT NOT NULL,
                                `studentNumber` INTEGER NOT NULL,
                                PRIMARY KEY (lectureCode,studentNumber) );
                                ''')
        """
        # Notice <id, 제목, 작성일, 조회수, 내용, 파일링크>
        self.__cursor.execute('''create table `Notice` (
                                `id` INTEGER NOT NULL PRIMARY KEY,
                                `title` TEXT NOT NULL,
                                `writeDate` TEXT,
                                `hitNumber` INTEGER,
                                `contents` TEXT,
                                `fileLink` TEXT );
                                ''')
        # Assignment <id, 과제이름, 과제내용, 제출시작일, 제출마감일, 연장제출일, 제출완료여부, 제출일자, 평가점수, 강의코드, 학번, 팀과제여부>
        self.__cursor.execute('''create table `Assignment` (
                                `id` INTEGER NOT NULL PRIMARY KEY,
                                `title` TEXT NOT NULL,
                                `contents` TEXT,
                                `startDate` TEXT,
                                `deadLine` TEXT,
                                `extenedDate` TEXT,
                                `status` TEXT,
                                `submitDate` TEXT,
                                `score` TEXT,
                                `lectureCode` TEXT,
                                `studentNumber` INTEGER,
                                `team` TEXT);
                                ''')
        # LearningResource <id, 제목, 작성일, 조회수, 내용, 파일링크>
        self.__cursor.execute('''create table `LearningResource` (
                                `id` INTEGER NOT NULL PRIMARY KEY,
                                `title` TEXT NOT NULL,
                                `writeDate` TEXT,
                                `hitNumber` INTEGER,
                                `contents` TEXT,
                                `fileLink` TEXT );
                                ''')
        # Bookmark <학번, 종류(유형), id>
        self.__cursor.execute('''create table `BookMark` (
                                `studentNumber` INTEGER,
                                `type` TEXT,
                                `id` INTEGER,
                                PRIMARY KEY (studentNumber, type, id) );
                                ''')
        # Exam <강의코드, 시험날짜, 시험시작시간, 시험종료시간, 강의실위치>
        # 미구현
        # Cancled <강의코드, 휴강날짜, 휴강시간>
        # 미구현
        # Reinforcement <강의코드, 보강날짜, 보강시작시간, 보강종료시간, 강의실>
        # 미구현

        self.__dbConnection.commit()
        self.__dbConnection.close()

    def __init(self):
        if (self.__firstCheck() is True):
            print('프로그램을 처음 실행합니다. 디렉토리 및 데이터베이스를 생성합니다.')
            self.__firstInit()
        self.__dbConnection = sqlite3.connect(self.__dataPath + "\\" + programName + ".db")
        self.__cursor = self.__dbConnection.cursor()

    def query(self, query):
        self.__cursor.execute(query)
        self.__dbConnection.commit()

    def select(self, _select, _from, _where, _order_by=None):
        if _select == "":
            _select = "*"
        if _order_by is None:
            query = 'SELECT ' + str(_select) + ' FROM ' + str(_from) + ' WHERE ' + str(_where)
        else :
            query = 'SELECT ' + str(_select) + ' FROM ' + str(_from) + ' WHERE ' + str(_where) + ' ORDER BY ' + str(
                _order_by)
        self.query(query)
        return self.__cursor.fetchall()

    def insert(self, _table, _into, _values):
        if _into.__len__() != 0:
            if _into.__len__() != _values.__len__():
                raise ValueError('column 수와 value 수가 일치하지 않습니다.')
            query = 'INSERT INTO ' + str(_table) + '('
            for i in _into:
                query += str(i) + ','
            query = query[:-1]
            query += ') VALUES ('
            for j in _values:
                query += '"' + str(j) + '",'
            query = query[:-1]
            query += ')'
        else:
            query = 'INSERT INTO ' + str(_table) + ' VALUES ('
            for j in _values:
                query += '"' + str(j) + '",'
            query = query[:-1]
            query += ')'
        self.query(query)

    def getInfo(self,t):
        if (t == 'connection'):
            if self.__dbConnection is not None:
                return True
            else:
                return False

class Lecture():
    #시스템 작성
    __lectureCode = None
    __lectureName = None
    __academicNumber = None
    __classNumber = None
    __totalStudentNumber = None
    __grades = None
    __dateTime = None
    __professorName = None
    __professorContact = None
    __professorMail = None
    __assistant1Name = None
    __assistant1Contact = None
    __assistant1Mail = None
    __assistant2Name = None
    __assistant2Contact = None
    __assistant2Mail = None
    #사용자 작성
    __scoreRatio = None
    __memo = None
    __directory = None

    def __init__(self,lectureData):
        raise NotImplementedError

    def updateInfo(self,t,v):
        raise NotImplementedError

    def getInfo(self,t):
        raise NotImplementedError

class SemesterList(ListBase):
    __Instance = None
    __list = {}
    __lectureListMap = {}

    def __init__(self):
        if self.__Instance is not None:
            raise ValueError("instance already exist!")
        else:
            self._ListBase__init()
            print(self.__list)

    def __del__(self):
        pass

    @classmethod
    def getInstance(cls):
        if cls.__Instance is None:
            cls.__Instance = SemesterList()
        return cls.__Instance

    def _ListBase__init(self):
        localList = self._ListBase__getLocalList()
        self.__list = localList
        remoteList = self._ListBase__getRemoteList()
        oCmpResult = localList.keys() - remoteList.keys()  # drop semester
        nCmpReuslt = remoteList.keys() - localList.keys()  # add semester
        if (oCmpResult.__len__() != 0) or (nCmpReuslt.__len__() != 0):
            print("업데이트(변경) 항목이 있습니다. ")
            self._ListBase__updateLocalList(remoteList)


    # 로컬에 저장된 학기목록 로드
    # 학기코드(key) : 학기이름(value)로 구성
    # ex) { '@@@@' : '2017년 2학기' }
    def _ListBase__getLocalList(self):
        user = User.getInstance()
        data = Data.getInstance()
        fetchResult = data.select('semesterCode, semesterName', 'Semester',
                                  """studentNumber = '""" + user.getInfo('studentNumber') + """'""")
        returnVal = {}
        for i in fetchResult:
            returnVal[i[0]] = i[1]
        return returnVal

    # 사용자가 이수했던 학기목록을 파악
    # 학기코드(key) : 학기이름(value)로 구성
    # ex) { '@@@@' : '2017년 2학기' }
    def _ListBase__getRemoteList(self):
        user = User.getInstance()
        user.sessionGet("https://eclass.dongguk.edu/Main.do?cmd=viewHome")  # 홈으로 초기화
        # 페이지 이동
        # https://eclass.dongguk.edu/Main.do?cmd=moveMenu&mainDTO.parentMenuId=menu_00026&mainDTO.menuId=menu_00031
        url = "https://eclass.dongguk.edu/Main.do"
        params = {'cmd': 'moveMenu',
                  'mainDTO.parentMenuId': 'menu_00026',
                  'mainDTO.menuId': 'menu_00031'}
        user.sessionPost(url, params)

        # https://eclass.dongguk.edu/Study.do?cmd=viewLearnerCourseList&boardInfoDTO.boardInfoGubun=learnercourse
        url = "https://eclass.dongguk.edu/Study.do"
        params = {'cmd': "viewLearnerCourseList",
                  'boardInfoDTO.boardInfoGubun': "learnercourse"}
        response = user.sessionPost(url, params)
        soup = BeautifulSoup(response.text, 'html.parser')
        soupResult = soup.find_all(id='termBox')
        soup = soupResult[0]
        remoteList = {}
        for option in soup:
            if option != "\n":
                remoteList[option.attrs['value']] = option.text
        return remoteList

    # 로컬과 원격을 비교하여 업데이트
    # 원격의 데이터를 무조건적으로 신뢰하여 업데이트 합니다.
    def _ListBase__updateLocalList(self, remote):
        data = Data.getInstance()
        user = User.getInstance()
        for key, value in remote.items():
            insertColumn = ['studentNumber', 'semesterCode', 'semesterName']
            insertValues = [user.getInfo('studentNumber'), key, value]
            data.insert('Semester', insertColumn, insertValues)
        self.__list = remote


# 한학기에 수강한 강의목록들의 List
# 학기별로 하나씩 가지고 있게 되며 SemesterList 에 저장된다.
class LectureList(ListBase):
    __instance = None
    __list = []
    __semesterCode = None

    def __init__(self, semesterCode):
        if self.__instance is not None:
            raise ValueError("instance already exist!")
        else:
            self.__semesterCode = semesterCode
            self._ListBase__init()

    @classmethod
    def getIntance(cls, semesterCode):
        if cls.__instance is None:
            cls.__instance = LectureList(semesterCode)
        return cls.__instance

    def _ListBase__init(self):
        localData = self._ListBase__getLocalList()
        remoteData = self._ListBase__getRemoteList()
        if localData.__len__() is not remoteData.__len__():
            print("업데이트(변경) 항목이 있습니다. ")
            self._ListBase__updateLocalList(localData, remoteData)

        # 해당 학기의
        # self.__getSemesterList()
        # for key, value in self.__semesterList.items():
        #    courseList = self.__scrapLectureData(key)

    def _ListBase__getLocalList(self):
        # 로컬데이터베이스로부터 강의정보를 읽어들여, data를 구축합니다.
        data = Data.getInstance()
        user = User.getInstance()
        fetchResult = data.select('*', 'Lecture',
                                  'semester = "' + self.__semesterCode + '" AND studentNumber = "' + user.getInfo(
                                      'studentNumber') + '"')
        returnVal = []
        for i in fetchResult:
            lecture = {}
            lecture['lectureCode'] = i[0]
            lecture['lectureName'] = i[1]
            lecture['academicNumber'] = i[2]
            lecture['classNumber'] = i[3]
            lecture['totalStudentNumber'] = i[4]
            lecture['grades'] = i[5]
            lecture['dateTime'] = i[6]
            lecture['professorName'] = i[7]
            lecture['professorContact'] = i[8]
            lecture['professorMail'] = i[9]
            lecture['assistant1Name'] = i[10]
            lecture['assistant1Contact'] = i[11]
            lecture['assistant1Mail'] = i[12]
            lecture['assistant2Name'] = i[13]
            lecture['assistant2Contact'] = i[14]
            lecture['assistant2Mail'] = i[15]
            returnVal.append(lecture)
        return returnVal

    def _ListBase__getRemoteList(self):
        lectureData = self.__scrapLectureData(self.__semesterCode)
        return lectureData

    def _ListBase__updateLocalList(self, local, remote):

        raise NotImplementedError

    # 강의데이터에 들어갈 항목들을 학기별로 정제
    def __scrapLectureData(self,semesterCode):
        lectureDataList = []
        user = User.getInstance()
        user.sessionGet("https://eclass.dongguk.edu/Main.do?cmd=viewHome")  # 홈으로 초기화
        # 페이지 이동
        # https://eclass.dongguk.edu/Main.do?cmd=moveMenu&mainDTO.parentMenuId=menu_00026&mainDTO.menuId=menu_00031
        url = "https://eclass.dongguk.edu/Main.do"
        params = {'cmd': 'moveMenu',
                  'mainDTO.parentMenuId': 'menu_00026',
                  'mainDTO.menuId': 'menu_00031'}
        user.sessionPost(url, params)

        # https://eclass.dongguk.edu/Study.do?cmd=viewLearnerCourseList&boardInfoDTO.boardInfoGubun=learnercourse&courseTermId=CORS_13080613542906b2006c
        url = "https://eclass.dongguk.edu/Study.do"
        params = {'cmd': "viewLearnerCourseList",
                  'boardInfoDTO.boardInfoGubun': "learnercourse",
                  'courseTermId':semesterCode}
        response = user.sessionPost(url,params)
        soup = BeautifulSoup(response.text,'html.parser')
        soupResult = soup.find_all('table',{'class':'boardListBasic'})
        if soupResult.__len__() is not 0:
            soup = soupResult[0]
            for item in soup.tbody:
                lecture = {}
                lecture.clear()
                if item != "\n":
                    exp = r"""(?<=<td><a href="javascript:viewStudyHome\(').+(?='\)">)"""
                    m = re.search(exp, str(item))
                    lecture['lectureCode'] = m.group()
                    exp = r"""(?<='\)">).+(?=</a></td>)"""
                    m = re.search(exp, str(item))
                    lecture['lectureName'] = m.group()

                    # https://eclass.dongguk.edu/Course.do?cmd=viewCourseInfo&boardInfoDTO.boardInfoGubun=course_info&courseDTO.courseId=S2017U0002003UDES330701&mainDTO.parentMenuId=menu_00047&mainDTO.menuId=menu_00053
                    url = "https://eclass.dongguk.edu/Course.do"
                    params = {'cmd': 'viewCourseInfo',
                              'boardInfoDTO.boardInfoGubun':'course_info',
                              'courseDTO.courseId':lecture['lectureCode'],
                              'mainDTO.parentMenuId': 'menu_00047',
                              'mainDTO.menuId': 'menu_00053'}
                    response = user.sessionPost(url,params)
                    soup = BeautifulSoup(response.text, 'html.parser')

                    soupResult = soup.find_all('h1',{'class':'f40'})
                    tempSoup = soupResult[0]
                    exp = r"""(?<=\n\t\t\t\t_).{2}"""
                    m = re.search(exp, str(tempSoup.a.text))
                    lecture['classNumber'] = m.group()

                    soupResult = soup.find_all('table',{'summary':'강의실에 관련한 기본정보 리스트입니다.'})
                    tempSoup = soupResult[0]
                    exp = r"""(?<=</i>학수번호\n\t\t\t\t</th>\n<td class="textLeft">\n\t\t\t\t\t).*"""
                    m = re.search(exp, str(tempSoup))
                    lecture['academicNumber'] = m.group()
                    exp = r"""(?<=</i>학점\n\t\t\t\t</th>\n<td class="textLeft">\n\t\t\t\t\t).*(?=학점)"""
                    m = re.search(exp, str(tempSoup))
                    lecture['grades'] = m.group()
                    exp = r"""(?<=</i>수강생수\n\t\t\t\t</th>\n<td class="textLeft">\n\t\t\t\t\t).*(?=명)"""
                    m = re.search(exp, str(tempSoup))
                    lecture['totalStudentNumber'] = m.group()

                    soupResult = soup.find_all('table', {'summary': '강의실에 관련한 과목운영자 리스트입니다.'})
                    tempSoup = soupResult[0]
                    assistantCount = 0
                    for tr in tempSoup.find_all('tr'):
                        tds = tr.find_all('td')
                        if tds.__len__() is not 0:

                            if (tds[1].text=="책임교수"):
                                lecture['professorName'] = tds[3].text
                                lecture['professorMail'] = tds[5].text
                            elif (tds[1].text=="조교"):
                                if assistantCount <= 2:
                                    assistantCount+=1
                                    lecture['assistant' + str(assistantCount) + 'Name'] = tds[3].text
                                    lecture['assistant' + str(assistantCount) + 'Mail'] = tds[5].text

                    #https://eclass.dongguk.edu/Course.do?cmd=viewCoursePlanChapterListNew&boardInfoDTO.boardInfoGubun=course_plan&courseDTO.courseId=S2017U0002001UCSE402902&mainDTO.parentMenuId=menu_00047&mainDTO.menuId=menu_00052
                    url = "https://eclass.dongguk.edu/Course.do"
                    params = {'cmd': 'viewCoursePlanChapterListNew',
                              'boardInfoDTO.boardInfoGubun': 'course_plan',
                              'courseDTO.courseId': lecture['lectureCode'],
                              'mainDTO.parentMenuId': 'menu_00047',
                              'mainDTO.menuId': 'menu_00052'}
                    response = user.sessionPost(url, params)
                    soup = BeautifulSoup(response.text, 'html.parser')
                    soupResult = soup.find_all('table', {'summary': '강의계획서에 관련한 기본정보 리스트입니다.'})
                    tempSoup = soupResult[0]

                    exp = r"""(?<=<th class="head">강의실/수업시간</th>\n<td class="textLeft" colspan="3">).*(?=</td>)"""
                    m = re.search(exp, str(tempSoup))
                    lecture['dateTime'] = m.group()
                    exp = r"""(?<=<tr>\n<th class="head">연락처2\(휴대폰\)</th>\n<td class="textLeft">).*(?=</td>)"""
                    m = re.search(exp, str(tempSoup))
                    if m is not None :
                        lecture['professorContact'] = m.group()
                    else:
                        lecture['professorContact'] = ""

                    someAssist = {}
                    exp = r"""(?<=<th class="head">연락처2\(휴대폰\)</th>\n<td class="textLeft">).*(?=</td>\n</tr>)"""
                    m = re.search(exp,str(soup))
                    if m is not None :
                        someAssist['contact'] = m.group()
                    else:
                        someAssist['contact'] = ""

                    exp = r"""(?<=<th class="head">이름</th>\n<td class="textLeft">).*(?=</td>\n</tr>)"""
                    m = re.search(exp, str(soup))
                    if m is not None :
                        someAssist['name'] = m.group()
                    else:
                        someAssist['name'] = ""
                    exp = r"""(?<=<th class="head">e\-메일</th>\n<td class="textLeft">).*(?=</td>\n</tr>)"""
                    m = re.search(exp, str(soup))
                    if m is not None:
                        someAssist['mail'] = m.group()
                    else:
                        someAssist['mail'] = ""
                    for i in range(1,3):
                        if  'assistant'+str(i)+'Name' in lecture: #조교가 있을때
                            if ((lecture['assistant'+str(i)+'Name'] == someAssist['name']) or
                                (lecture['assistant' + str(i) + 'Mail'] == someAssist['mail'])) and not(
                                    ((lecture['assistant'+str(i)+'Name'] =="")or (lecture['assistant' + str(i) + 'Mail']==""))):
                                lecture['assistant' + str(i) + 'Contact'] = someAssist['contact']
                                if (lecture['assistant'+str(i)+'Mail'] != someAssist['mail']):
                                    lecture['assistant' + str(i) + 'Mail'] += ' / '+someAssist['mail']
                    lectureDataList.append(lecture)
        return lectureDataList

    def addList(self,lecture):
        raise NotImplementedError


class LectureFactory():
    __instance = None

    def __init__(self):
        if self.__Instance is not None:
            raise ValueError("instance already exist!")
        else:
            #constructor
            raise NotImplementedError

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = LectureFactory()
        return cls.__instance

    def createLecture(self):
        raise NotImplementedError


class System():
    __instance = None

    def __init__(self):
        raise NotImplementedError

    @classmethod
    def getInstace(cls):
        raise NotImplementedError

    # 프로그램 실행시 체크
    def InitCheck(self):
        # 디렉토리 존재유무
        # 데이터베이스 존재유무
        # 네트워크 연결여부 검사
        raise NotImplementedError

    # 프로그램이 설치 후 최초로 실행되었을때
    def firstCheck(self):
        raise NotImplementedError

    # 자동저장 프로시저
    def autoSave(self):
        raise NotImplementedError

    # 로깅
    def logging(self):
        raise NotImplementedError

if __name__ == "__main__":
    user = User.getInstance()
    stNum = input("사용자 학번을 입력하세요 : ")
    stPW = input("비밀번호를 입력하세요 : ")
    print('로그인중..')
    if user.login(stNum, stPW) is not True:
        print('로그인 실패')
        exit()
    print('로그인 성공! '+ user.getInfo('name') + '님, 환영합니다.')
    
    print('로컬데이터베이스 연결중..')
    data = Data.getInstance()
    if data.getInfo('connection') is not True:
        print('로컬데이터베이스 연결 실패! 관리자에게 문의하세요')
        exit()
    print('로컬데이터베이스 연결 성공.')
    print('\n학기 목록을 조회합니다..')
    semesterList = SemesterList.getInstance()
    print("학기목록 조회 & 업데이트 완료")

    print("\n학기에 해당하는 강의정보를 불러옵니다.")
    lectureList = LectureList.getIntance('CORS_170221A123822I0f1040')
