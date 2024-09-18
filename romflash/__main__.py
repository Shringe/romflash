import typer
from pathlib import Path


app = typer.Typer(no_args_is_help=True)


@app.command()
def start_tui():
    """
    Main entry point for the TUI.
    """
    raise NotImplementedError()


@app.command()
def start_flash(
    flasher: Path,
    device: Path,
    filehandler: Path,
):
    """
    Starts main flashing process
    """
    print(
        f"""
          {flasher=}
          {device=}
          {filehandler=}"""
    )


if __name__ == "__main__":
    app()
