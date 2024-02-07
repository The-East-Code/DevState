import tkinter as tk
from tkinter import ttk, messagebox, filedialog, Listbox, Scrollbar, Text, font
import platform
import subprocess
import distro
import logging
from logging.handlers import RotatingFileHandler
import pkgutil
#import winreg
from bs4 import BeautifulSoup
import urllib.request

    
if platform.system() == 'Windows':
    import winreg
    import os
    import shutil
    import datetime


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

        
        self.hardware_info_label = tk.Label(root, text="", bg=self.label_bg_color, fg=self.text_color, font=self.font_style)
        self.hardware_info_label.pack(pady=20)  # Increase vertical padding
        # Display hardware information
        self.hardware_info_label = tk.Label(root, text="")
        self.hardware_info_label.pack()
        
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
        self.backup_path = "testBakup"
        if not os.path.exists(self.backup_path):
            os.makedirs(self.backup_path)
            self.logger.info("Backup directory created successfully.")
        else:
            self.logger.info("Backup directory already exists.")
        # Button for rollback updates
        self.rollback_button = tk.Button(root, text="Rollback Updates", command=self.rollback_updates)
        self.rollback_button.pack(pady=10)  # Add some padding for aesthetic purposes

        # Check for any existing backup and offer rollback option
        if self.check_existing_backup():
            rollback_prompt = messagebox.askyesno("Rollback Updates", "A previous backup exists. Do you want to rollback updates?")
            if rollback_prompt:
                self.rollback_updates()
            else:
                self.logger.info("User chose not to rollback updates.")

    def check_existing_backup(self):
        # Check if there's any existing backup
        if os.listdir(self.backup_path):
            return True
        else:
            return False

    def rollback_updates(self):
        try:
            # Backup directory name with timestamp
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            backup_path = "testBak" + timestamp
            
            # Check if the backup directory already exists
            if os.path.exists(backup_path):
                # If it exists, create a new unique backup directory name
                backup_path = "nova__" + timestamp
                
            # Create the backup directory
            os.makedirs(backup_path)

            # Copy files from the root directory to the backup directory
            for root, dirs, files in os.walk("/"):
                for file in files:
                    src_file = os.path.join(root, file)
                    dest_file = os.path.join(backup_path, os.path.relpath(src_file, "/"))

                    # Check if destination file exists and is writable
                    if os.path.exists(dest_file) and not os.access(dest_file, os.W_OK):
                        self.logger.warning(f"Skipping {dest_file}: Permission denied")
                        continue

                    # Copy file from root directory to backup directory
                    shutil.copy2(src_file, dest_file)
                    self.logger.info(f"Copied {src_file} to {dest_file}")

            # Inform the user about the successful rollback
            messagebox.showinfo("Rollback Successful", "Updates have been rolled back successfully.")
        except Exception as e:
            # Log any errors that occur during the rollback process
            self.logger.error(f"Error occurred during rollback: {str(e)}")
            messagebox.showerror("Rollback Failed", "Error occurred during rollback. Please check logs for details.")




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

        self.setup_logging()

        self.hardware_info_label = tk.Label(root, text="", bg=self.label_bg_color, fg=self.text_color,
                                            font=self.font_style)
        self.hardware_info_label.pack(pady=20)  # Increase vertical padding

        # Loading indicator
        self.loading_indicator = ttk.Progressbar(root, orient="horizontal", mode="indeterminate")

        # Status label
        self.status_label = tk.Label(root, text="", bg=self.label_bg_color, fg=self.text_color, font=self.font_style)


    def create_custom_dialog(self, title, message):
        dialog = tk.Toplevel(self.root)
        dialog.title(title)
        dialog.configure(bg='#333333')  # Dark background for dialog
        dialog.geometry("600x400")  # Adjust size as needed

        # Message label
        message_label = tk.Label(dialog, text=message, wraplength=350, bg=self.label_bg_color, fg=self.text_color,
                                 font=self.font_style)
        message_label.pack(padx=10, pady=10)

        # Close button
        close_button = tk.Button(dialog, text="Close", command=dialog.destroy, bg=self.button_color,
                                 fg=self.button_text_color, font=self.font_style)
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


    def get_user_consent(self):
        return messagebox.askyesno("User Consent", "Do you want to install your system updates?")


    def show_loading_indicator(self):
        self.loading_indicator.pack(pady=10)
        self.loading_indicator.start()


    def hide_loading_indicator(self):
        self.loading_indicator.stop()
        self.loading_indicator.pack_forget()


    def update_status_label(self, text):
        self.status_label.config(text=text)
        self.status_label.pack(pady=10)


    def check_updates(self):
        self.get_hardware_info()

        if self.get_user_consent():
            
            ask_if_should_update = messagebox.askyesno("User Consent", "Are you sure?")

            if ask_if_should_update:
                # Create a backup before applying updates
                backup_path = "testBak"
                shutil.copytree("/", backup_path)  # Copy entire system to backup folder
                self.logger.info("System backup created successfully.")
                # Check for updates based on the user's operating system
                if platform.system() == 'Windows':
                    # Trigger Windows Update
                    subprocess.run(["powershell", "Install-Module PSWindowsUpdate -Force -AllowClobber"])
                    subprocess.run(["powershell", "Get-WindowsUpdate -Install -AcceptAll"])
                    self.logger.info("Windows Update checked")

                elif platform.system() == 'Darwin':
                    # Trigger macOS Update
                    subprocess.run(["softwareupdate", "-i", "-a"])
                    self.logger.info("macOS Update checked")

                elif platform.system() == 'Linux':
                    # Use distro.id() to get the distribution ID as a string
                    dist_id = distro.id()
                    update_command = ""
                    if "ubuntu" in dist_id or "debian" in dist_id:
                        update_command = "sudo apt-get update"
                    elif "fedora" in dist_id or "centos" in dist_id:
                        update_command = "sudo dnf update"
                    elif "arch" in dist_id:
                        update_command = "sudo pacman -Syu"
                    else:
                        self.create_custom_dialog("Linux Update Information",
                                                "Your Linux distribution is not supported for automatic updates through this script.")
                        return
                    self.create_custom_dialog("Update Information",
                                            f"For your system ({dist_id}), use the following command to update:\n{update_command}")
                    self.logger.info(f"Linux Update Information provided for {dist_id}")
                    # Run the update command in the terminal
                    subprocess.run(update_command.split())

                else:
                    self.create_custom_dialog("Unsupported System",
                                            "Updates are not supported for the current operating system.")
                self.logger.info("Update process completed.")
                
                # Check if user wants to roll back updates
                rollback_prompt = messagebox.askyesno("Rollback Updates", "Do you want to rollback updates?")
                if rollback_prompt:
                    # Rollback updates by restoring from backup
                    if os.path.exists(backup_path):
                        shutil.rmtree("/")
                        shutil.copytree(backup_path, "/")
                        self.logger.info("Updates rolled back successfully.")
                        messagebox.showinfo("Rollback Successful", "Updates have been rolled back successfully.")
                    else:
                        self.logger.error("Backup not found. Unable to rollback updates.")
                        messagebox.showerror("Rollback Failed", "Backup not found. Unable to rollback updates.")
                else:
                    self.logger.info("User chose not to rollback updates.")
            
            else:
                self.create_custom_dialog("User Does Not Consent",
                                          "Understood. Updates will not be installed on your system. Thank you.")
                self.logger.info("User chose not to install updates.")

                   
        else:
            self.create_custom_dialog("User Does Not Consent",
                                                "Understood. PatchNova will not install any updates on your system. Thank you.")


    def check_software_updates(self):
        if platform.system() == "Windows":
            installed_programs = self.get_installed_programs_windows()
        elif platform.system() == "Darwin":
            installed_programs = self.get_installed_programs_mac()
        else:
            print("Unsupported operating system")
            return

        # Create popup
        popup = tk.Toplevel(self.root)
        popup.geometry("500x600")  # Set the size of the popup window
        popup.title("Installed Software")  # Set title
        popup.configure(bg="dark gray")  # Set background color
        # Customize font style for Listbox
        listbox_font = font.Font(family="Helvetica", size=12, weight="bold")
        listbox = Listbox(popup, font=listbox_font, bg="gray", fg="blue")  # Set font, background color, and foreground color
        listbox.pack(side="left", fill="both", expand=True, padx=10, pady=10)  # Expand to fill the popup window, add padding

        # Check updates
        for name, version in installed_programs.items():
            listbox.insert(tk.END, f"{name}: {version}")

        # Add scrollbar
        scrollbar = Scrollbar(popup, command=listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        listbox.config(yscrollcommand=scrollbar.set)


    def get_installed_programs_windows(self):
        installed_programs = {}
        reg_path = r"Software\Microsoft\Windows\CurrentVersion\Uninstall"
        try:
            with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, reg_path) as reg_key:
                for i in range(winreg.QueryInfoKey(reg_key)[0]):
                    try:
                        key = winreg.EnumKey(reg_key, i)
                        with winreg.OpenKey(reg_key, key) as val:
                            name = winreg.QueryValueEx(val, "DisplayName")[0]
                            version = winreg.QueryValueEx(val, "DisplayVersion")[0]
                            installed_programs[name] = version
                    except OSError:
                        pass
        except FileNotFoundError:
            pass
        return installed_programs


    def get_installed_programs_mac(self):
        installed_programs = {}
        try:
            output = subprocess.check_output(["/usr/sbin/system_profiler", "SPApplicationsDataType", "-xml"])
            soup = BeautifulSoup(output, features='xml')

            for item in soup.find_all('dict'):
                name_tag = item.find('key', string='_name')
                version_tag = item.find('key', string='version')

                if name_tag and version_tag:
                    name = name_tag.find_next('string').text
                    version = version_tag.find_next('string').text
                    installed_programs[name] = version

        except subprocess.CalledProcessError:
            pass

        return installed_programs


if __name__ == "__main__":
    root = tk.Tk()
    app = UpdateCheckerApp(root)
    root.mainloop()