#! /usr/bin/env python3

from argparse import ArgumentParser, Namespace


class USGBAFixer():
    def __init__(self) -> None:
        # Original bugged bytes at 0x0E4536-0x0E453F
        self.__expected_bytes: dict[int, int] = {
            0x0E4536: 0x08,
            0x0E4537: 0x40,
            0x0E4538: 0x00,
            0x0E4539: 0x28,
            0x0E453A: 0x01,
            0x0E453B: 0xD0,
            0x0E453C: 0xE0,
            0x0E453D: 0x1C,
            0x0E453E: 0x18,
            0x0E453F: 0x80
        }

        # Fixed bytes to be written at 0x0E4536-0x0E453F
        self.__fixed_bytes: dict[int, int] = {
            0x0E4536: 0x00,
            0x0E4537: 0x19,
            0x0E4538: 0x80,
            0x0E4539: 0x1C,
            0x0E453A: 0x18,
            0x0E453B: 0x80,
            0x0E453C: 0xC0,
            0x0E453D: 0x46,
            0x0E453E: 0xC0,
            0x0E453F: 0x46
        }

        self.__minimum_rom_size: int = 0x0E4540

    def __parse_args(self) -> None:
        parser: ArgumentParser = ArgumentParser(description="Fix for the FFV agility bug in US GBA ROMs")

        parser.add_argument("-i", "--input", help="Path to the input GBA ROM")
        parser.add_argument("-o", "--output", help="Path to the output fixed GBA ROM")

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
    fixer: USGBAFixer = USGBAFixer()

    fixer.run()
