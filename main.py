import rsa
import copy
import requests
import yaml
import io
import os.path
import sqlite3
from bs4 import BeautifulSoup

config_path = "C:\\eclass\\"
user_config = "user_info.yaml" #사용자 id,pw 수강강좌 목록
lecture_config = "leture_info.yaml" #강의별 글 목록 상태 등을 저장
session = requests.Session()


##단일사용자를 위한 시스템임
class Lecture:
    """
    """

#설정 경로로부터 파일을 읽어서 사용자 정보 초기화
def user_init():
    if os.path.exists(config_path+user_config):
        #파일이 존재할 경우
        print("File exist!")
        print("사용자 정보를 읽어옵니다.")
        #stream = open(config_path + user_config, 'r')
        stream = io.FileIO(config_path+user_config,'r')
        user_info =  yaml.load(stream)
        stream.close()
    else:
        #파일이 없을경우 = 처음 접속할경우, id, pw 를 입력받아 씀
        print("사용자 정보가 없습니다. ID 와 PW 를 입력해주세요")
        user_info = {}
        user_info['id'] = input("ID : ")
        user_info['pw'] = input("PW : ")
        user_info['lecture'] = {}
        stream = open(config_path+user_config,'w')
        #stream = io.FileIO(config_path + user_config, 'w')
        yaml.dump(user_info, stream, default_flow_style=False)
        stream.close()
    return user_info

def user_login(p_id,p_pw,session):
    id = str(p_id).encode()
    pw = p_pw.encode()

    url_user = "https://eclass.dongguk.edu/User.do"
    params = {'cmd': 'getRsaPublicKey'}
    response = session.get(url_user, params=params)
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
    session.post(url_user, data=params)
    response = session.get("https://eclass.dongguk.edu/Main.do?cmd=viewHome")
    #로그인 성공 여부 체크
    if response.text.find(str(p_id)) == -1:
        return False
    else:
        return True
    
#user_info.yaml 과 비교해서 강좌 목록 변경을 확인함
def lecture_init(user_info, session):
    response = session.get("https://eclass.dongguk.edu/Main.do?cmd=viewHome")
    soup = BeautifulSoup(response.text, 'html.parser')
    result = soup.find_all("option")
    lecture_num = result.__len__()
    tmp_info = copy.deepcopy(user_info)
    tmp_info['lecture'] = {}
    for i in range(1,lecture_num):
        lecture_code, pf_name, null = result[i].attrs['value'].split(',')
        tmp_info['lecture'].update({lecture_code:pf_name})
    if (user_info['lecture'].__len__() < tmp_info['lecture'].__len__()):
        print("수강목록이 변경(추가)이 감지 되었습니다.")
        #강좌가 새로 추가되었을때
    elif (user_info['lecture'].__len__() > tmp_info['lecture'].__len__()):
        print("수강목록이 변경(감소)이 감지 되었습니다.")
        #강좌가 삭제되었을때
    else:
        print("수강목록이 변경이 감지 되었습니다.")
    print("현재 사용자 정보")
    print(user_info)
    print("변경된 사용자 정보")
    print(tmp_info)
        #개수는 똑같으나 개수가 변경되었을 경우


def get_notice(session,lecture_code):
    url = "https://eclass.dongguk.edu/Course.do"
    params = {'cmd':'viewBoardContentsList',
              'boardInfoDTO.boardInfoGubun':'notice',
              'boardInfoDTO.boardInfoId':lecture_code+'N',
              'boardInfoDTO.boardClass':'notice',
              'boardInfoDTO.boardType':'course',
              'courseDTO.courseId':lecture_code,
              'mainDTO.parentMenuId':'menu_00048',
              'mainDTO.menuId':'menu_00056'}
    response = session.get(url,params=params)
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

    

user_info = user_init()
login_result = user_login(user_info['id'],user_info['pw'],session)
if login_result == True:
    print("로그인성공! 강좌 목록조회로 넘어갑니다.")
    lecture_init(user_info, session)
    #쏘공 S2017U0002003UCSE405802
    #S2017U0002003UDES330701 뭔지모르는 손교수님꺼
    get_notice(session,"S2017U0002003UDES330701")
else:
    print("로그인실패 ㅜㅠ")


