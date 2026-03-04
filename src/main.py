# ================================
# PowerLang Compiler v0.1
# main.py - Complete Single File
# ================================

import re

# ── Token Definitions ─────────────
# ORDER MATTERS! Units before Name!
TOKEN_TYPES = [

    # KEYWORDS
    ('CONVERTER',   r'\bconverter\b'),
    ('CONTROL',     r'\bcontrol\b'),
    ('PROTECT',     r'\bprotect\b'),
    ('MONITOR',     r'\bmonitor\b'),
    ('HARDWARE',    r'\bhardware\b'),
    ('SIGNAL',      r'\bsignal\b'),
    ('DEFINE',      r'\bdefine\b'),
    ('RETURN',      r'\breturn\b'),
    ('IMPORT',      r'\bimport\b'),

    # CONTROL TYPES
    ('PID',         r'\bpid\b'),
    ('CASCADE',     r'\bcascade\b'),
    ('SMC',         r'\bsmc\b'),
    ('MPC',         r'\bmpc\b'),

    # TOPOLOGIES
    ('BUCK',        r'\bbuck\b'),
    ('BOOST',       r'\bboost\b'),
    ('HBRIDGE',     r'\bhbridge\b'),
    ('FLYBACK',     r'\bflyback\b'),
    ('FULLBRIDGE',  r'\bfullbridge\b'),
    ('INVERTER',    r'\binverter\b'),
    ('PFC',         r'\bpfc\b'),

    # PROPERTIES
    ('SETPOINT',    r'\bsetpoint\b'),
    ('FEEDBACK',    r'\bfeedback\b'),
    ('SWITCH',      r'\bswitch\b'),
    ('INPUT',       r'\binput\b'),
    ('OUTPUT',      r'\boutput\b'),
    ('DEADTIME',    r'\bdeadtime\b'),
    ('BANDWIDTH',   r'\bbandwidth\b'),
    ('EFFICIENCY',  r'\befficiency\b'),
    ('TOPOLOGY',    r'\btopology\b'),

    # PID PARAMETERS
    ('KP',          r'\bKp\b'),
    ('KI',          r'\bKi\b'),
    ('KD',          r'\bKd\b'),

    # PROTECTION KEYWORDS
    ('OVERVOLTAGE',      r'\bovervoltage\b'),
    ('UNDERVOLTAGE',     r'\bundervoltage\b'),
    ('OVERCURRENT',      r'\bovercurrent\b'),
    ('UNDERTEMPERATURE', r'\bundertemperature\b'),
    ('OVERTEMPERATURE',  r'\bovertemperature\b'),
    ('SHORT_CIRCUIT',    r'\bshort_circuit\b'),
    ('WATCHDOG',         r'\bwatchdog\b'),

    # ACTIONS
    ('SHUTDOWN',    r'\bshutdown\b'),
    ('ALARM',       r'\balarm\b'),
    ('DERATE',      r'\bderate\b'),
    ('RESTART',     r'\brestart\b'),
    ('NOTIFY',      r'\bnotify\b'),

    # HARDWARE TARGETS
    ('STM32',       r'\bSTM32\w*'),
    ('TI_C2000',    r'\bTI_C2000\b'),
    ('ESP32',       r'\bESP32\b'),
    ('ARDUINO',     r'\bArduino\b'),

    # ── UNITS ──────────────────────
    # CRITICAL: Units MUST come
    # BEFORE NAME in this list!
    # Otherwise V, A, Hz etc get
    # recognised as NAME not UNIT!

    # Frequency units
    ('UNIT_MHZ',    r'MHz'),
    ('UNIT_KHZ',    r'kHz'),
    ('UNIT_HZ',     r'Hz'),

    # Power units
    ('UNIT_MW',     r'MW'),
    ('UNIT_KW',     r'kW'),
    ('UNIT_W',      r'W'),

    # Voltage units
    ('UNIT_MV',     r'mV'),
    ('UNIT_KV',     r'kV'),
    ('UNIT_V',      r'V'),

    # Current units
    ('UNIT_MA',     r'mA'),
    ('UNIT_A',      r'A(?![a-zA-Z_])'),

    # Inductance units
    ('UNIT_UH',     r'uH'),
    ('UNIT_MH',     r'mH'),

    # Capacitance units
    ('UNIT_UF',     r'uF'),
    ('UNIT_NF',     r'nF'),

    # Other units
    ('UNIT_PERCENT', r'%'),
    ('UNIT_DEG_C',  r'°C'),
    ('UNIT_OHM',    r'Ohm'),

    # Time units
    ('UNIT_MS',     r'ms'),
    ('UNIT_US',     r'us'),
    ('UNIT_NS',     r'ns'),
    ('UNIT_S',      r's'),

    # ── NUMBERS ────────────────────
    # Float MUST come before Integer!
    ('FLOAT',       r'\d+\.\d+'),
    ('INTEGER',     r'\d+'),

    # ── IDENTIFIER ─────────────────
    # NAME must come AFTER all units!
    ('NAME',        r'[a-zA-Z_][a-zA-Z0-9_]*'),

    # ── OPERATORS ──────────────────
    ('ARROW',       r'->'),
    ('PLUS_MINUS',  r'\+-'),
    ('GTE',         r'>='),
    ('LTE',         r'<='),
    ('EQEQ',        r'=='),
    ('GT',          r'>'),
    ('LT',          r'<'),
    ('EQUALS',      r'='),
    ('PLUS',        r'\+'),
    ('MINUS',       r'-'),
    ('MULTIPLY',    r'\*'),
    ('DIVIDE',      r'/'),

    # ── DELIMITERS ─────────────────
    ('COLON',       r':'),
    ('COMMA',       r','),
    ('LPAREN',      r'\('),
    ('RPAREN',      r'\)'),
    ('LBRACKET',    r'\['),
    ('RBRACKET',    r'\]'),
    ('DOT',         r'\.'),

    # ── SKIP THESE ─────────────────
    ('NEWLINE',     r'\n'),
    ('SKIP',        r'[ \t]+'),
    ('COMMENT',     r'#[^\n]*'),
]


