from .testParser import TestParser


class IncremmentalTest(TestParser):

    def test_parseOneHeader(self):
        self._assertParseResult("N:V{}", "N:V\n.\n")

    def test_parseManyHeaders(self):
        self._assertParseResult(" N1 : V1\tN2 : V2\n{}", "N1:V1\nN2:V2\n.\n")

    def test_noHeader(self):
        self._assertParseResult(" {}", ".\n")

    def test_simpleTransition(self):
        self._assertParseResult("{ s e ns a}", "{\n  s e ns a\n}\n.\n")

    def test_transitionWithNullActions(self):
        self._assertParseResult("{ s e ns -}", "{\n  s e ns {}\n}\n.\n")

    def test_transitionWithManyActions(self):
        self._assertParseResult("{ s e ns {a1 a2}}",
                                "{\n  s e ns {a1 a2}\n}\n.\n")

    def test_stateWithSubTransition(self):
        self._assertParseResult("{ s {e ns a}}",
                                "{\n  s e ns a\n}\n.\n")

    def test_stateWithSeveralSubTransitions(self):
        self._assertParseResult("{s {e1 ns1 a1 e2 ns2 a2}}",
                                "{\n" +
                                "  s {\n" +
                                "    e1 ns1 a1\n" +
                                "    e2 ns2 a2\n" +
                                "  }\n" +
                                "}\n" +
                                ".\n")

    def test_manyTransitions(self):
        self._assertParseResult("{s1 e1 ns1 a1 s2 e2 ns2 a2}",
                                "{\n" +
                                "  s1 e1 ns1 a1\n" +
                                "  s2 e2 ns2 a2\n" +
                                "}\n" +
                                ".\n")

    def test_superState(self):
        self._assertParseResult("{(ss) e s a}",
                                "{\n  (ss) e s a\n}\n.\n")

    def test_entryAction(self):
        self._assertParseResult("{s <ea e s a}",
                                "{\n  s <ea e s a\n}\n.\n")

    def test_exitAction(self):
        self._assertParseResult("{s >xa e s a}",
                                "{\n  s >xa e s a\n}\n.\n")

    def test_derivedState(self):
        self._assertParseResult("{s:ss e s a}",
                                "{\n  s:ss e s a\n}\n.\n")

    def test_allStateAdorments(self):
        self._assertParseResult("{(s):ss <ea >xa e s a}",
                                "{\n  (s):ss <ea >xa e s a\n}\n.\n")

    def test_stateWithNoSubTransitions(self):
        self._assertParseResult("{s {}}", "{\n  s {\n  }\n}\n.\n")

    def test_stateWithAllDashes(self):
        self._assertParseResult("{s - - -}", "{\n  s null null {}\n}\n.\n")

    def test_multipleSuperStates(self):
        self._assertParseResult("{s :x :y - - -}",
                                "{\n  s:x:y null null {}\n}\n.\n")

    def test_multipleEntryActions(self):
        self._assertParseResult("{s <x <y - - -}",
                                "{\n  s <x <y null null {}\n}\n.\n")

    def test_multipleExitActions(self):
        self._assertParseResult("{s >x >y - - -}",
                                "{\n  s >x >y null null {}\n}\n.\n")

    def test_multipleEntryAndExitActions(self):
        self._assertParseResult("{s <{u v} >{w x} - - -}",
                                "{\n  s <u <v >w >x null null {}\n}\n.\n")
