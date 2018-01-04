import os, sqlite3
import system


class Data():
    __Instance = None
    __dataPath = os.environ['LOCALAPPDATA'] + "\\" + system.programName
    __documentPath = os.environ['HOMEDRIVE'] + os.environ['HOMEPATH'] + "\\Documents\\" + system.programName
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

    # sqlite query testing : https://sqliteonline.com/
    def __firstInit(self):
        # 프로그램을 처음 설치 후 실행했을때. 디렉토리와 데이터베이스&테이블을 생성.
        os.mkdir(self.__dataPath)
        os.mkdir(self.__documentPath)

        # 데이터베이스 생성 및 테이블 정의
        # sqlite 자료형 : INTEGER, REAL, TEXT, BLOB, NULL
        # https://wikidocs.net/12454, http://lovedb.tistory.com/348 참조
        self.__dbConnection = sqlite3.connect(self.__dataPath + "\\" + system.programName + ".db")
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
        self.__dbConnection = sqlite3.connect(self.__dataPath + "\\" + system.programName + ".db")
        self.__cursor = self.__dbConnection.cursor()

    def query(self, query):
        self.__cursor.execute(query)
        self.__dbConnection.commit()

    def select(self, _select, _from, _where, _order_by=None):
        if _select == "":
            _select = "*"
        if _order_by is None:
            query = 'SELECT ' + str(_select) + ' FROM ' + str(_from) + ' WHERE ' + str(_where)
        else:
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

    def getInfo(self, t):
        if (t == 'connection'):
            if self.__dbConnection is not None:
                return True
            else:
                return False


if __name__ == "__main__":
    pass
