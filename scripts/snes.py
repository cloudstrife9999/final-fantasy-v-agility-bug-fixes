#! /usr/bin/env python3

from argparse import ArgumentParser, Namespace


class SNESFixer():
    def __init__(self) -> None:
        # Original bugged bytes at 0x28113-0x28116
        self.__expected_bytes: dict[int, int] = {
            0x28113: 0xA5,
            0x28114: 0x26,
            0x28115: 0xC2,
            0x28116: 0x20
        }

        # Fixed bytes to be written at 0x28113-0x28116
        self.__fixed_bytes: dict[int, int] = {
            0x28113: 0xC2,
            0x28114: 0x20,
            0x28115: 0xA5,
            0x28116: 0x26
        }

        self.__minimum_rom_size: int = 0x28117

    def __parse_args(self) -> None:
        parser: ArgumentParser = ArgumentParser(description="Fix for the FFV agility bug in SNES ROMs")

        parser.add_argument("-i", "--input", help="Path to the input SNES ROM")
        parser.add_argument("-o", "--output", help="Path to the output fixed SNES ROM")

        args: Namespace = parser.parse_args()

        self.__input_file_path: str = args.input
        self.__output_file_path: str = args.output

    def __load_rom(self) -> None:
        with open(self.__input_file_path, "rb") as f:
            self.__rom_data: bytes = bytes(f.read())

    def __input_bytes_check(self) -> bool:
        if len(self.__rom_data) < self.__minimum_rom_size:
            print("Error: ROM file is too small to contain the expected bytes.")

            return False

        for address, expected_byte in self.__expected_bytes.items():
            if self.__rom_data[address] != expected_byte:
                print(f"Error: Byte at address {hex(address)} is {hex(self.__rom_data[address])}, expected {hex(expected_byte)}.")

                return False
        return True

    def __fix_rom(self) -> None:
        self.__fixed_rom_data: bytearray = bytearray(self.__rom_data)

        for address, fixed_byte in self.__fixed_bytes.items():
            self.__fixed_rom_data[address] = fixed_byte

    def __save_fixed_rom(self) -> None:
        with open(self.__output_file_path, "wb") as f:
            f.write(self.__fixed_rom_data)

    def run(self) -> None:
        self.__parse_args()
        self.__load_rom()

        if not self.__input_bytes_check():
            return

        self.__fix_rom()
        self.__save_fixed_rom()


if __name__ == "__main__":
    fixer: SNESFixer = SNESFixer()

    fixer.run()
