import flet.dev as fd

class UpdateCheckerApp:
    def __init__(self):
        self.root = fd.Window(title="Update Checker", width=800, height=400, bg='#333333')
        
        # Enhanced font and color configuration for larger UI elements
        self.font_style = ("Consolas", 14)  # Increase font size
        self.button_color = "#15065c"
        self.text_color = "#FFFFFF"
        self.button_text_color = "#FFFFFF"
        self.label_bg_color = "#333333"

        # Show Logs Button
        self.show_logs_button = fd.Button(self.root, text="Show Logs", command=self.show_logs, bg=self.button_color, fg=self.button_text_color, font=self.font_style)
        self.show_logs_button.pack(pady=10)

        # Hardware Information Label
        self.hardware_info_label = fd.Label(self.root, text="", bg=self.label_bg_color, fg=self.text_color, font=self.font_style)
        self.hardware_info_label.pack(pady=20)
        self.get_hardware_info()

        # Loading Indicator
        self.loading_indicator = fd.Progressbar(self.root, mode="indeterminate")
        self.loading_indicator.pack(pady=10)

        # Status Label
        self.status_label = fd.Label(self.root, text="", bg=self.label_bg_color, fg=self.text_color, font=self.font_style)
        self.status_label.pack(pady=10)

        # Check Updates Button
        self.check_updates_button = fd.Button(self.root, text="System Updates", command=self.check_updates, bg=self.button_color, fg=self.button_text_color, font=self.font_style)
        self.check_updates_button.pack(pady=10)

        # Check Software Updates Button
        self.check_software_updates_button = fd.Button(self.root, text="Check Installed Software", command=self.check_software_updates, bg=self.button_color, fg=self.button_text_color, font=self.font_style)
        self.check_software_updates_button.pack(pady=10)

        self.setup_logging()

        self.hardware_info_label = flet.Label(root, text="", bg=self.label_bg_color, fg=self.text_color,
                                            font=self.font_style)
        self.hardware_info_label.pack(pady=20)  # Increase vertical padding

        # Loading indicator
        self.loading_indicator = flet.Progressbar(root)

        # Status label
        self.status_label = flet.Label(root, text="", bg=self.label_bg_color, fg=self.text_color, font=self.font_style)

        # Larger buttons with increased padding
        self.check_updates_button = flet.Button(root, text="Check for Updates", command=self.check_updates,
                                              bg=self.button_color, fg=self.button_text_color,
                                              font=self.font_style)
        self.check_updates_button.pack(pady=10)

        self.check_software_updates_button = flet.Button(root, text="Check Software Updates",
                                                       command=self.check_software_updates,
                                                       bg=self.button_color, fg=self.button_text_color,
                                                       font=self.font_style)
        self.check_software_updates_button.pack(pady=10)

        self.choose_log_location_button = flet.Button(root, text="Choose Log Location",
                                                    command=self.choose_log_location,
                                                    bg=self.button_color, fg=self.button_text_color,
                                                    font=self.font_style)
        self.choose_log_location_button.pack(pady=10)

    def create_custom_dialog(self, title, message):
        dialog = flet.Dialog(self.root)
        dialog.title = title
        dialog.bg = '#333333'
        dialog.size = (600, 400)

        message_label = flet.Label(dialog, text=message, wraplength=350, bg=self.label_bg_color, fg=self.text_color,
                                 font=self.font_style)
        message_label.pack(padx=10, pady=10)

        close_button = flet.Button(dialog, text="Close", command=dialog.destroy, bg=self.button_color,
                                 fg=self.button_text_color, font=self.font_style)
        close_button.pack(pady=10)

    def setup_logging(self):
        self.logger = logging.getLogger("UpdateCheckerApp")
        self.logger.setLevel(logging.DEBUG)

        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

        self.history_handler = RotatingFileHandler("update_history.log", maxBytes=1024 * 1024, backupCount=5)
        self.history_handler.setLevel(logging.INFO)
        self.history_handler.setFormatter(formatter)
        self.logger.addHandler(self.history_handler)

        self.error_handler = RotatingFileHandler("error_log.log", maxBytes=1024 * 1024, backupCount=5)
        self.error_handler.setLevel(logging.ERROR)
        self.error_handler.setFormatter(formatter)
        self.logger.addHandler(self.error_handler)

    def get_hardware_info(self):
        system_info = platform.uname()
        info_text = f"System: {system_info.system}\nNode Name: {system_info.node}\n" \
                    f"Release: {system_info.release}\nVersion: {system_info.version}\n" \
                    f"Machine: {system_info.machine}\nProcessor: {system_info.processor}"
        self.hardware_info_label.text = info_text

    def get_user_consent(self):
        return flet.message_box.ask_yes_no("User Consent", "Do you want to check for updates?")

    def show_loading_indicator(self):
        self.loading_indicator.pack(pady=10)
        self.loading_indicator.start()

    def hide_loading_indicator(self):
        self.loading_indicator.stop()
        self.loading_indicator.pack_forget()

    def update_status_label(self, text):
        self.status_label.text = text
        self.status_label.pack(pady=10)

    def check_updates(self):
        self.get_hardware_info()
        if self.get_user_consent():
            if platform.system() == 'Windows':
                subprocess.run(["powershell", "Install-Module PSWindowsUpdate -Force -AllowClobber"])
                subprocess.run(["powershell", "Get-WindowsUpdate -Install -AcceptAll"])
                self.logger.info("Windows Update checked")

            elif platform.system() == 'Darwin':
                subprocess.run(["softwareupdate", "-i", "-a"])
                self.logger.info("macOS Update checked")

            elif platform.system() == 'Linux':
                dist_id = distro.id()
                update_command = ""
                if "ubuntu" in dist_id or "debian" in dist_id:
                    update_command = "sudo apt-get update && sudo apt-get upgrade -y"
                elif "fedora" in dist_id or "centos" in dist_id:
                    update_command = "sudo dnf update -y"
                elif "arch" in dist_id:
                    update_command = "sudo pacman -Syu"
                else:
                    self.create_custom_dialog("Linux Update Information",
                                              "Your Linux distribution is not supported for automatic updates through this script.")
                    return
                self.create_custom_dialog("Update Information",
                                          f"For your system ({dist_id}), use the following command to update:\n{update_command}")
                self.logger.info(f"Linux Update Information provided for {dist_id}")
                subprocess.run(update_command.split())

            else:
                self.create_custom_dialog("Unsupported System",
                                          "Updates are not supported for the current operating system.")
            self.logger.info("Update process completed.")

    def check_software_updates(self):
        if platform.system() == "Windows":
            installed_programs = self.get_installed_programs_windows()
        elif platform.system() == "Darwin":
            installed_programs = self.get_installed_programs_mac()
        else:
            print("Unsupported operating system")
            return

        popup = flet.Dialog(self.root)
        listbox = flet.Listbox(popup)
        listbox.pack()

        for name, version in installed_programs.items():
            update = self.check_update(name)
            if update:
                listbox.insert(flet.END, f"{name}: {version} -> {update}")

        scrollbar = flet.Scrollbar(popup, command=listbox.yview)
        scrollbar.pack(side=flet.RIGHT, fill=flet.Y)
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
            output = output.decode("utf-8").split("\n")
            for line in output:
                if "<key>_name</key>" in line:
                    name = line.split("<string>")[1].split("</string>")[0]
                elif "<key>version</key>" in line:
                    version = line.split("<string>")[1].split("</string>")[0]
                    installed_programs[name] = version
        except subprocess.CalledProcessError:
            pass
        return installed_programs

    def check_update(self, name):
        return "2.0"  # Dummy update version

    def choose_log_location(self):
        log_location = flet.file_dialog.ask_directory()
        if log_location:
            self.history_handler.baseFilename = f"{log_location}/update_history.log"
            self.error_handler.baseFilename = f"{log_location}/error_log.log"
            self.create_custom_dialog("Log Location Updated", f"Log files will be saved in: {log_location}")


if __name__ == "__main__":
    app = UpdateCheckerApp()
    app.root.run()
