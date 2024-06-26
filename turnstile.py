
from __future__ import annotations
from abc import ABC, abstractmethod
from enum import Enum


class TurnstileFSM(ABC):

    _state: TurnstileState

    def coin(self):
        self._state.coin(self)

    def passed(self):
        self._state.passed(self)
    
    def setState(self, state: TurnstileState):
        self._state = state


    @abstractmethod
    def alarm(self):
        pass

    @abstractmethod
    def lock(self):
        pass

    @abstractmethod
    def unlock(self):
        pass

    @abstractmethod
    def thankyou(self):
        pass

class TurnstileState(ABC):

    @abstractmethod
    def passed(self, fsm: TurnstileFSM):
        pass

    @abstractmethod
    def coin(self, fsm: TurnstileFSM):
        pass

class SimpleTurnstileFSM(TurnstileFSM):

    def alarm(self):
        print("alarm")

    def lock(self):
        print("lock")

    def unlock(self):
        print("unlock")

    def thankyou(self):
        print("thankyou")



class Locked(TurnstileState):

    def passed(self, fsm: TurnstileFSM):
        fsm.alarm()

    def coin(self, fsm: TurnstileFSM):
        fsm.unlock()
        fsm.setState(Unlocked())


class Unlocked(TurnstileState):
    
    def passed(self, fsm: TurnstileFSM):
        fsm.lock()
        fsm.setState(Locked())

    def coin(self, fsm: TurnstileFSM):
        fsm.thankyou()


class OneCoinTurnstileState(Enum):
    LOCKED = Locked()
    UNLOCKED = Unlocked()


if __name__ == "__main__":
    print("start")
    fsm = SimpleTurnstileFSM()
    fsm.setState(OneCoinTurnstileState.LOCKED.value)
    fsm.coin()
    fsm.passed()
    fsm.passed()
