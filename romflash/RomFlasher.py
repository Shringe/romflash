from abc import ABC, abstractmethod


class RomFlasher(ABC):
    """
    Organizes and verifies the flashing process. This class is to be extended with flashers with the appropiate methods overidden for their devices.
    """

    @abstractmethod
    def format_device(self):
        """
        Wipes and formats data on device.
        """
        raise NotImplementedError(
            "The flasher for your device does not support this option."
        )

    @abstractmethod
    def flash_full_rom(self):
        """
        Executes the entire rom flashing process for this device.
        """
        raise NotImplementedError(
            "The flasher for your device does not support this option."
        )

    @abstractmethod
    def flash_updatepackage(self):
        """
        Flash update package to this device.
        """
        raise NotImplementedError(
            "The flasher for your device does not support this option."
        )

    @abstractmethod
    def flash_a10(self):
        """
        Flash A10 firmware to this device.
        """
        raise NotImplementedError(
            "The flasher for your device does not support this option."
        )

    @abstractmethod
    def flash_a11(self):
        """
        Flash A11 firmware to this device.
        """
        raise NotImplementedError(
            "The flasher for your device does not support this option."
        )

    @abstractmethod
    def flash_a12(self):
        """
        Flash A12 firmware to this device.
        """
        raise NotImplementedError(
            "The flasher for your device does not support this option."
        )

    @abstractmethod
    def flash_a13(self):
        """
        Flash A13 firmware to this device.
        """
        raise NotImplementedError(
            "The flasher for your device does not support this option."
        )

    @abstractmethod
    def flash_a14(self):
        """
        Flash A14 firmware to this device.
        """
        raise NotImplementedError(
            "The flasher for your device does not support this option."
        )
