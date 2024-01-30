from abc import ABC, abstractmethod


class Exercise(ABC):
    @abstractmethod
    def provide_description(self):
        pass
