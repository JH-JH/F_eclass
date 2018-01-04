from common import *
from user import *
from data import *
from bs4 import BeautifulSoup


class Lecture():
    # 시스템 작성
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
    # 사용자 작성
    __scoreRatio = None
    __memo = None
    __directory = None

    def __init__(self, lectureData):
        raise NotImplementedError

    def updateInfo(self, t, v):
        raise NotImplementedError

    def getInfo(self, t):
        raise NotImplementedError


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
        #
        raise NotImplementedError

    # 강의데이터에 들어갈 항목들을 학기별로 정제
    def __scrapLectureData(self, semesterCode):
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
                  'courseTermId': semesterCode}
        response = user.sessionPost(url, params)
        soup = BeautifulSoup(response.text, 'html.parser')
        soupResult = soup.find_all('table', {'class': 'boardListBasic'})
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
                              'boardInfoDTO.boardInfoGubun': 'course_info',
                              'courseDTO.courseId': lecture['lectureCode'],
                              'mainDTO.parentMenuId': 'menu_00047',
                              'mainDTO.menuId': 'menu_00053'}
                    response = user.sessionPost(url, params)
                    soup = BeautifulSoup(response.text, 'html.parser')

                    soupResult = soup.find_all('h1', {'class': 'f40'})
                    tempSoup = soupResult[0]
                    exp = r"""(?<=\n\t\t\t\t_).{2}"""
                    m = re.search(exp, str(tempSoup.a.text))
                    lecture['classNumber'] = m.group()

                    soupResult = soup.find_all('table', {'summary': '강의실에 관련한 기본정보 리스트입니다.'})
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

                            if (tds[1].text == "책임교수"):
                                lecture['professorName'] = tds[3].text
                                lecture['professorMail'] = tds[5].text
                            elif (tds[1].text == "조교"):
                                if assistantCount <= 2:
                                    assistantCount += 1
                                    lecture['assistant' + str(assistantCount) + 'Name'] = tds[3].text
                                    lecture['assistant' + str(assistantCount) + 'Mail'] = tds[5].text

                    # https://eclass.dongguk.edu/Course.do?cmd=viewCoursePlanChapterListNew&boardInfoDTO.boardInfoGubun=course_plan&courseDTO.courseId=S2017U0002001UCSE402902&mainDTO.parentMenuId=menu_00047&mainDTO.menuId=menu_00052
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
                    if m is not None:
                        lecture['professorContact'] = m.group()
                    else:
                        lecture['professorContact'] = ""

                    someAssist = {}
                    exp = r"""(?<=<th class="head">연락처2\(휴대폰\)</th>\n<td class="textLeft">).*(?=</td>\n</tr>)"""
                    m = re.search(exp, str(soup))
                    if m is not None:
                        someAssist['contact'] = m.group()
                    else:
                        someAssist['contact'] = ""

                    exp = r"""(?<=<th class="head">이름</th>\n<td class="textLeft">).*(?=</td>\n</tr>)"""
                    m = re.search(exp, str(soup))
                    if m is not None:
                        someAssist['name'] = m.group()
                    else:
                        someAssist['name'] = ""
                    exp = r"""(?<=<th class="head">e\-메일</th>\n<td class="textLeft">).*(?=</td>\n</tr>)"""
                    m = re.search(exp, str(soup))
                    if m is not None:
                        someAssist['mail'] = m.group()
                    else:
                        someAssist['mail'] = ""
                    for i in range(1, 3):
                        if 'assistant' + str(i) + 'Name' in lecture:  # 조교가 있을때
                            if ((lecture['assistant' + str(i) + 'Name'] == someAssist['name']) or
                                (lecture['assistant' + str(i) + 'Mail'] == someAssist['mail'])) and not (
                                    ((lecture['assistant' + str(i) + 'Name'] == "") or (
                                            lecture['assistant' + str(i) + 'Mail'] == ""))):
                                lecture['assistant' + str(i) + 'Contact'] = someAssist['contact']
                                if (lecture['assistant' + str(i) + 'Mail'] != someAssist['mail']):
                                    lecture['assistant' + str(i) + 'Mail'] += ' / ' + someAssist['mail']
                    lectureDataList.append(lecture)
        return lectureDataList

    def addList(self, lecture):
        raise NotImplementedError


class LectureFactory():
    __instance = None

    def __init__(self):
        if self.__Instance is not None:
            raise ValueError("instance already exist!")
        else:
            # constructor
            raise NotImplementedError

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = LectureFactory()
        return cls.__instance

    def createLecture(self):
        raise NotImplementedError


if __name__ == "__main__":
    pass
