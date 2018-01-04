from common import *
from user import *
from data import *
from bs4 import BeautifulSoup


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


if __name__ == "__main__":
    pass
