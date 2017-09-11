import rsa, requests, yaml
from bs4 import BeautifulSoup
import copy,io, os.path
import sqlite3


config_path = "C:\\eclass\\"
user_config = "user_info.yaml"  # 사용자 id,pw 수강강좌 목록
# 강의별 글 목록 상태 등을 저장 ==> sqlite 로 대체 예정
# 과제목록 저장 ==> sqlite
##단일사용자를 위한 시스템임
class Lecture:
    """
    """

#사용자 클래스. 사용자 정보, 세션정보를 다룬다.
class User:
    user_info = None
    session = None
    def __init__(self):
        self.session = requests.Session()

    def user_check(self):
        if os.path.exists(config_path + user_config):
            return True
        else:
            return False

    #사용자 정보가 있을경우
    def load_file(self):
        # 파일이 존재할 경우
        print("File exist! 사용자 정보를 읽어옵니다.")
        # stream = open(config_path + user_config, 'r')
        stream = io.FileIO(config_path + user_config, 'r')
        self.user_info = yaml.load(stream)
        stream.close()
    
    #처음 사용
    def init(self,id_p, pw_p):
        self.user_info['id'] = id_p
        self.user_info['pw'] = pw_p
        self.user_info['lecture'] = {}
        stream = open(config_path + user_config, 'w')
        yaml.dump(self.user_info, stream, default_flow_style=False)
        stream.close()

    def login(self):
        if ((self.user_info['id'].__len__()==0)or(self.user_info['pw'].__len__()==0)):
            print("사용자 정보가 제대로 초기화 되지 않았습니다.")
            return False
        else:
            id = str(self.user_info['id']).encode()
            pw = self.user_info['pw'].encode()
            url = "https://eclass.dongguk.edu/User.do"
            params = {'cmd': 'getRsaPublicKey'}
            response = self.session.get(url, params=params)
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
            self.session.post(url, data=params)
            response = self.session.get("https://eclass.dongguk.edu/Main.do?cmd=viewHome")

            # 로그인 성공 여부 체크
            if response.text.find(str(self.user_info['id'])) == -1:
                return False
            else:
                return True

#데이터베이스 클래스
class Db:

    def __init__(self,id_p):
        self.conn = sqlite3.connect(id_p+".db")

    #프로그램을 처음 사용하는경우
    def init(self):
        c = self.conn.cursor()
        #<ARTICLE> (lecture_code, 구분(공지사항/학습자료실), B_ID, LINK, 등록 시간, 읽은 시간)
        c.execute("""CREATE TABLE article (lecture_code, gubun, board_id, link, write_time, read_time, is_done)""")
        #<ASSIGN> (lecture_code, 과제명, 기간, is_done) 등등...
        #공지사항, 학습자료실의 목록과는 별도의 테이블로 운영
        self.conn.commit()


# user_info.yaml 과 비교해서 강좌 목록 변경을 확인함
def lecture_init(user_info, session):
    response = session.get("https://eclass.dongguk.edu/Main.do?cmd=viewHome")
    soup = BeautifulSoup(response.text, 'html.parser')
    result = soup.find_all("option")
    lecture_num = result.__len__()
    tmp_info = copy.deepcopy(user_info)
    tmp_info['lecture'] = {}
    for i in range(1, lecture_num):
        lecture_code, pf_name, null = result[i].attrs['value'].split(',')
        tmp_info['lecture'].update({lecture_code: pf_name})
    if (user_info['lecture'].__len__() < tmp_info['lecture'].__len__()):
        print("수강목록이 변경(추가)이 감지 되었습니다.")
        # 강좌가 새로 추가되었을때
    elif (user_info['lecture'].__len__() > tmp_info['lecture'].__len__()):
        print("수강목록이 변경(감소)이 감지 되었습니다.")
        # 강좌가 삭제되었을때
    else:
        print("수강목록이 변경이 감지 되었습니다.")
    print("현재 사용자 정보")
    print(user_info)
    print("변경된 사용자 정보")
    print(tmp_info)
    # 개수는 똑같으나 개수가 변경되었을 경우

