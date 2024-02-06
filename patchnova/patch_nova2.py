from tkinter.font import BOLD
from turtle import bgcolor, color
import flet as ft
import webbrowser
import platform  # Use platform module for system information

def main(page: ft.Page):
    page.theme = ft.Theme(color_scheme=ft.ColorScheme())
  
    
    # System information container
    system_info_text = f"System: {platform.system()}\n" \
                       f"Node Name: {platform.node()}\n" \
                       f"Release: {platform.release()}\n" \
                       f"Version: {platform.version()}\n" \
                       f"Machine: {platform.machine()}\n" \
                       f"Processor: {platform.processor()}"
                       
    system_info_container = ft.Container(
        content=ft.Text(system_info_text, style=ft.TextStyle(color="black", )),
        width=400,
        padding=10,
        bgcolor="white"
    )
    page.add(system_info_container)

    # Update buttons container
    update_buttons_container = ft.Container(
        content=ft.Column([
            ft.TextButton(
                "Windows Update",
                on_click=lambda _: webbrowser.open("https://support.microsoft.com/en-us/windows/update"),
                tooltip="Opens the official Windows Update page",
            ),
            ft.TextButton(
                "macOS Update",
                on_click=lambda _: webbrowser.open("https://support.apple.com/en-us/HT201509"),
                tooltip="Opens the official Apple Software Update page",
            ),
        ]),
        width=400,
        padding=10,
        bgcolor="teal"
    )
    page.add(update_buttons_container)

    # Browser dropdown container
    browser_dropdown_label = ft.Text("Select A Browser")
    browser_dropdown = ft.Dropdown(
        options=[
            ft.dropdown.Option(text="Chrome"),
            ft.dropdown.Option(text="Firefox")
        ],
        on_change=lambda e: print(f"Selected browser: {e.control.value}"),
        tooltip="Select your preferred browser for update check",
    )
    browser_dropdown_container = ft.Container(
        content=ft.Column([browser_dropdown_label, browser_dropdown]),
        width=400,
        padding=10,
        bgcolor="green"
    )
    page.add(browser_dropdown_container)

    


ft.app(target=main)
