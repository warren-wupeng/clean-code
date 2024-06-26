from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum

@dataclass
class FsmSyntax:
    headers: list[Header] = field(default_factory=list)
    logic: list[Transition] = field(default_factory=list)
    errors: list[SyntaxError] = field(default_factory=list)
    done: bool = False

    def __str__(self) -> str:
        return  f"{''.join([str(h) for h in self.headers])}" + \
            self._format_logic() + \
            ".\n" if self.done else "" + \
            f"{''.join([self._formatError(e) for e in self.errors])}"

    def _format_logic(self):
        if len(self.logic) > 0:
            return "{\n"+f"{''.join([str(t) for t in self.logic])}"+"}\n"
        else:
            return ""
    
    def getError(self) -> str:
        return self._formatErrors()
    
    def _formatErrors(self) -> str:
        return self._formatError(self.errors[0]) if len(self.errors) > 0 else ""

    def _formatError(self, error: SyntaxError) -> str:
        return f"Syntax error: {error.type.value}. {error.msg}. line {error.lineNumber}, position {error.position}.\n"


class Header:
    name: str
    value: str

    def __repr__(self) -> str:
        return f"{self.name}:{self.value}\n"


@dataclass
class Transition:
    state: StateSpec
    subTransitions: list[SubTransition] = field(default_factory=list)

    def __repr__(self) -> str:
        return f"  {self.state} {self._formatSubTransactions()}\n"

    def _formatSubTransactions(self) -> str:
        if len(self.subTransitions) == 1:
            return str(self.subTransitions[0])
        else:
            result = "{\n"
            for subTransition in self.subTransitions:
                result += f"    {subTransition}\n"
            return result + "  }"

@dataclass
class StateSpec:
    name: str
    superStates: list[str] = field(default_factory=list)
    entryActions: list[str] = field(default_factory=list)
    exitActions: list[str] = field(default_factory=list)
    abstractState: bool = False

    def __repr__(self) -> str:
        stateName = f"({self.name})" if self.abstractState else f"{self.name}"
        for superState in self.superStates:
            stateName += f":{superState}"
        for entryAction in self.entryActions:
            stateName += f" <{entryAction}"
        for exitAction in self.exitActions:
            stateName += f" >{exitAction}"
        return stateName

@dataclass
class SubTransition:
    event: str
    nextState: str = ""
    actions: list[str] = field(default_factory=list)

    def __repr__(self) -> str:
        return f"{self.event} {self.nextState} {self._formatActions()}"
    
    def _formatActions(self) -> str:
        if len(self.actions) == 1:
            return self.actions[0]
        else:
            result = "{"
            first = True
            for action in self.actions:
                result += f"{'' if first else ' '}{action}"
                first = False
            return result + "}"


@dataclass
class SyntaxError:
    type: Type
    msg: str
    lineNumber: int
    position: int


    class Type(Enum):
        HEADER = 'HEADER'
        STATE = 'STATE'
        TRANSITION = 'TRANSITION'
        TRANSITION_GROUP = 'TRANSITION_GROUP'
        END = 'END'
        SYNTAX = 'SYNTAX'
