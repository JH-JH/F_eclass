from user import *
from data import *
from semester import *
from lecture import *
programName = "donggukEclassHelper"

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
