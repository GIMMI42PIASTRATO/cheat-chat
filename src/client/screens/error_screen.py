from textual.screen import ModalScreen
from textual.widgets import Static, Button
from textual.containers import Center


class ErrorScreen(ModalScreen):
    """A modal screen to display errors"""

    def __init__(self, message: str):
        super().__init__()
        self.message = message

    def compose(self):
        yield Center(Static(self.message, id="error_message"))
        yield Center(Button("Ok", id="error_ok"))

    def on_button_pressed(self, event: Button.Pressed):
        """Handle the button pressed event"""
        self.app.pop_screen()
