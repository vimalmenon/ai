from abc import ABC, abstractmethod


class BaseBuilder(ABC):

    @abstractmethod
    def invoke(self):
        pass
