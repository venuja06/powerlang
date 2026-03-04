# ================================
# PowerLang Compiler v0.1
# tokens.py - All Token Definitions
# ================================

# ORDER MATTERS!
# Units MUST come before NAME!

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

    # PID PARAMETERS
    ('KP',          r'\bKp\b'),
    ('KI',          r'\bKi\b'),
    ('KD',          r'\bKd\b'),

    # PROTECTION
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
    ('ESP32',       r'\bESP32\b'),
    ('ARDUINO',     r'\bArduino\b'),

    # ── UNITS ──────────────────────
    # Frequency
    ('UNIT_MHZ',    r'MHz'),
    ('UNIT_KHZ',    r'kHz'),
    ('UNIT_HZ',     r'Hz'),

    # Power
    ('UNIT_MW',     r'MW'),
    ('UNIT_KW',     r'kW'),
    ('UNIT_W',      r'W(?![a-zA-Z_])'),

    # Voltage
    ('UNIT_MV',     r'mV'),
    ('UNIT_KV',     r'kV'),
    ('UNIT_V',      r'V(?![a-zA-Z_])'),

    # Current
    ('UNIT_MA',     r'mA'),
    ('UNIT_A',      r'A(?![a-zA-Z_])'),

    # Inductance
    ('UNIT_UH',     r'uH'),
    ('UNIT_MH',     r'mH'),

    # Capacitance
    ('UNIT_UF',     r'uF'),
    ('UNIT_NF',     r'nF'),

    # Other
    ('UNIT_PERCENT', r'%'),
    ('UNIT_OHM',    r'Ohm'),

    # Time
    ('UNIT_MS',     r'ms'),
    ('UNIT_US',     r'us'),
    ('UNIT_NS',     r'ns'),
    ('UNIT_S',      r's(?![a-zA-Z_])'),

    # ── NUMBERS ────────────────────
    # Float BEFORE Integer!
    ('FLOAT',       r'\d+\.\d+'),
    ('INTEGER',     r'\d+'),

    # ── NAME ───────────────────────
    # MUST be after all units!
    ('NAME',        r'[a-zA-Z_][a-zA-Z0-9_]*'),

    # ── OPERATORS ──────────────────
    ('ARROW',       r'->'),
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

    # ── SKIP ───────────────────────
    ('NEWLINE',     r'\n'),
    ('SKIP',        r'[ \t]+'),
    ('COMMENT',     r'#[^\n]*'),
]