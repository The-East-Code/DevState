import flet as ft
import platform
import webbrowser
import logging
from logging.handlers import RotatingFileHandler

def setup_logging():
    # Configure logging
    logger = logging.getLogger("UpdateCheckerApp")
    logger.setLevel(logging.DEBUG)
    # Create a formatter and add it to the handler
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    # Rotating file handlers
    history_handler = RotatingFileHandler("update_history.log", maxBytes=1024 * 1024, backupCount=5)
    history_handler.setLevel(logging.INFO)
    history_handler.setFormatter(formatter)
    error_handler = RotatingFileHandler("error_log.log", maxBytes=1024 * 1024, backupCount=5)
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(formatter)
    # Add handlers to the logger
    logger.addHandler(history_handler)
    logger.addHandler(error_handler)
    return logger

def main(page: ft.Page):
    logger = setup_logging()

    page.title = "Update Checker"
    page.theme = ft.Theme(color_scheme=ft.ColorScheme())

    # Display system information
    system_info_text = f"System: {platform.system()}\n" \
                       f"Node Name: {platform.node()}\n" \
                       f"Release: {platform.release()}\n" \
                       f"Version: {platform.version()}\n" \
                       f"Machine: {platform.machine()}\n" \
                       f"Processor: {platform.processor()}"
    
    system_info_container = ft.Container(
        content=ft.Text(system_info_text, style=ft.TextStyle(color=ft.colors.BLACK)),
        width=400,
        padding=10,
        bgcolor=ft.colors.WHITE
    )
    page.add(system_info_container)

    # Function to handle update checks
    def check_system_updates(e):
        logger.info("Checking for system updates...")
        if platform.system() == "Windows":
            webbrowser.open("https://support.microsoft.com/en-us/windows/update")
            logger.info("Directed user to Windows Update")
        elif platform.system() == "Darwin":
            webbrowser.open("https://support.apple.com/en-us/HT201541")
            logger.info("Directed user to macOS Update")
        else:
            logger.warning("Update check for unsupported system: " + platform.system())

            alert_dialog = ft.AlertDialog(
            title=ft.Text("Update Information"),  # Use ft.Text for title
            content=ft.Text("Please check your system settings or package manager for updates."),
            actions=[ft.ElevatedButton("Close", on_click=lambda _: page.alert_dialog.close_button())]  # Use actions for buttons
            )
            alert_dialog.open()

    # Buttons for initiating update checks
    update_buttons_container = ft.Container(
        content=ft.Column([
            ft.ElevatedButton("Check System Updates", on_click=check_system_updates, bgcolor=ft.colors.TEAL,style=ft.ButtonStyle(foreground_color=ft.colors.WHITE)) ]),
        width=400,
        padding=10,
        bgcolor=ft.colors.TEAL
    )
    page.add(update_buttons_container)

# Run the Flet app
if __name__ == "__main__":
    ft.app(target=main)
