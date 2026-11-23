import argparse
import json

LOAD_CONST_CODE = 14
READ_MEM_CODE = 12
WRITE_MEM_CODE = 11
NEG_CODE = 6

LOAD_CONST_SIZE = 7
LONG_COMMAND_SIZE = 10


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


def encode_command(fields):
    """Переводит одну команду (словарь полей) в байты"""
    code = fields["A"]
    if code == LOAD_CONST_CODE:
        value = code | (fields["B"] << 4) | (fields["C"] << 34)
        return value.to_bytes(LOAD_CONST_SIZE, "little")
    if code == READ_MEM_CODE:
        value = code | (fields["B"] << 4) | (fields["C"] << 34)
        value = value | (fields["D"] << 46)
        return value.to_bytes(LONG_COMMAND_SIZE, "little")
    value = code | (fields["B"] << 4) | (fields["C"] << 16)
    value = value | (fields["D"] << 46)
    return value.to_bytes(LONG_COMMAND_SIZE, "little")


def assemble(program):
    """Переводит внутреннее представление в список байтов команд"""
    result = []
    for fields in program:
        result.append(encode_command(fields))
    return result


def read_program(path):
    """Читает файл с программой на языке ассемблера (JSON)"""
    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)


def write_binary(path, codes):
    """Записывает машинный код в двоичный файл, возвращает размер"""
    data = b"".join(codes)
    with open(path, "wb") as file:
        file.write(data)
    return len(data)


def format_bytes(code):
    """Возвращает строку вида '0xAE, 0x06, 0x00'"""
    parts = []
    for byte in code:
        parts.append("0x{:02X}".format(byte))
    return ", ".join(parts)


def print_codes(codes):
    """Выводит на экран машинный код каждой команды"""
    for code in codes:
        print(format_bytes(code))


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
    codes = assemble(program)
    size = write_binary(args.output, codes)
    if args.test:
        print_codes(codes)
    print("Размер двоичного файла:", size, "байт")


if __name__ == "__main__":
    main()
