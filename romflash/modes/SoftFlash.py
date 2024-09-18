from romflash.modes.Flash import Flash
from pathlib import Path
from romflash.modes import device_mode
from sys import exit
import logging


class SoftFlash(Flash):
    def __init__(self, rom_zip: Path):
        super().__init__(rom_zip, rom_zip.with_suffix(""))

    def flashFull(self, interactive=True, format=True):
        super().flashFull(interactive)

        logging.info("Rebooting to bootloader...")
        mode: int = self.getDeviceMode()
        match mode:
            case device_mode.BOOTLOADER:
                logging.debug("Already in bootloader")
            case device_mode.SYSTEM:
                self.run("adb reboot bootloader")
            case device_mode.FASTBOOT:
                self.run("fastboot reboot bootloader")
            case _:
                logging.error(f"Device mode {mode} unknown, unable to proceed.")
                exit(1)

        if format:
            logging.info("Formatting device...")
            self.run("fastboot -w")

        logging.info("Flashing rom update and then rebooting to fastboot to finish...")
        self.run(f"fastboot update {self.rom_zip}")
        logging.debug("Flashing rom update complete.")

        mode = self.getDeviceMode()
        if not mode == device_mode.FASTBOOT:
            logging.error(f"Device is not in fastboot, {mode=}.")
            if interactive and not self.ynprompt(
                "Something fatal has likely accurd. Would you like to continue?", False
            ):
                exit(1)

        logging.info("Flashing final rom images...")
        self.flash("product.img")
        self.flash("system.img")
        self.flash("vendor.img")

        logging.info(
            "Flashing complete! Make sure to check the output or log for potential errors."
        )
        if interactive and self.ynprompt("Reboot to system?", True):
            logging.info("Rebooting to system...")
            self.run("fastboot reboot")
