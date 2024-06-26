
import unittest

from lexer import Lexer


class TestLexer(unittest.TestCase, Lexer.TokenCollector):
    tokens: str = ""
    lexer: Lexer
    _firstToken: bool = True

    def setUp(self) -> None:
        self.lexer = Lexer(self)
    
    def addToken(self, token: str):
        if not self._firstToken:
            self.tokens += ","
        self.tokens += token
        self._firstToken = False
    

    def _assertLexResult(self, s: str, expected: str):
        self.lexer.lex(s)
        self.assertEqual(expected, self.tokens)

    def openBrace(self, line: int, pos: int):
        return self.addToken("OB")
    
    def closeBrace(self, line: int, pos: int):
        return self.addToken("CB")
    
    def openParen(self, line: int, pos: int):
        return self.addToken("OP")
    
    def closeParen(self, line: int, pos: int):
        return self.addToken("CP")
    
    def openAngle(self, line: int, pos: int):
        return self.addToken("OA")
    
    def closeAngle(self, line: int, pos: int):
        return self.addToken("CA")
    
    def dash(self, line: int, pos: int):
        return self.addToken("D")
    
    def colon(self, line: int, pos: int):
        return self.addToken("C")
    
    def name(self, name: str, line: int, pos: int):
        return self.addToken(f"#{name}#")
    
    def error(self, line: int, pos: int):
        return self.addToken(f"E{line}/{pos}")
    

class TestSingleCharacterTokens(TestLexer):

    def test_findsOpenBrace(self):
        self._assertLexResult("{", "OB")

    def test_findsCloseBrace(self):
        self._assertLexResult("}", "CB")

    def test_findsOpenParen(self):
        self._assertLexResult("(", "OP")

    def test_findsCloseParen(self):
        self._assertLexResult(")", "CP")
    
    def test_findsOpenAngle(self):
        self._assertLexResult("<", "OA")

    def test_findsCloseAngle(self):
        self._assertLexResult(">", "CA")

    def test_findsDash(self):
        self._assertLexResult("-", "D")

    def test_findsColon(self):
        self._assertLexResult(":", "C")

    def test_findsName(self):
        self._assertLexResult("name", "#name#")
    
    def test_findsComplexName(self):
        self._assertLexResult("Room_123", "#Room_123#")
    
    def test_error(self):
        self._assertLexResult("!", "E1/1")

    def test_nothingButWhiteSpace(self):
        self._assertLexResult("   ", "")

    def test_whiteSpaceBefore(self):
        self._assertLexResult(" \t\n -", "D")


class TestMultipleTokens(TestLexer):

    def test_simpleSequence(self):
        self._assertLexResult("{}", "OB,CB")
    
    def test_complexSequence(self):
        self._assertLexResult("FSM:fsm{this}", "#FSM#,C,#fsm#,OB,#this#,CB")

    def test_complexSequenceWithErrors(self):
        self._assertLexResult(
            "{}()<>-: name .", "OB,CB,OP,CP,OA,CA,D,C,#name#,E1/15")


    def test_multipleLines(self):
        self._assertLexResult(
            "FSM:fsm. \n{bob-.}", "#FSM#,C,#fsm#,E1/8,OB,#bob#,D,E2/6,CB")

if __name__ == "__main__":
    unittest.main()