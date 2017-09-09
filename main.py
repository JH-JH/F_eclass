import rsa
import requests
from bs4 import BeautifulSoup

session = requests.Session()

def user_login(p_id,p_pw,session):
    id = p_id.encode()
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
    #response = session.post(url_user, data=params)
    #response = session.get("https://eclass.dongguk.edu/Main.do?cmd=viewHome")
    return session

user_login("st_id","st_pw!!",session)

response = session.get("https://eclass.dongguk.edu/Main.do?cmd=viewHome")
print(response.text)