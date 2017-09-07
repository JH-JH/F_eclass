import rsa
import requests

#학생 id 와 pw. 추후 암호화 필요
id = b"st_id".encode('utf8')
pw = b"st_pw".encode('utf8')

#로그인 url
url_user = "https://eclass.dongguk.edu/User.do"
params = {'cmd':'getRsaPublicKey'}
session = requests.Session()

response = session.get(url_user,params=params)
result = response.json()
print(result)
#n,e 설정 후 Public Key 초기화
n = int(result['pubKey1'],16) #pubKey1, 256 length(hex)
e = int(result['pubKey2'],16) #pubKey2, 10001(hex) 65537(int)
pubKey = rsa.PublicKey(n,e) #Public Key setting

idCrypto = rsa.encrypt(id,pubKey)
pwCrypto = rsa.encrypt(pw,pubKey)

#hex string 으로 변환
print(idCrypto.hex())
print(pwCrypto.hex())
response = session.post(url,data = {'paramUserId':idCrypto.hex(), 'paramPassword':pwCrypto.hex()})
response = session.get("https://eclass.dongguk.edu/Main.do?cmd=viewHome")