#공지사항 크롤링
def get_notice(session, lecture_code):
    url = "https://eclass.dongguk.edu/Course.do"
    params = {'cmd': 'viewBoardContentsList',
              'boardInfoDTO.boardInfoGubun': 'notice',
              'boardInfoDTO.boardInfoId': lecture_code + 'N',
              'boardInfoDTO.boardClass': 'notice',
              'boardInfoDTO.boardType': 'course',
              'courseDTO.courseId': lecture_code,
              'mainDTO.parentMenuId': 'menu_00048',
              'mainDTO.menuId': 'menu_00056'}
    response = session.get(url, params=params)
    soup = BeautifulSoup(response.text, 'html.parser')
    result = soup.find_all("table", {"class": "boardListBasic"})
    if (result.__len__() != 0):
        result = result[0].contents[5]
        article_num = result.contents.__len__() - 1

        for i in range(article_num // 2):
            now_article = result.contents[i * 2 + 1]
            tmp = now_article.contents[3].find_all('a', {"class": "fcBlack"})
            if (tmp.__len__() == 0):
                tmp = now_article.contents[3].find_all('a', {"class": "clip boardTitleNcontent TITLE_ORIGIN"})

            javascript_code = tmp[0].attrs['href']
            print(javascript_code)
            print(now_article.contents[3].text.strip())  # 글 제목
            print(now_article.contents[7].text.strip())  # 작성자
            print(now_article.contents[9].text.strip())  # 작성일자
            print("이상!!!")
    else:
        print("공지내용이 없습니다.")

#학습자료실 크롤링
def get_refer(session, lecture_code):  # 학습자료실
    url = "https://eclass.dongguk.edu/Main.do"
    params = {'cmd': 'moveCourseMenu',
              'courseDTO.courseId': lecture_code,
              'mainDTO.parentMenuId': 'menu_00091',
              'mainDTO.menuId': 'menu_00232'}
    response = session.get(url, params=params)
    soup = BeautifulSoup(response.text, 'html.parser')
    result = soup.find_all("table", {"class": "boardListBasic"})
    if (result.__len__() != 0):
        result = result[0].contents[5]
        article_num = result.contents.__len__() - 1

        for i in range(article_num // 2):
            now_article = result.contents[i * 2 + 1]
            try :
                tmp = now_article.contents[3].find_all('a')
            except:
                print("학습자료실에 등록된 내용이 없습니다.")
                break
            javascript_code = tmp[0].attrs['href']
            print(javascript_code)
            print(now_article.contents[3].text.strip())  # 글 제목
            print(now_article.contents[7].text.strip())  # 작성자
            print(now_article.contents[9].text.strip())  # 작성일자
            print("이상!!!")
    else:
        print("학습자료실에 등록된 내용이 없습니다.")

#과제 크롤링
def get_assign(session, lecture_code):
    #과목정보 갱신
    url = "https://eclass.dongguk.edu/Course.do"
    params = {'cmd': 'viewStudyHome',
              'courseDTO.courseId': lecture_code,
              'boardInfoDTO.boardInfoGubun':'study_home',
              'gubun': 'study_course'}
    session.get(url, params=params)

    url = "https://eclass.dongguk.edu/Main.do"
    params = {'cmd': 'moveCourseMenu',
              'courseDTO.courseId': lecture_code,
              'mainDTO.parentMenuId': 'menu_00104',
              'mainDTO.menuId': 'menu_00063'}
    response = session.get(url, params=params)

    soup = BeautifulSoup(response.text, 'html.parser')
    result = soup.find_all("div", {"id": "listBox"})
    if (result.__len__() != 0):
        result = result[0].contents
        article_num = result.__len__() - 3

        for i in range(article_num // 2):
            #3 5 7 9 11
            #0 1 2 3 4
            now_article = result[i * 2 + 3]
            #여기서부터 수정
            tmp = now_article.find_all("ul",{"class":"btnBox"})
            if tmp.__len__() == 0:
                print("등록된 과제내용이 없습니다.")
                break
            try:
                javascript_code = tmp[0].contents[5].next.attrs['onclick']
            except:
                javascript_code = "Invalid"
            print(javascript_code) # 자바 코드
            tmp = now_article.find_all("i",{"class":"icon-openbook-color mr10"})
            print(tmp[0].next.strip())  # 과제 글 제목
            tmp = now_article.find_all("tbody")
             #제출정보
            print(tmp[0].contents[1].contents[1].text.strip())  # 마감기간
            print(tmp[0].contents[1].contents[13].text.strip())  # 제출유무


            print("이상!!!")
    else:
        print("err")


user = User()
if user.user_check():
    user.load_file()
else:
    user.init()

if (user.login()):
    print("로그인 성공")
else :
    print("로그인 실패")


# S2017U0002003UCSE405802 쏘공
# S2017U0002003UDES330701 개별연구
# S2017U0002003UCSE202401 프언개
# S2017U0002003UCSE406601 종설1
# S2017U0002003UCSE403402 컴구조
# S2017U0002003UCSE403501 프언개
# S2017U0002003UCSE403602 인공지능
# S2017U0002003UCSE403802 데통

#lecture_init(user.user_info,user.session)
lec_code = "S2017U0002003UCSE403802"
print()
print("공지사항을 가져옵니다..")
get_notice(user.session,lec_code)
print()
print("학습자료실 목록 가져옵니다..")
get_refer(user.session,lec_code)
print()
print("과제 목록 가져옵니다..")
get_assign(user.session,lec_code)

