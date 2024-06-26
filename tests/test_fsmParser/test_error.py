from .testParser import TestParser


class ErrorTest(TestParser):

    def test_parseNothing(self):
        self._assertParseError("", 
            "Syntax error: HEADER. HEADER|EOF. line -1, position -1.\n")

    def test_headerWithNoColonOrValue(self):
        self._assertParseError("A {s e ns a}", 
            "Syntax error: HEADER. HEADER_COLON|OPEN_BRACE. line 1, position 2.\n"
        )
    
    def test_headerWithNoValue(self):
        self._assertParseError("A: {s e ns a}", 
            "Syntax error: HEADER. HEADER_VALUE|OPEN_BRACE. line 1, position 3.\n"
        )
    
    def test_transitionWayTooShort(self):
        self._assertParseError("{s}",
            "Syntax error: STATE. STATE_MODIFIER|CLOSE_BRACE. line 1, position 2.\n"
        )
    
    def test_transitionTooShort(self):
        self._assertParseError("{s e}",
            "Syntax error: TRANSITION. SINGLE_EVENT|CLOSE_BRACE. line 1, position 4.\n"
        )

    def test_transitionNoAction(self):
        self._assertParseError("{s e ns}",
            "Syntax error: TRANSITION. SINGLE_NEXT_STATE|CLOSE_BRACE. line 1, position 7.\n"
        )
    
    def test_noClosingBrace(self):
        self._assertParseError("{",
            "Syntax error: STATE. STATE_SPEC|EOF. line -1, position -1.\n"
        )

    def test_initialStateDash(self):
        self._assertParseError("{- e ns a}",
            "Syntax error: STATE. STATE_SPEC|DASH. line 1, position 1.\n"
        )
    
    def test_lexicalError(self):
        self._assertParseError("{.}",
            "Syntax error: SYNTAX. . line 1, position 2.\n"
        )