from abc import *


# 학기목록, 강의목록, 과제목록, 공지사항목록, 학습자료실 목록에 사용
class ListBase(metaclass=ABCMeta):

    @abstractmethod
    def __init(self):
        pass

    @abstractmethod
    def __getLocalList(self):
        pass

    @abstractmethod
    def __getRemoteList(self):
        pass

    @abstractmethod
    def __updateLocalList(self):
        pass


if __name__ == "__main__":
    pass
