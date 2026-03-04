# ================================
# PowerLang Compiler v0.1
# main.py - Entry Point
# ================================

import sys
import os

# Add src folder to path
sys.path.insert(0, os.path.dirname(__file__))

from lexer import Lexer, LexerError

# ── Test PowerLang Program ────────
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
    overvoltage:     14V
    undervoltage:    10V
    overcurrent:     12A
    overtemperature: 85
"""

# ── Run ───────────────────────────
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

    for i, token in enumerate(tokens, 1):
        print(f"[{i:2}] {token}")

    print()
    print("=" * 50)
    print(f"  SUCCESS!")
    print(f"  Total tokens: {len(tokens)}")
    print(f"  Lexer complete!")
    print(f"  PowerLang is ALIVE!")
    print("=" * 50)
    print()

except LexerError as e:
    print(e)