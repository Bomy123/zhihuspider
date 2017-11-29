from zhihuspider.items import ZhihuspiderItem
from abc import ABC, abstractmethod


class IDbTools(ABC):
    def __init__(self):
        self._register()

    @classmethod
    def getinstance(cls, *args, **kwargs):
        if cls.minstance is None:
            cls.minstance = cls(*args, **kwargs)
        return cls.minstance

    @abstractmethod
    def commit(self, item: ZhihuspiderItem): ...

    @abstractmethod
    def _register(self): ...
