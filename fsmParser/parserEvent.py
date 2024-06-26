
from enum import Enum


class ParserEvent(Enum):
    OPEN_BRACE = 'OPEN_BRACE'
    CLOSE_BRACE = 'CLOSE_BRACE'
    OPEN_PAREN = 'OPEN_PAREN'
    CLOSE_PAREN = 'CLOSE_PAREN'
    OPEN_ANGLE = 'OPEN_ANGLE'
    CLOSE_ANGLE = 'CLOSE_ANGLE'
    DASH = 'DASH'
    COLON = 'COLON'
    NAME = 'NAME'
    EOF = 'EOF'
