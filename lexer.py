from __future__ import annotations
from abc import ABC, abstractmethod
import re


class Lexer:

    _collector: TokenCollector
    _lineNumber: int
    _position: int

    def __init__(self, collector: TokenCollector):
        self._collector = collector
    
    def lex(self, s: str):
        self._lineNumber = 1
        lines = s.split("\n")
        for line in lines:
            self.lexLine(line)
            self._lineNumber += 1
    
    def lexLine(self, line: str):
        self._position = 0
        while self._position < len(line):
            self.lexToken(line)
    
    def lexToken(self, line: str):
        if not self.findToken(line):
            self._collector.error(self._lineNumber, self._position + 1)
            self._position += 1
    
    def findToken(self, line: str) -> bool:
        return self.findWhiteSpace(line) or \
            self.findSingleCharacterToken(line) or \
            self.findName(line)
    
    whitePattern = re.compile(r"\s+")

    def findWhiteSpace(self, line: str) -> bool:
        m = self.whitePattern.match(line[self._position:])
        if m:
            self._position += m.end()
            return True
        return False

    def findSingleCharacterToken(self, line: str) -> bool:
        c = line[self._position]
        match c:
            case "{":
                self._collector.openBrace(self._lineNumber, self._position)
            case "}":
                self._collector.closeBrace(self._lineNumber, self._position)
            case "(":
                self._collector.openParen(self._lineNumber, self._position)
            case ")":
                self._collector.closeParen(self._lineNumber, self._position)
            case "<":
                self._collector.openAngle(self._lineNumber, self._position)
            case ">":
                self._collector.closeAngle(self._lineNumber, self._position)
            case "-":
                self._collector.dash(self._lineNumber, self._position)
            case ":":
                self._collector.colon(self._lineNumber, self._position)
            case _:
                return False
        self._position += 1
        return True

    namePattern = re.compile(r"\w+")

    def findName(self, line: str) -> bool:
        m = self.namePattern.match(line[self._position:])
        if m:
            self._collector.name(m.group(0), self._lineNumber, self._position)

            self._position += m.end()
            return True
        return False


    class TokenCollector(ABC):

        @abstractmethod
        def openBrace(self, line: int, pos: int):
            pass
        
        @abstractmethod
        def closeBrace(self, line: int, pos: int):
            pass

        @abstractmethod
        def openParen(self, line: int, pos: int):
            pass

        @abstractmethod
        def closeParen(self, line: int, pos: int):
            pass

        @abstractmethod
        def openAngle(self, line: int, pos: int):
            pass

        @abstractmethod
        def closeAngle(self, line: int, pos: int):
            pass

        @abstractmethod
        def dash(self, line: int, pos: int):
            pass

        @abstractmethod
        def colon(self, line: int, pos: int):
            pass

        @abstractmethod
        def name(self, name: str, line: int, pos: int):
            pass

        @abstractmethod
        def error(self, line: int, pos: int):
            pass
