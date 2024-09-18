from pathlib import Path
from logging import Logger
from zipfile import ZipFile
from shutil import rmtree
from typing import Optional


class FileHandler:
    def __init__(
        self,
        rom_zip: Path,
        logger: Logger,
        rom_zip_extracted: Optional[Path] = None,
        working_directory: Optional[Path] = None,
    ) -> None:
        """
        Handles files and directories of the flashing process.
        """
        self.rom_zip = rom_zip
        self.logger = logger

        if not working_directory:
            self.working_directory = self.rom_zip.with_suffix("")
        else:
            self.working_directory = working_directory

        if not rom_zip_extracted:
            self.rom_zip_extracted = self.working_directory / "rom"
        else:
            self.rom_zip_extracted = rom_zip_extracted

        if not self.verify_paths(self.rom_zip, logger=self.logger):
            raise FileNotFoundError(f"{self.rom_zip=}, could not be found.")
            exit(1)

    def extract_rom(self) -> None:
        self.logger.info(f"Extracting {self.rom_zip} to {self.rom_zip_extracted}")

        self.verify_paths(self.rom_zip, self.working_directory, logger=self.logger)
        self.extract_zip(self.rom_zip, self.rom_zip_extracted)
        self.verify_paths(
            self.rom_zip,
            self.working_directory,
            self.rom_zip_extracted,
            logger=self.logger,
        )

    def prepare_working_directory(self) -> None:
        """
        Clears self.working_directory if exists, then extracts rom into self.rom_zip_extracted.
        """
        self.logger.info(f"Clearing {self.working_directory=}")
        rmtree(self.working_directory)

        self.logger.info(f"Creating {self.working_directory=}")
        self.working_directory.mkdir()
        self.verify_paths(self.working_directory)

    @staticmethod
    def verify_paths(*paths_to_verify: Path, logger: Optional[Logger] = None) -> bool:
        """
        Logs the state of all paths_to_verify, and returns True if all paths are found.
        """
        all_exist: bool = True
        for path in paths_to_verify:
            if path.exists():
                if logger:
                    logger.info(f"{path} found.")
            else:
                if logger:
                    logger.warning(f"{path} was not found.")
                all_exist = False

        return all_exist

    @staticmethod
    def extract_zip(source_zip: Path, target_dir: Path) -> None:
        with ZipFile(source_zip, "r") as zip:
            zip.extractall(target_dir)
