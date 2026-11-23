"""Тесты ассемблера на примерах из спецификации УВМ."""

import os
import sys
import unittest

TESTS_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(TESTS_DIR, "..", "src"))

import assembler


class TestAssembler(unittest.TestCase):
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

    def test_spec_program(self):
        """Файл spec_test.json даёт те же поля, что и спецификация."""
        path = os.path.join(TESTS_DIR, "spec_test.json")
        program = assembler.translate_program(assembler.read_program(path))
        lines = [assembler.format_fields(fields) for fields in program]
        expected = [
            "A=14, B=106, C=723",
            "A=12, B=183, C=438, D=923",
            "A=11, B=694, C=172, D=732",
            "A=6, B=124, C=423, D=97",
        ]
        self.assertEqual(lines, expected)


if __name__ == "__main__":
    unittest.main()
