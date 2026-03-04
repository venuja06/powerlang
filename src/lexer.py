# ================================
# PowerLang Compiler v0.1
# lexer.py - Tokenizer Engine
# ================================

import re
from tokens import TOKEN_TYPES


# ── Token Class ───────────────────
class Token:
    """
    One piece of PowerLang code.

    Example:
      48V becomes TWO tokens:
      Token(INTEGER, '48', line 6)
      Token(UNIT_V,  'V',  line 6)
    """
    def __init__(self, type, value, line):
        self.type  = type
        self.value = value
        self.line  = line

    def __repr__(self):
        return (f"  [{self.type:<20}]"
                f"  '{self.value}'"
                f"  (line {self.line})")


# ── Lexer Error ───────────────────
class LexerError(Exception):
    """
    Raised when an unknown
    character is found
    """
    def __init__(self, char, line):
        self.char = char
        self.line = line
        super().__init__(
            f"\n  LEXER ERROR line {line}:\n"
            f"  Unknown: '{char}'\n"
            f"  Check your PowerLang code!"
        )


# ── Lexer Class ───────────────────
class Lexer:
    """
    Step 1 of PowerLang compilation.

    Input:  raw source code text
    Output: list of Token objects
    """

    def __init__(self, source_code):
        self.source = source_code
        self.tokens = []
        self.line   = 1

    def tokenize(self):
        pos = 0

        while pos < len(self.source):
            match = None

            for token_type, pattern in TOKEN_TYPES:
                regex = re.compile(pattern)
                match = regex.match(
                    self.source, pos
                )

                if match:
                    value = match.group(0)

                    if token_type == 'NEWLINE':
                        self.line += 1

                    elif token_type not in (
                        'SKIP', 'COMMENT'
                    ):
                        self.tokens.append(
                            Token(
                                token_type,
                                value,
                                self.line
                            )
                        )

                    pos = match.end()
                    break

            if not match:
                raise LexerError(
                    self.source[pos],
                    self.line
                )

        return self.tokens