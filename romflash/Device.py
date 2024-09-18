from logger import Logger
from pathlib import Path
from enum import Enum
from typing import Optional
from romflash import FileHandler
import subprocess


class DeviceMode(Enum):
    UNKNOWN = -1
    SYSTEM = 0
    BOOTLOADER = 1
    FASTBOOT = 2


class Device:
    """
    Interacts with core utilities such as adb and fastboot.
    """

    def __init__(self, filehandler: FileHandler, logger: Logger):
        self.logger: Logger = logger
        self.filehandler: FileHandler = filehandler

    def is_unlocked(self) -> bool | None:
        """
        Returns none if unable to determine booloader status.
        """
        if self.is_fastboot_available():
            return "securestate: flashing_unlocked" in self.fastboot(
                "getvar securestate"
            )

        self.logger.error("Fastboot not available to chech device bootloader status.")
        return None

    def is_adb_available(self) -> bool:
        """Check if ADB (Android Debug Bridge) is available."""
        available: bool = "device" in self.adb("devices")[0]

        self.logger.debug(f"adb status {available=}")
        return available

    def is_fastboot_available(self) -> bool:
        """Check if Fastboot is available."""
        available: bool = "device" in self.fastboot("devices")[0]

        self.logger.debug(f"fastboot status {available=}")
        return available

    def get_boot_mode(self) -> DeviceMode:
        """Get the current boot mode of the device."""
        if self.is_adb_available():
            return DeviceMode.SYSTEM
        elif self.is_fastboot_available():
            if "is-userspace: yes" in self.fastboot("getvar is-userspace"):
                return DeviceMode.FASTBOOT
            else:
                return DeviceMode.BOOTLOADER
        else:
            self.logger.warning("Device is in unknown boot mode.")
            return DeviceMode.UNKNOWN

    def flash_file(
        self,
        img: Path | str,
        img_dir: Optional[Path] = None,
        android: Optional[str] = None,
    ) -> None:
        """Flash a file to the connected device."""
        if isinstance(img, str):
            img = Path(img)

        if not android:
            android = img.stem
        if not img_dir:
            img_dir = self.filehandler.working_directory

        return self.fastboot(f"flash {android} {img}")

    def adb(self, cmd: str) -> tuple[str, str]:
        """Execute ADB commands."""
        return self._run_cmd("adb " + cmd)

    def fastboot(self, cmd: str) -> tuple[str, str]:
        """Execute Fastboot commands."""
        return self._run_cmd("fastboot " + cmd)

    def _run_cmd(self, cmd: str) -> tuple[str, str]:
        try:
            result = subprocess.run(
                cmd,
                stdout=subprocess.PIPE,  # Capture standard output
                stderr=subprocess.PIPE,  # Capture standard error
                text=True,  # Return output as string (text mode)
                check=True,  # Raise an error if the command fails
                shell=True,
            )

            return result.stdout, result.stderr
        except subprocess.CalledProcessError as e:
            # Handle errors in command execution
            self.logger.error(f"Command '{e.cmd}' failed with exit code {e.returncode}")
            self.logger.error(f"Error output: {e.stderr}")
            exit(e.cmd)
