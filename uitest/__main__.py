# Required Python libraries
import typer
import npyscreen
from curses import initscr

initscr()

app = typer.Typer()


# CLI implementation using Click
@app.command()
# @click.option("--flasher", help="Specify the flasher to use")
# @click.option("--device", help="Specify the device to use")
def main_cli(flasher: str, device: str):
    print(f"Using Flasher: {flasher}")
    print(f"Using Device: {device}")
    # Add logic to instantiate and use the specified Flasher and Device objects


# TUI implementation using npyscreen
class FlasherDeviceForm(npyscreen.Form):
    def create(self):
        self.add(npyscreen.TitleText, name="Flasher:", value="", editable=True)
        self.add(npyscreen.TitleText, name="Device:", value="", editable=True)


@app.command()
def main_tui():
    app = npyscreen.NPSAppManaged()
    form = FlasherDeviceForm(name="Flasher and Device Selection")
    form.edit()
    flasher = form.get_widget("Flasher:").value
    device = form.get_widget("Device:").value
    # Add logic to instantiate and use the specified Flasher and Device objects
    # Display selected Flasher and Device
    npyscreen.notify_confirm(
        f"Using Flasher: {flasher}\nUsing Device: {device}",
        title="Selection Confirmation",
    )
    app.run()


if __name__ == "__main__":
    # Run either the CLI or TUI based on user input
    app()
    # if user_input == "cli":
    #     app()
    # elif user_input == "tui":
    #     main_tui()
    # else:
    #     print("Invalid choice. Please choose CLI or TUI.")
