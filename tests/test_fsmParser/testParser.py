from fsmParser import PE, Parser
from fsmParser.syntaxBuilder import SyntaxBuilder
from lexer import Lexer


import unittest


class TestParser(unittest.TestCase):
    _lexer: Lexer
    _parser: Parser
    _builder: SyntaxBuilder

    def setUp(self) -> None:
        self._builder = SyntaxBuilder()
        self._parser = Parser(self._builder)
        self._lexer = Lexer(self._parser)

    def _assertParseResult(self, s: str, expected: str):
        self._lexer.lex(s)
        self._parser.handleEvent(PE.EOF, -1, -1)
        self.assertEqual(expected, str(self._builder.getFsm()))

    def _assertParseError(self, s: str, expected: str):
        self._lexer.lex(s)
        self._parser.handleEvent(PE.EOF, -1, -1)
        self.assertEqual(expected, str(self._builder.getFsm().getError()))
