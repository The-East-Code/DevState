import tkinter as tk
from tkinter import ttk, messagebox, Text, font
import platform
import subprocess
import logging
from logging.handlers import RotatingFileHandler
import os
import shutil
import datetime

if platform.system() == 'Windows':
    import winreg

class UpdateCheckerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Update Checker")

        # Increase the initial size of the main window
        self.root.geometry('1000x500')  # Adjust width and height as needed
        self.root.configure(bg='#333333')  # Dark background for the main window

        # Enhanced font and color configuration for larger UI elements
        self.font_style = ("Consolas", 16)  # Increase font size
        self.button_color = "#15065c"
        self.text_color = "#FFFFFF"
        self.button_text_color = "#FFFFFF"
        self.label_bg_color = "#333333"

        self.backup_button = tk.Button(root, text="System Backup", command=self.system_backup, bg=self.button_color, fg=self.button_text_color, font=self.font_style)
        self.backup_button.pack(pady=10)  # Add some padding for aesthetic purposes

        # Other initialization code...

        self.hardware_info_label = tk.Label(root, text="", bg=self.label_bg_color, fg=self.text_color, font=self.font_style)
        self.hardware_info_label.pack(pady=20)  # Increase vertical padding
        
        self.get_hardware_info()

        # Loading indicator
        self.loading_indicator = ttk.Progressbar(root, orient="horizontal", mode="indeterminate")
        
        # Status label
        self.status_label = tk.Label(root, text="", bg=self.label_bg_color, fg=self.text_color, font=self.font_style)

        # Larger buttons with increased padding
        self.check_updates_button = tk.Button(root, text="System Updates", command=self.check_updates, bg=self.button_color, fg=self.button_text_color, font=self.font_style)
        self.check_updates_button.pack(pady=10)  # Increase vertical padding
        
        self.check_software_updates_button = tk.Button(root, text="Check Installed Software", command=self.check_software_updates, bg=self.button_color, fg=self.button_text_color, font=self.font_style)
        self.check_software_updates_button.pack(pady=10)  # Increase vertical padding
        
        self.show_logs_button = tk.Button(root, text="Show Logs", command=self.show_logs, bg=self.button_color, fg=self.button_text_color, font=self.font_style)
        self.show_logs_button.pack(pady=10)

        self.setup_logging()

        # Initialize backup directory for update rollback
        self.backup_path = "testBackup"

        # Check for any existing backup and offer rollback option
        if self.check_existing_backup():
            rollback_prompt = messagebox.askyesno("Rollback Updates", "A previous backup exists. Do you want to rollback updates?")
            if rollback_prompt:
                self.rollback_updates()
            else:
                self.logger.info("User chose not to rollback updates.")

    def check_existing_backup(self):
        # Check if there's any existing backup
        if os.path.exists(self.backup_path) and os.listdir(self.backup_path):
            return True
        return False

    def system_backup(self):
        # Create the backup directory only if the system backup button is pressed
        if not os.path.exists(self.backup_path):
            os.makedirs(self.backup_path)
            self.logger.info("Backup directory created successfully.")
        else:
            self.logger.info("Backup directory already exists.")

        # Create progress bar popup
        self.progress_window = tk.Toplevel(self.root)
        self.progress_window.title("Backup Progress")
        self.progress_label = tk.Label(self.progress_window, text="Backup in progress...")
        self.progress_label.pack(pady=10)
        self.progress_bar_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(self.progress_window, orient='horizontal', length=300, mode='determinate', variable=self.progress_bar_var)
        self.progress_bar.pack(pady=10)

        # Backup files
        total_files = sum(len(files) for _, _, files in os.walk("/"))
        current_file = 0
        for root, dirs, files in os.walk("/"):
            for file in files:
                src_file = os.path.join(root, file)
                dest_file = os.path.join(self.backup_path, os.path.relpath(src_file, "/"))

                # Check if destination file exists and is writable
                if os.path.exists(dest_file) and not os.access(dest_file, os.W_OK):
                    self.logger.warning(f"Skipping {dest_file}: Permission denied")
                    continue

                # Copy file from root directory to backup directory
                shutil.copy2(src_file, dest_file)
                self.logger.info(f"Copied {src_file} to {dest_file}")
                
                # Update progress
                current_file += 1
                progress_percentage = (current_file / total_files) * 100
                self.progress_bar_var.set(progress_percentage)
                self.progress_window.update_idletasks()

        # Inform the user about the successful backup
        messagebox.showinfo("Backup Successful", "System backup completed successfully.")
        self.progress_window.destroy()

    def rollback_updates(self):
        # Rollback updates by restoring from backup
        try:
            if os.path.exists(self.backup_path):
                shutil.rmtree("/")
                shutil.copytree(self.backup_path, "/")
                self.logger.info("Updates rolled back successfully.")
                messagebox.showinfo("Rollback Successful", "Updates have been rolled back successfully.")
            else:
                self.logger.error("Backup not found. Unable to rollback updates.")
                messagebox.showerror("Rollback Failed", "Backup not found. Unable to rollback updates.")
        except Exception as e:
            self.logger.error(f"Error occurred during rollback: {str(e)}")
            messagebox.showerror("Rollback Failed", f"Error occurred during rollback: {str(e)}")

    def show_logs(self):
        log_dialog = tk.Toplevel(self.root)
        log_dialog.title("Logs")
        log_dialog.geometry("800x600")  # Adjust size as needed
        log_dialog.configure(bg='#333333')
        tab_control = ttk.Notebook(log_dialog)  # Define tab_control variable

        update_history_tab = ttk.Frame(tab_control)
        tab_control.add(update_history_tab, text='Update History')
        update_history_text = Text(update_history_tab, wrap='word', yscrollcommand=lambda *args: True)
        update_history_text.pack(expand=True, fill='both')

        error_log_tab = ttk.Frame(tab_control)
        tab_control.add(error_log_tab, text='Error Log')
        error_log_text = Text(error_log_tab, wrap='word', yscrollcommand=lambda *args: True)
        error_log_text.pack(expand=True, fill='both')
        
        tab_control.pack(expand=True, fill='both')  

        with open("update_history.log", "r") as file:
            update_history_text.insert('1.0', file.read())
        
        with open("error_log.log", "r") as file:
            error_log_text.insert('1.0', file.read())

        close_button = tk.Button(log_dialog, text="Close", command=log_dialog.destroy, bg=self.button_color, fg=self.button_text_color, font=self.font_style)
        close_button.pack(pady=10)

    def setup_logging(self):
        # Create a logger
        self.logger = logging.getLogger("UpdateCheckerApp")
        self.logger.setLevel(logging.DEBUG)
        # Create a formatter and add it to the handler
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        # Create a rotating file handler for update history
        self.history_handler = RotatingFileHandler("update_history.log", maxBytes=1024 * 1024, backupCount=5)
        self.history_handler.setLevel(logging.INFO)
        self.history_handler.setFormatter(formatter)
        self.logger.addHandler(self.history_handler)
        # Create a rotating file handler for errors
        self.error_handler = RotatingFileHandler("error_log.log", maxBytes=1024 * 1024, backupCount=5)
        self.error_handler.setLevel(logging.ERROR)
        self.error_handler.setFormatter(formatter)
        self.logger.addHandler(self.error_handler)

    def get_hardware_info(self):
        system_info = platform.uname()
        info_text = f"System: {system_info.system}\nNode Name: {system_info.node}\n" \
                    f"Release: {system_info.release}\nVersion: {system_info.version}\n" \
                    f"Machine: {system_info.machine}\nProcessor: {system_info.processor}"
        self.hardware_info_label.config(text=info_text)

    # Remaining methods...

if __name__ == "__main__":
    root = tk.Tk()
    app = UpdateCheckerApp(root)
    root.mainloop()
git ch