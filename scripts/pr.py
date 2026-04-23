#! /usr/bin/env python3

from argparse import ArgumentParser, Namespace
from pathlib import Path


class PRFixer():
    def __init__(self) -> None:
        # Original bugged bytes at 0xAC105F-0xAC106E
        self.__expected_bytes: dict[int, int] = {
            0xAC105F: 0x25,
            0xAC1060: 0xFF,
            0xAC1061: 0x00,
            0xAC1062: 0x00,
            0xAC1063: 0x80,
            0xAC1064: 0x7D,
            0xAC1065: 0x09,
            0xAC1066: 0xFF,
            0xAC1067: 0xC8,
            0xAC1068: 0x0D,
            0xAC1069: 0x00,
            0xAC106A: 0xFF,
            0xAC106B: 0xFF,
            0xAC106C: 0xFF,
            0xAC106D: 0xFF,
            0xAC106E: 0xC0
        }

        # Fixed bytes to be written at 0xAC105F-0xAC106E
        self.__fixed_bytes: dict[int, int] = {
            0xAC105F: 0x90,
            0xAC1060: 0x90,
            0xAC1061: 0x90,
            0xAC1062: 0x90,
            0xAC1063: 0x90,
            0xAC1064: 0x90,
            0xAC1065: 0x90,
            0xAC1066: 0x90,
            0xAC1067: 0x90,
            0xAC1068: 0x90,
            0xAC1069: 0x90,
            0xAC106A: 0x90,
            0xAC106B: 0x90,
            0xAC106C: 0x90,
            0xAC106D: 0x90,
            0xAC106E: 0x90
        }

        self.__minimum_dll_size: int = 0xAC106F

    def __parse_args(self) -> None:
        parser: ArgumentParser = ArgumentParser(description="Fix for the FFV agility bug in the Pixel Remaster PC release")

        parser.add_argument("-i", "--input", help="Path to GameAssembly.dll")

        args: Namespace = parser.parse_args()

        self.__dll_path: Path = Path(args.input)
        self.__backup_path: Path = self.__dll_path.with_name(f"{self.__dll_path.stem}_original.dll")

    def __load_dll(self) -> None:
        with open(self.__dll_path, "rb") as f:
            self.__dll_data: bytes = bytes(f.read())

    def __input_bytes_check(self) -> bool:
        if len(self.__dll_data) < self.__minimum_dll_size:
            print("Error: DLL file is too small to contain the expected bytes.")

            return False

        for address, expected_byte in self.__expected_bytes.items():
            if self.__dll_data[address] != expected_byte:
                print(f"Error: Byte at offset {hex(address)} is {hex(self.__dll_data[address])}, expected {hex(expected_byte)}")

                return False
        return True

    def __fix_dll(self) -> None:
        self.__fixed_dll_data: bytearray = bytearray(self.__dll_data)

        for address, fixed_byte in self.__fixed_bytes.items():
            self.__fixed_dll_data[address] = fixed_byte

    def __save_fixed_dll(self) -> None:
        if self.__backup_original_dll():
            self.__write_fixed_dll()

    def __backup_original_dll(self) -> bool:
        try:
            if self.__backup_path.exists():
                print(f"Error: Backup file {self.__backup_path} already exists. Please remove or rename it before running this script.")

                return False
            else:
                self.__dll_path.rename(self.__backup_path)

                return True
        except OSError as e:
            print(f"Error: Could not rename {self.__dll_path} to {self.__backup_path}: {e}")

            return False

    def __write_fixed_dll(self) -> None:
        try:
            with open(self.__dll_path, "wb") as f:
                f.write(self.__fixed_dll_data)
        except OSError as e:
            print(f"Error: Could not write patched DLL to {self.__dll_path}: {e}")
            print("Restoring original...")

            self.__restore_original_dll()

    def __restore_original_dll(self) -> None:
        try:
            self.__backup_path.rename(self.__dll_path)

            print("Original restored successfully.")
        except OSError as restore_error:
            print(f"Error: Could not restore original: {restore_error}")
            print(f"The original DLL is still available at {self.__backup_path}.")

    def run(self) -> None:
        self.__parse_args()
        self.__load_dll()

        if not self.__input_bytes_check():
            return

        self.__fix_dll()
        self.__save_fixed_dll()


if __name__ == "__main__":
    fixer: PRFixer = PRFixer()

    fixer.run()
