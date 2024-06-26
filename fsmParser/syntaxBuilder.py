from fsmParser.builder import Builder
from fsmParser.fsmSyntax import (
    FsmSyntax, Header, StateSpec, SubTransition, SyntaxError, Transition
)
from fsmParser.parserEvent import ParserEvent
from fsmParser.parserState import ParserState


class SyntaxBuilder(Builder):
    _fsm: FsmSyntax
    _header: Header
    _parsedName: str
    _transition: Transition
    _subtransition: SubTransition

    def __init__(self):
        self._fsm = FsmSyntax()

    @property
    def name(self) -> str:
        return self._parsedName

    @name.setter
    def name(self, name: str):
        self._parsedName = name

    def newHeaderWithName(self):
        self._header = Header()
        self._header.name = self._parsedName

    def addHeaderWithValue(self):
        self._header.value = self._parsedName
        self._fsm.headers.append(self._header)

    def setStateName(self):
        self._transition = Transition(StateSpec(self._parsedName))
        self._fsm.logic.append(self._transition)

    def done(self):
        self._fsm.done = True

    def setEvent(self):
        self._subtransition = SubTransition(self._parsedName)

    def setNullEvent(self):
        self._subtransition = SubTransition("null")

    def setNextState(self):
        self._subtransition.nextState = self._parsedName

    def setNullNextState(self):
        self._subtransition.nextState = "null"

    def setSuperStateName(self):
        self.setStateName()
        self._transition.state.abstractState = True

    def setEntryAction(self):
        self._transition.state.entryActions.append(self._parsedName)

    def setExitAction(self):
        self._transition.state.exitActions.append(self._parsedName)

    def setStateBase(self):
        self._transition.state.superStates.append(self._parsedName)

    def transitionWithAction(self):
        self._subtransition.actions.append(self._parsedName)
        self._transition.subTransitions.append(self._subtransition)

    def transitionNullAction(self):
        self._transition.subTransitions.append(self._subtransition)

    def addAction(self):
        self._subtransition.actions.append(self._parsedName)

    def headerError(
            self, state: ParserState, event: ParserEvent, line: int, pos: int):
        self._fsm.errors.append(SyntaxError(
            SyntaxError.Type.HEADER, f"{state.value}|{event.value}", line, pos))

    def stateSpecError(
            self, state: ParserState, event: ParserEvent, line: int, pos: int):
        self._fsm.errors.append(SyntaxError(
            SyntaxError.Type.STATE, f"{state.value}|{event.value}", line, pos))

    def transitionError(
            self, state: ParserState, event: ParserEvent, line: int, pos: int):
        self._fsm.errors.append(SyntaxError(
            SyntaxError.Type.TRANSITION,
            f"{state.value}|{event.value}", line, pos))

    def transitionGroupError(
            self, state: ParserState, event: ParserEvent, line: int, pos: int):
        self._fsm.errors.append(SyntaxError(
            SyntaxError.Type.TRANSITION_GROUP,
            f"{state.value}|{event.value}", line, pos))

    def endError(
            self, state: ParserState, event: ParserEvent, line: int, pos: int):
        self._fsm.errors.append(SyntaxError(
            SyntaxError.Type.END, f"{state.value}|{event.value}", line, pos))

    def syntaxError(self, line: int, pos: int):
        self._fsm.errors.append(SyntaxError(
            SyntaxError.Type.SYNTAX, "", line, pos))

    def getFsm(self) -> FsmSyntax:
        return self._fsm
