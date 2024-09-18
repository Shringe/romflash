from pathlib import Path
from abc import ABC, abstractmethod
from zipfile import ZipFile
from romflash.__main__ import log_args
from romflash.modes import device_mode
import shutil
import logging
import subprocess
from typing import List, Iterable, Any, Optional


class Flash(ABC):
    def __init__(self, rom_zip: Path, working_directory: Path) -> None:
        self.working_directory: Path = working_directory
        self.rom_zip: Path = rom_zip

        self.extracted_directory: Path = working_directory / rom_zip.with_suffix("")

    @abstractmethod
    def verifyFilePaths(self, *paths_to_verify: Path) -> bool:
        """
        Logs the state of all paths_to_verify, and returns True if all paths are found.
        """
        all_exist: bool = True
        for path in paths_to_verify:
            exists: bool = path.exists()
            if exists:
                logging.info(f"{path} found.")
            else:
                logging.warning(f"{path} is not found.")
                all_exist = False

        return all_exist

    def isBootloaderUnlocked(self) -> Optional[bool]:
        """
        Returns none if unable to determine locked status.
        """
        if self.isFastBootAvailable():
            return (
                "securestate: flashing_unlocked"
                in self.run("fastboot getvar securestate").stdout
            )

        logging.error("Fastboot not available to chech device bootloader status.")
        return None

    def isAdbAvailable(self) -> bool:
        available: bool = "device" in self.run("adb devices").stdout

        logging.debug(f"adb status {available=}")
        return available

    def isFastBootAvailable(self) -> bool:
        available: bool = "device" in self.run("fastboot devices").stdout

        logging.debug(f"fastboot status {available=}")
        return available

    @abstractmethod
    def getDeviceMode(self) -> int:
        """
        Returns a device_mode for the current boot state of the connected device.
        """
        if self.isAdbAvailable():
            return device_mode.SYSTEM
        elif self.isFastBootAvailable():
            if "is-userspace: yes" in self.run("fastboot getvar is-userspace").stdout:
                return device_mode.FASTBOOT
            else:
                return device_mode.BOOTLOADER
        else:
            logging.warning("Device is in unknown boot mode.")
            return device_mode.UNKNOWN

    @log_args
    @abstractmethod
    def flashFull(self, interactive: bool):
        """
        Fully flashes rom.
        """
        self.verifyFilePaths(self.rom_zip, self.working_directory)

        self.createWorkingDir()
        self.extractZip()

        self.verifyFilePaths(self.extracted_directory)

    @abstractmethod
    def createWorkingDir(self):
        """
        Creates empty self.working_directory. Clears contents of directory instead if already present.
        """
        if self.working_directory.is_dir():
            logging.debug(f"{self.working_directory} already found, removing.")
            shutil.rmtree(self.working_directory)

        logging.debug(f"Creating {self.working_directory}")
        self.working_directory.mkdir()

    @abstractmethod
    def extractZip(self):
        """
        Extracts self.rom_zip to self.working_directory
        """
        logging.info(f"Extracting {self.rom_zip}")
        with ZipFile(self.rom_zip, "r") as zip:
            zip.extractall(self.extracted_directory)

    @log_args
    @abstractmethod
    def run(
        self, cmd: str, shell=True, text=True, check=True
    ) -> subprocess.CompletedProcess[Any]:
        """
        Runs and logs process with default parameters. Returns output
        """
        cmd = "Just example"
        return subprocess.run(
            cmd,
            shell=shell,
            text=text,
            check=check,
            cwd=self.working_directory,
        )

    @abstractmethod
    def flash(
        self,
        img: Path | str,
        android: Optional[Path] = None,
        img_dir: Optional[Path] = None,
    ) -> subprocess.CompletedProcess[Any]:
        """
        Calls self.run(f"fastboot flash {android} {img}", working_directory=img_dir).
        """
        img = Path(img)
        if not android:
            android = img.with_suffix("")
        if not img_dir:
            img_dir = self.extracted_directory

        return self.run(f"fastboot flash {android} {img}", working_directory=img_dir)

    @staticmethod
    def ynprompt(msg: str, default_answer=False, skip=False) -> bool:
        if skip:
            return default_answer

        suffix: str
        if default_answer:
            suffix = "[Y/n]: "
        else:
            suffix = "[y/N]: "

        response: str = input(msg + suffix).strip().lower()
        return response == "y"
