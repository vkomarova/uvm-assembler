"""Тесты ассемблера на примерах из спецификации УВМ."""

import os
import sys
import unittest

TESTS_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(TESTS_DIR, "..", "src"))

import assembler


class TestTranslate(unittest.TestCase):
    """Проверка перевода команд во внутреннее представление."""

    def test_load(self):
        """Загрузка константы: A=14, B=106, C=723."""
        command = {"command": "load", "address": 106, "value": 723}
        expected = {"A": 14, "B": 106, "C": 723}
        self.assertEqual(assembler.translate_command(command), expected)

    def test_read(self):
        """Чтение из памяти: A=12, B=183, C=438, D=923."""
        command = {"command": "read", "base": 183, "offset": 438,
                   "dest": 923}
        expected = {"A": 12, "B": 183, "C": 438, "D": 923}
        self.assertEqual(assembler.translate_command(command), expected)

    def test_write(self):
        """Запись в память: A=11, B=694, C=172, D=732."""
        command = {"command": "write", "offset": 694, "base": 172,
                   "src": 732}
        expected = {"A": 11, "B": 694, "C": 172, "D": 732}
        self.assertEqual(assembler.translate_command(command), expected)

    def test_neg(self):
        """Унарный минус: A=6, B=124, C=423, D=97."""
        command = {"command": "neg", "offset": 124, "base": 423,
                   "src": 97}
        expected = {"A": 6, "B": 124, "C": 423, "D": 97}
        self.assertEqual(assembler.translate_command(command), expected)


class TestEncode(unittest.TestCase):
    """Проверка перевода команд в машинный код."""

    def test_load(self):
        """Загрузка константы даёт байты из спецификации."""
        fields = {"A": 14, "B": 106, "C": 723}
        expected = bytes([0xAE, 0x06, 0x00, 0x00, 0x4C, 0x0B, 0x00])
        self.assertEqual(assembler.encode_command(fields), expected)

    def test_read(self):
        """Чтение из памяти даёт байты из спецификации."""
        fields = {"A": 12, "B": 183, "C": 438, "D": 923}
        expected = bytes([0x7C, 0x0B, 0x00, 0x00, 0xD8,
                          0xC6, 0xE6, 0x00, 0x00, 0x00])
        self.assertEqual(assembler.encode_command(fields), expected)

    def test_write(self):
        """Запись в память даёт байты из спецификации."""
        fields = {"A": 11, "B": 694, "C": 172, "D": 732}
        expected = bytes([0x6B, 0x2B, 0xAC, 0x00, 0x00,
                          0x00, 0xB7, 0x00, 0x00, 0x00])
        self.assertEqual(assembler.encode_command(fields), expected)

    def test_neg(self):
        """Унарный минус даёт байты из спецификации."""
        fields = {"A": 6, "B": 124, "C": 423, "D": 97}
        expected = bytes([0xC6, 0x07, 0xA7, 0x01, 0x00,
                          0x40, 0x18, 0x00, 0x00, 0x00])
        self.assertEqual(assembler.encode_command(fields), expected)

    def test_spec_program(self):
        """Файл spec_test.json даёт все байты из спецификации."""
        path = os.path.join(TESTS_DIR, "spec_test.json")
        program = assembler.translate_program(assembler.read_program(path))
        lines = [assembler.format_bytes(code)
                 for code in assembler.assemble(program)]
        expected = [
            "0xAE, 0x06, 0x00, 0x00, 0x4C, 0x0B, 0x00",
            "0x7C, 0x0B, 0x00, 0x00, 0xD8, 0xC6, 0xE6, 0x00, 0x00, 0x00",
            "0x6B, 0x2B, 0xAC, 0x00, 0x00, 0x00, 0xB7, 0x00, 0x00, 0x00",
            "0xC6, 0x07, 0xA7, 0x01, 0x00, 0x40, 0x18, 0x00, 0x00, 0x00",
        ]
        self.assertEqual(lines, expected)


if __name__ == "__main__":
    unittest.main()
