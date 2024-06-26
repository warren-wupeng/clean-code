
from abc import ABC, abstractmethod

from fsmParser.parserEvent import ParserEvent
from fsmParser.parserState import ParserState


class Builder(ABC):

    @property
    def name(self) -> str:
        raise NotImplementedError

    @name.setter
    def name(self, name: str):
        raise NotImplementedError

    @abstractmethod
    def addAction(self):
        pass

    @abstractmethod
    def addHeaderWithValue(self):
        pass

    @abstractmethod
    def done(self):
        pass

    @abstractmethod
    def newHeaderWithName(self):
        pass

    @abstractmethod
    def setStateName(self):
        pass

    @abstractmethod
    def setEvent(self):
        pass

    @abstractmethod
    def setNullEvent(self):
        pass

    @abstractmethod
    def setSuperStateName(self):
        pass

    @abstractmethod
    def setEntryAction(self):
        pass

    @abstractmethod
    def setExitAction(self):
        pass

    @abstractmethod
    def setNextState(self):
        pass

    @abstractmethod
    def setNullNextState(self):
        pass

    @abstractmethod
    def transitionWithAction(self):
        pass

    @abstractmethod
    def transitionNullAction(self):
        pass

    @abstractmethod
    def headerError(
            self, state: ParserState, event: ParserEvent, line: int, pos: int):
        pass

    @abstractmethod
    def stateSpecError(
            self, state: ParserState, event: ParserEvent, line: int, pos: int):
        pass

    @abstractmethod
    def transitionError(
            self, state: ParserState, event: ParserEvent, line: int, pos: int):
        pass

    @abstractmethod
    def transitionGroupError(
            self, state: ParserState, event: ParserEvent, line: int, pos: int):
        pass

    @abstractmethod
    def endError(
            self, state: ParserState, event: ParserEvent, line: int, pos: int):
        pass

    @abstractmethod
    def syntaxError(self, line: int, pos: int):
        pass