# ── Token Class ───────────────────
class Token:
    """
    Represents one piece of
    PowerLang source code.

    Example:
      48V → TWO tokens:
      Token(INTEGER, '48', line 3)
      Token(UNIT_V,  'V',  line 3)
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
    Raised when PowerLang finds
    a character it cannot recognise
    """
    def __init__(self, char, line):
        self.char = char
        self.line = line
        super().__init__(
            f"\n  LEXER ERROR on line {line}:\n"
            f"  Unknown character: '{char}'\n"
            f"  Check your PowerLang syntax!"
        )


# ── Lexer Class ───────────────────
class Lexer:
    """
    Step 1 of PowerLang compilation.

    Takes raw source code text.
    Returns list of Token objects.

    This is the HEARTBEAT of
    the PowerLang compiler.
    """

    def __init__(self, source_code):
        self.source = source_code
        self.tokens = []
        self.line   = 1

    def tokenize(self):
        """
        Read source code character
        by character.
        Match against token patterns.
        Build and return token list.
        """
        pos = 0

        while pos < len(self.source):
            match = None

            # Try every token pattern
            # in order of priority
            for token_type, pattern in TOKEN_TYPES:
                regex = re.compile(pattern)
                match = regex.match(
                    self.source, pos
                )

                if match:
                    value = match.group(0)

                    # Count lines for errors
                    if token_type == 'NEWLINE':
                        self.line += 1

                    # Skip whitespace & comments
                    elif token_type in (
                        'SKIP', 'COMMENT'
                    ):
                        pass

                    # Keep all real tokens
                    else:
                        self.tokens.append(
                            Token(
                                token_type,
                                value,
                                self.line
                            )
                        )

                    pos = match.end()
                    break

            # No pattern matched
            if not match:
                raise LexerError(
                    self.source[pos],
                    self.line
                )

        return self.tokens


# ════════════════════════════════════
# TEST — First PowerLang Program
# A complete buck converter system
# ════════════════════════════════════

source_code = """
# PowerLang Example 1
# Buck Converter 48V to 12V

converter buck:
    input:  48V
    output: 12V
    switch: 100kHz

control pid:
    Kp: 0.5
    Ki: 0.1
    Kd: 0.05
    setpoint: 12V
    feedback: ADC_channel_1

protect:
    overvoltage:    14V
    undervoltage:   10V
    overcurrent:    12A
    overtemperature: 85
"""

# ── Run The Lexer ─────────────────
print()
print("=" * 50)
print("  PowerLang Compiler v0.1")
print("  Author: venjiii")
print("  Tokenizing buck converter...")
print("=" * 50)
print()

try:
    lexer  = Lexer(source_code)
    tokens = lexer.tokenize()

    # Print every token
    for i, token in enumerate(tokens, 1):
        print(f"[{i:2}] {token}")

    print()
    print("=" * 50)
    print(f"  SUCCESS!")
    print(f"  Total tokens: {len(tokens)}")
    print(f"  PowerLang is ALIVE!")
    print("=" * 50)
    print()

except LexerError as e:
    print(e)

except Exception as e:
    print(f"  Unexpected error: {e}")
