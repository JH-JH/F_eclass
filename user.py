import requests, rsa, re


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

    def getInfo(self, t):
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
            exp = r"(?<=" + str(studentNumber) + "\().+(?=\))"
            m = re.search(exp, response.text)
            self.__studentNumber = str(studentNumber)
            self.__name = m.group()
            return True

    def sessionPost(self, url, params):
        return self.__session.post(url, data=params)

    def sessionGet(self, url):
        return self.__session.get(url)


if __name__ == "__main__":
    pass
