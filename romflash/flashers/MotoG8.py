from romflash.RomFlasher import RomFlasher
from romflash.FileHandler import FileHandler
from romflash.Device import Device


class MotoG8(RomFlasher):
    def __init__(self, filehandler: FileHandler, device: Device):
        self.filehandler = filehandler
        self.device = device

    def flash_a10(self):
        pass

    def flash_a11(self):
        pass

    def flash_updatepackage(self):
        pass

    def flash_full_rom(self):
        pass
