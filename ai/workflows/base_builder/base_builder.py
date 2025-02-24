from abc import ABC, abstractmethod


class BaseBuilder(ABC):

    @abstractmethod
    def invoke(self):
        pass

    def pretty_print_response(self, events):
        for event in events:
            event["messages"][-1].pretty_print()
