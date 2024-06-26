
from .testParser import TestParser


class AcceptanceTest(TestParser):

    def test_simpleOneCoinTurns(self):
        self._assertParseResult(
            "" +
            "Actions: Turnstile\n" +
            "FSM: OneCoinTurnstile\n" +
            "Initial: Locked\n" +
            "{\n" +
            "  Locked\tCoin\tUnlocked\t{alarmOff unlock}\n" +
            "  Locked \tPass\tLocked\t\talarmOn\n" +
            "  Unlocked\tCoin\tUnlocked\tthankyou\n" +
            "  Unlocked\tPass\tLocked\t\tlock\n" +
            "}",
            "" +
            "Actions:Turnstile\n" +
            "FSM:OneCoinTurnstile\n" +
            "Initial:Locked\n" +
            "{\n" +
            "  Locked Coin Unlocked {alarmOff unlock}\n" +
            "  Locked Pass Locked alarmOn\n" +
            "  Unlocked Coin Unlocked thankyou\n" +
            "  Unlocked Pass Locked lock\n" +
            "}\n" +
            ".\n"
        )

    def test_twoCoinTurnsileWithoutSuperState(self):
        self._assertParseResult(
            "" +
            "Actions: Turnstile\n" +
            "FSM: TwoCoinTurnstile\n" +
            "Initial: Locked\n" +
            "{\n" +
            "\tLocked {\n" +
            "\t\tPass\tAlarming\talarmOn\n" +
            "\t\tCoin\tFirstCoin\t-\n" +
            "\t\tReset\tLocked\t{lock alarmOff}\n" +
            "\t}\n" +
            "\t\n" +
            "\tAlarming\tReset\tLocked {lock alarmOff}\n" +
            "\t\n" +
            "\tFirstCoin {\n" +
            "\t\tPass\tAlarming\t-\n" +
            "\t\tCoin\tUnlocked\tunlock\n" +
            "\t\tReset\tLocked {lock alarmOff}\n" +
            "\t}\n" +
            "\t\n" +
            "\tUnlocked {\n" +
            "\t\tPass\tLocked\tlock\n" +
            "\t\tCoin\t-\t\tthankyou\n" +
            "\t\tReset\tLocked {lock alarmOff}\n" +
            "\t}\n" +
            "}",
            "" +
            "Actions:Turnstile\n" +
            "FSM:TwoCoinTurnstile\n" +
            "Initial:Locked\n" +
            "{\n" +
            "  Locked {\n" +
            "    Pass Alarming alarmOn\n" +
            "    Coin FirstCoin {}\n" +
            "    Reset Locked {lock alarmOff}\n" +
            "  }\n" +
            "  Alarming Reset Locked {lock alarmOff}\n" +
            "  FirstCoin {\n" +
            "    Pass Alarming {}\n" +
            "    Coin Unlocked unlock\n" +
            "    Reset Locked {lock alarmOff}\n" +
            "  }\n" +
            "  Unlocked {\n" +
            "    Pass Locked lock\n" +
            "    Coin null thankyou\n" +
            "    Reset Locked {lock alarmOff}\n" +
            "  }\n" +
            "}\n" +
            ".\n"
        )

    def test_twoCoinTurnsileWithSuperState(self):
        self._assertParseResult(
            "" +
            "Actions: Turnstile\n" +
            "FSM: TwoCoinTurnstile\n" +
            "Initial: Locked\n" +
            "{\n" +
            "    (Base)\tReset\tLocked\tlock\n" +
            "\n" +
            "\tLocked : Base {\n" +
            "\t\tPass\tAlarming\t-\n" +
            "\t\tCoin\tFirstCoin\t-\n" +
            "\t}\n" +
            "\t\n" +
            "\tAlarming : Base\t<alarmOn >alarmOff -\t-\t-\n" +
            "\t\n" +
            "\tFirstCoin : Base {\n" +
            "\t\tPass\tAlarming\t-\n" +
            "\t\tCoin\tUnlocked\tunlock\n" +
            "\t}\n" +
            "\t\n" +
            "\tUnlocked : Base {\n" +
            "\t\tPass\tLocked\tlock\n" +
            "\t\tCoin\t-\t\tthankyou\n" +
            "\t}\n" +
            "}",
            "" +
            "Actions:Turnstile\n" +
            "FSM:TwoCoinTurnstile\n" +
            "Initial:Locked\n" +
            "{\n" +
            "  (Base) Reset Locked lock\n" +
            "  Locked:Base {\n" +
            "    Pass Alarming {}\n" +
            "    Coin FirstCoin {}\n" +
            "  }\n" +
            "  Alarming:Base <alarmOn >alarmOff null null {}\n" +
            "  FirstCoin:Base {\n" +
            "    Pass Alarming {}\n" +
            "    Coin Unlocked unlock\n" +
            "  }\n" +
            "  Unlocked:Base {\n" +
            "    Pass Locked lock\n" +
            "    Coin null thankyou\n" +
            "  }\n" +
            "}\n" +
            ".\n")
