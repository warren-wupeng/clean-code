"""
<FSM> ::= <header>* <logic>
<header> ::= <name> ":" <name>

<logic> ::= "{" <transition>* "}"
<transition> ::= <state-spec> <subtransition>
             |   <state-spec> "{" <subtransition>* "}"

<state-spec> ::= <state> <state-modifier>*
<state> ::= <name> | "(" <name> ")"
<state-modifier> ::=  ":" <name> | "<" <name> | ">" <name>
<subtransition> ::= <event> <next-state> <action>
<event> ::= <name> | "-"
<next-state> ::= <state> | "-"
<action> ::= <name> | "{" <name> "}" | "-"
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import Callable

from .builder import Builder
from fsmParser.parserEvent import ParserEvent as PE
from .parserState import ParserState as PS
from lexer import Lexer


@dataclass
class Transition:
    currentState: PS
    event: PE
    nextState: PS
    action: Callable[[Builder], None]


TRANSITION_TABLE = [
    (PS.HEADER, PE.NAME, PS.HEADER_COLON, lambda t: t.newHeaderWithName()),
    (PS.HEADER_COLON, PE.COLON, PS.HEADER_VALUE, lambda t: None),
    (PS.HEADER_VALUE, PE.NAME, PS.HEADER, lambda t: t.addHeaderWithValue()),
    (PS.HEADER, PE.OPEN_BRACE, PS.STATE_SPEC, lambda t: None),
    (PS.STATE_SPEC, PE.OPEN_PAREN, PS.SUPER_STATE_NAME, lambda t: None),
    (PS.STATE_SPEC, PE.NAME, PS.STATE_MODIFIER, lambda t: t.setStateName()),
    (PS.STATE_SPEC, PE.CLOSE_BRACE, PS.END, lambda t: t.done()),
    (PS.SUPER_STATE_NAME, PE.NAME, PS.SUPER_STATE_CLOSE, lambda t: t.setSuperStateName()),
    (PS.SUPER_STATE_CLOSE, PE.CLOSE_PAREN, PS.STATE_MODIFIER, lambda t: None),
    (PS.STATE_MODIFIER, PE.NAME, PS.SINGLE_EVENT, lambda t: t.setEvent()),
    (PS.STATE_MODIFIER, PE.DASH, PS.SINGLE_EVENT, lambda t: t.setNullEvent()),
    (PS.STATE_MODIFIER, PE.OPEN_BRACE, PS.SUBTRANSITION_GROUP, lambda t: None),
    (PS.STATE_MODIFIER, PE.OPEN_ANGLE, PS.ENTRY_ACTION, lambda t: None),
    (PS.STATE_MODIFIER, PE.CLOSE_ANGLE, PS.EXIT_ACTION, lambda t: None),
    (PS.STATE_MODIFIER, PE.COLON, PS.STATE_BASE, lambda t: None),
    (PS.ENTRY_ACTION, PE.NAME, PS.STATE_MODIFIER, lambda t: t.setEntryAction()),
    (PS.ENTRY_ACTION, PE.OPEN_BRACE, PS.MULTIPLE_ENTRY_ACTIONS, lambda t: None),
    (PS.MULTIPLE_ENTRY_ACTIONS, PE.NAME, PS.MULTIPLE_ENTRY_ACTIONS, lambda t: t.setEntryAction()),
    (PS.MULTIPLE_ENTRY_ACTIONS, PE.CLOSE_BRACE, PS.STATE_MODIFIER, lambda t: None),
    (PS.EXIT_ACTION, PE.NAME, PS.STATE_MODIFIER, lambda t: t.setExitAction()),
    (PS.EXIT_ACTION, PE.OPEN_BRACE, PS.MULTIPLE_EXIT_ACTIONS, lambda t: None),
    (PS.MULTIPLE_EXIT_ACTIONS, PE.NAME, PS.MULTIPLE_EXIT_ACTIONS, lambda t: t.setExitAction()),
    (PS.MULTIPLE_EXIT_ACTIONS, PE.CLOSE_BRACE, PS.STATE_MODIFIER, lambda t: None),
    (PS.SUBTRANSITION_GROUP, PE.NAME, PS.GROUP_EVENT, lambda t: t.setEvent()),
    (PS.SUBTRANSITION_GROUP, PE.CLOSE_BRACE, PS.STATE_SPEC, lambda t: None),
    (PS.GROUP_EVENT, PE.NAME, PS.GROUP_NEXT_STATE, lambda t: t.setNextState()),
    (PS.GROUP_EVENT, PE.DASH, PS.GROUP_NEXT_STATE, lambda t: t.setNullNextState()),
    (PS.GROUP_NEXT_STATE, PE.NAME, PS.SUBTRANSITION_GROUP, lambda t: t.transitionWithAction()),
    (PS.GROUP_NEXT_STATE, PE.DASH, PS.SUBTRANSITION_GROUP, lambda t: t.transitionNullAction()),
    (PS.GROUP_NEXT_STATE, PE.OPEN_BRACE, PS.GROUP_ACTION_GROUP, lambda t: None),
    (PS.GROUP_ACTION_GROUP, PE.NAME, PS.GROUP_ACTION_GROUP_NAME, lambda t: t.addAction()),
    (PS.GROUP_ACTION_GROUP, PE.CLOSE_BRACE, PS.SUBTRANSITION_GROUP, lambda t: t.transitionNullAction()),
    (PS.GROUP_ACTION_GROUP_NAME, PE.NAME, PS.GROUP_ACTION_GROUP_NAME, lambda t: t.addAction()),
    (PS.GROUP_ACTION_GROUP_NAME, PE.CLOSE_BRACE, PS.SUBTRANSITION_GROUP, lambda t: t.transitionNullAction()),
    (PS.STATE_BASE, PE.NAME, PS.STATE_MODIFIER, lambda t: t.setStateBase()),
    (PS.SINGLE_EVENT, PE.NAME, PS.SINGLE_NEXT_STATE, lambda t: t.setNextState()),
    (PS.SINGLE_EVENT, PE.DASH, PS.SINGLE_NEXT_STATE, lambda t: t.setNullNextState()),
    (PS.SINGLE_NEXT_STATE, PE.NAME, PS.STATE_SPEC, lambda t: t.transitionWithAction()),
    (PS.SINGLE_NEXT_STATE, PE.DASH, PS.STATE_SPEC, lambda t: t.transitionNullAction()),
    (PS.SINGLE_NEXT_STATE, PE.OPEN_BRACE, PS.SINGLE_ACTION_GROUP, lambda t: None),
    (PS.SINGLE_ACTION_GROUP, PE.NAME, PS.SINGLE_ACTION_GROUP_NAME, lambda t: t.addAction()),
    (PS.SINGLE_ACTION_GROUP_NAME, PE.NAME, PS.SINGLE_ACTION_GROUP_NAME, lambda t: t.addAction()),
    (PS.SINGLE_ACTION_GROUP_NAME, PE.CLOSE_BRACE, PS.STATE_SPEC, lambda t: t.transitionNullAction()),
    (PS.END, PE.EOF, PS.END, lambda t: None),
]

class Parser(Lexer.TokenCollector):
    _state: PS
    _builder: Builder

    def __init__(self, builder: Builder):
        self._builder = builder
        self._state = PS.HEADER

    def openBrace(self, line: int, pos: int):
        self.handleEvent(PE.OPEN_BRACE, line, pos)

    def closeBrace(self, line: int, pos: int):
        self.handleEvent(PE.CLOSE_BRACE, line, pos)

    def openParen(self, line: int, pos: int):
        self.handleEvent(PE.OPEN_PAREN, line, pos)

    def closeParen(self, line: int, pos: int):
        self.handleEvent(PE.CLOSE_PAREN, line, pos)

    def openAngle(self, line: int, pos: int):
        self.handleEvent(PE.OPEN_ANGLE, line, pos)

    def closeAngle(self, line: int, pos: int):
        self.handleEvent(PE.CLOSE_ANGLE, line, pos)

    def dash(self, line: int, pos: int):
        self.handleEvent(PE.DASH, line, pos)

    def colon(self, line: int, pos: int):
        self.handleEvent(PE.COLON, line, pos)

    def name(self, name: str, line: int, pos: int):
        self._builder.name = name
        self.handleEvent(PE.NAME, line, pos)

    def error(self, line: int, pos: int):
        self._builder.syntaxError(line, pos)


    transitions = [Transition(*t) for t in TRANSITION_TABLE]


    def handleEvent(self, event: PE, line: int, pos: int):
        for t in self.transitions:
            if t.currentState == self._state and t.event == event:
                self._state = t.nextState
                if t.action:
                    t.action(self._builder)
                return
        self.handleEventError(event, line, pos)

    def handleEventError(self, event: PE, line: int, pos: int):
        match self._state:
            case PS.HEADER | PS.HEADER_COLON | PS.HEADER_VALUE:
                self._builder.headerError(self._state, event, line, pos)
            case PS.STATE_SPEC | PS.STATE_MODIFIER | PS.SUPER_STATE_NAME | \
                 PS.SUPER_STATE_CLOSE | PS.ENTRY_ACTION | PS.EXIT_ACTION | \
                 PS.STATE_BASE:
                self._builder.stateSpecError(self._state, event, line, pos)
            case PS.SINGLE_EVENT | PS.SINGLE_NEXT_STATE | \
                 PS.SINGLE_ACTION_GROUP | PS.SINGLE_ACTION_GROUP_NAME:
                self._builder.transitionError(self._state, event, line, pos)
            
            case PS.SUBTRANSITION_GROUP | PS.GROUP_EVENT | \
                 PS.GROUP_NEXT_STATE | PS.GROUP_ACTION_GROUP | \
                 PS.GROUP_ACTION_GROUP_NAME:    
                self._builder.transitionGroupError(self._state, event, line, pos)
            
            case PS.END:
                self._builder.endError(self._state, event, line, pos)
