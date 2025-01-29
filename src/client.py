import socket
import threading
from textual.app import App, ComposeResult
from textual.containers import Vertical, Horizontal
from textual.widgets import Header, Footer, TextArea, Input, Button, Static


class CheatChatClient(App):
    """The Cheat chat client built using the textual framework"""

    CSS_PATH = ""

    def __init__(self):
        super().__init__()
        self.client: socket.socket | None = None
        self.username = ""

    def on_mount(self):
        """Show the login screen on mount"""
        self.push_screen("login", LoginScreen())

    def connect_to_server(self, host: str, port: int, username: str):
        """Try to connect to the server and, if it succeds, show the chat"""
        try:
            self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client.connect((host, port))
            self.username = username
            self.switch_to_chat()
            threading.Thread(target=self.recive_message, daemon=True).start()
        except (socket.error, ValueError):
            self.show_error("❌ Connection error, check the data and try again.")

    def switch_to_chat(self):
        """Passa alla schermata della chat"""
        self.pop_screen()
        self.push_screen("chat", ChatScreen())

    def recive_message(self):
        """Recive the messages from the server and update the chat"""
        if not self.client:
            self.show_error("❌ Connection error, check the data and try again.")
            return

        chat_box = self.query_one("#chat_box", TextArea)
        while True:
            try:
                message = self.client.recv(1024).decode()
                if message == "INSERT USERNAME":
                    self.client.send(self.username.encode())
                else:
                    self.call_from_thread(self.display_message, message)
            except (ConnectionAbortedError, OSError):
                self.show_error("❌ Connection error, check the data and try again.")
                break

    def display_message(self, message: str):
        """Display a message in the chat box"""
        chat_box = self.query_one("#chat_box", TextArea)
        chat_box.insert(f"{message}\n", chat_box.document.end)

    # def write(self, client: socket.socket):
    #     while True:
    #         try:
    #             message = f"[{username}]$ {input('')}"
    #             client.send(message.encode())
    #         except ConnectionAbortedError as e:
    #             print(f"❌ Connection aborted: {e}")
    #             client.close()
    #             break
    #         except OSError as e:
    #             print(f"❌ An error occurred while sending a message: {e}")
    #             client.close()
    #             break

    def on_button_pressed(self, event: Button.Pressed):
        """Handle the button pressed event"""
        if event.button.id == "connect_button":
            self.handle_login()
        elif event.button.id == "send_button":
            self.send_message()

    def on_input_submitted(self, event: Input.Submitted):
        """Handle the input submitted event"""
        if event.input.id == "input_field":
            self.send_message()

    def handle_login(self):
        """Retrives the user's input and tries to connect"""
        host = self.query_one("#host_input", Input).value.strip()
        port_input = self.query_one("#port_input", Input).value.strip()
        username = self.query_one("#username_input", Input).value.strip()

        if not host or not port_input or not username:
            self.show_error("❌ All fields are required.")
            return

        try:
            port = int(port_input)
            self.connect_to_server(host, port, username)
        except ValueError:
            self.show_error("❌ The port must be a number.")

    def show_error(self, message: str):
        """Show an error message in the login screen"""
        error_label = self.query_one("#error_label", Static)
        error_label.update(message)

    def send_message(self):
        """Invia un messaggio al server"""
        input_field = self.query_one("#input_field", Input)
        message = input_field.value.strip()

        if message:
            full_message = f"[{self.username}]$ {message}"

            if self.client:
                self.client.send(full_message.encode())
                self.display_message(full_message)
                input_field.clear()


if __name__ == "__main__":
    app = CheatChatClient()
    app.run()
