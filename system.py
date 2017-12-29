import os, sqlite3
from bs4 import BeautifulSoup
import requests, rsa, re

programName = "donggukEclassHelper"

class User():
    __Instance = None
    __studentNumber = None
    __name = None
    __session = None

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

    def getInfo(self):
        return {'studentNumber':self.__studentNumber, 'name':self.__name}

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
            soup = BeautifulSoup(response.text, 'html.parser')
            exp = r"(?<="+str(studentNumber)+"\().+(?=\))"
            m = re.search(exp,response.text)
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
        # Lecture <강의코드, 교수님성함, 교수님연락처, 교수님메일, 학수번호, 분반, 수강생수, 학점, 성적비중, 한줄메모, 수업날짜, 폴더경로>
        self.__cursor.execute('''create table `Lecture` (
                                `lectureCode` TEXT NOT NULL PRIMARY KEY,
                                `professorName` TEXT,
                                `professorContact` TEXT,
                                `professorMail` TEXT,
                                `academicNumber` TEXT,
                                `classNumber` INTEGER,
                                `totalStudentNumber` INTEGER,
                                `grades` INTEGER,
                                `scoreRatio` TEXT,
                                `memo` TEXT,
                                `dateTime` TEXT,
                                `directory` TEXT
                                `semester` TEXT);
                                ''')
        # CourseList <강의코드, 학번>
        self.__cursor.execute('''create table `CourseList` (
                                `lectureCode` TEXT NOT NULL,
                                `studentNumber` INTEGER NOT NULL,
                                PRIMARY KEY (lectureCode,studentNumber) );
                                ''')
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
            self.__firstInit()
        self.__dbConnection = sqlite3.connect(self.__dataPath + "\\" + programName + ".db")
        self.__cursor = self.__dbConnection.cursor()

    def query(self, query):
        self.__cursor.execute(query)
        self.__dbConnection.commit()

class Lecture():
    #시스템 작성
    __lectureCode = None
    __academicNumber = None
    __classNumber = None
    __professorName = None
    __professorMail = None
    __professorContact = None
    __totalStudentNumber = None
    __dateTime = None
    #사용자 작성
    __scoreRatio = None
    __memo = None
    __directory = None
    __semester = None

    def __init__(self,lectureCode, academicNumber, classNumber, professorName, professorMail, profssorContact,
                 totalStudentNumber, dateTime):
        a = 1


    def updateMemo(self):
        a = 1

class LectureList():
    __instance = None
    __list = []
    __semesterList = {}

    def __init__(self):
        if self.__instance is not None:
            raise ValueError("instance already exist!")
        else:
            #constructor
            self.__init()

    @classmethod
    def getIntance(cls):
        if cls.__instance is None:
            cls.__instance = LectureList()
        return cls.__instance

    def __init(self):
        user = User.getInstance()
        userInfo = user.getInfo()
        studentNumber = userInfo['studentNumber']

        # 이수학기 파악
        self.__getSemesterList()



    def __getSemesterList(self):
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
        for option in soup:
            if option != "\n" :
                self.__semesterList[option.attrs['value']] = option.text

    def addList(self,lecture):
        NotImplementedError


class LectureFactory():
    __instance = None

    def __init__(self):
        if self.__Instance is not None:
            raise ValueError("instance already exist!")
        else:
            #constructor
            a = 1

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = LectureFactory()
        return cls.__instance

#    def createLecture(self):


user = User.getInstance()
loginResult = user.login('2013112003', 'asdf1020@@')
print(loginResult)
lectureList = LectureList.getIntance()
print(1)


'''
#Data 클래스 테스트
data = Data.getInstance()
print(1)
'''

'''
#사용자 로그인 테스트
user = User.getInstance()
loginResult = user.login('id', 'password')
print(loginResult)'''

