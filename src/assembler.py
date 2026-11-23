import argparse
import json

LOAD_CONST_CODE = 14
READ_MEM_CODE = 12
WRITE_MEM_CODE = 11
NEG_CODE = 6


def translate_command(command):
    """Переводит одну команду JSON в словарь с полями УВМ"""
    name = command["command"]
    if name == "load":
        return {
            "A": LOAD_CONST_CODE,
            "B": command["address"],
            "C": command["value"],
        }
    if name == "read":
        return {
            "A": READ_MEM_CODE,
            "B": command["base"],
            "C": command["offset"],
            "D": command["dest"],
        }
    if name == "write":
        return {
            "A": WRITE_MEM_CODE,
            "B": command["offset"],
            "C": command["base"],
            "D": command["src"],
        }
    if name == "neg":
        return {
            "A": NEG_CODE,
            "B": command["offset"],
            "C": command["base"],
            "D": command["src"],
        }
    raise ValueError("Неизвестная команда: " + name)


def translate_program(commands):
    """Переводит список команд JSON во внутреннее представление"""
    result = []
    for command in commands:
        result.append(translate_command(command))
    return result


def read_program(path):
    """Читает файл с программой на языке ассемблера (JSON)"""
    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)


def format_fields(fields):
    """Возвращает строку вида 'A=14, B=106, C=723'"""
    parts = []
    for name, value in fields.items():
        parts.append(name + "=" + str(value))
    return ", ".join(parts)


def print_program(program):
    """Выводит на экран внутреннее представление программы"""
    for fields in program:
        print(format_fields(fields))


def parse_args():
    """Разбирает аргументы командной строки"""
    parser = argparse.ArgumentParser(description="Ассемблер УВМ")
    parser.add_argument("source", help="путь к файлу с программой")
    parser.add_argument("output", help="путь к двоичному файлу-результату")
    parser.add_argument(
        "--test", action="store_true", help="режим тестирования"
    )
    return parser.parse_args()


def main():
    args = parse_args()
    commands = read_program(args.source)
    program = translate_program(commands)
    if args.test:
        print_program(program)


if __name__ == "__main__":
    main()
