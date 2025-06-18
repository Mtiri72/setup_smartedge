from smartedge_installer.core.base_installer import BaseInstaller
import subprocess
import os
import shutil
import venv
import psutil
from smartedge_installer.utils.logger import get_logger

logger = get_logger("AccessPointInstaller")

PROGRAM_DIR = os.path.expanduser("~/smartedge_program")
VENV_DIR = os.path.join(PROGRAM_DIR, ".venv")
REQUIREMENTS_FILE = os.path.expanduser("~/setup_smartedge/smartedge_installer/requirements/access_point.txt")
LOOPBACK_ALIAS = "127.1.0.3"

class AccessPointInstaller(BaseInstaller):
    def __init__(self):
        super().__init__()
        logger.info("AccessPointInstaller: Initialized.")

    def run(self):
        print("\n➡️  Starting installation for: Access Point")
        self.pre_checks()
        self.install_dependencies()
        self.setup_virtualenv_and_install_python_deps()
        self.configure_network()
        self.validate_installation()
        logger.info("AccessPointInstaller: ✅ Installation completed successfully.")

    def pre_checks(self):
        self.logger.info("Running pre-checks for Access Point...")
        self.check_ubuntu_version()
        self.check_disk_space(min_gb=2)

    def install_dependencies(self):
        self.logger.info("Installing dependencies for Access Point...")
        apt_packages = [
            "net-tools", "screen", "python3-pip", "python3-venv", "iproute2"
        ]
        self.install_apt_dependencies(apt_packages)

    def setup_virtualenv_and_install_python_deps(self):
        self.logger.info("Setting up virtual environment for Access Point...")
        if not os.path.exists(VENV_DIR):
            venv.create(VENV_DIR, with_pip=True)
        pip_path = os.path.join(VENV_DIR, "bin", "pip")
        subprocess.run([pip_path, "install", "--upgrade", "pip"])
        subprocess.run([pip_path, "install", "-r", REQUIREMENTS_FILE], check=True)

    def configure_network(self):
        self.logger.info("Configuring network for Access Point...")
        self.prompt_for_wireless_interface_rename()
        try:
            subprocess.run([
                "sudo", "ip", "addr", "add", f"{LOOPBACK_ALIAS}/32",
                "dev", "lo", "label", "lo:0"
            ], check=True)
            self.logger.info("Loopback alias lo:0 assigned.")
        except subprocess.CalledProcessError as e:
            self.logger.warning(f"Loopback alias already exists or failed to add: {e}")

    def validate_installation(self):
        self.logger.info("Validating Access Point setup...")
        if os.path.exists(VENV_DIR):
            self.logger.info("Virtual environment is present.")
        else:
            self.logger.error("Virtual environment is missing!")
            raise FileNotFoundError(".venv not found")

        if os.path.exists(REQUIREMENTS_FILE):
            self.logger.info("Requirements file is present.")
        else:
            self.logger.warning("Requirements file is missing.")

    def prompt_for_wireless_interface_rename(self):
        print("\n🔧 Detecting wireless interfaces...\n")
        interfaces = psutil.net_if_addrs().keys()
        wireless_interfaces = [iface for iface in interfaces if not iface.startswith("lo")]
        if not wireless_interfaces:
            print("❌ No wireless interfaces found.")
            return

        print("📡 Available wireless interfaces:")
        for i, iface in enumerate(wireless_interfaces, start=1):
            print(f"{i}. {iface}")

        try:
            selected = int(input("\nPlease select which interface to rename to 'wlan0': "))
            selected_iface = list(wireless_interfaces)[selected - 1]
            print(f"🔄 Renaming '{selected_iface}' to 'wlan0'...")

            subprocess.run(["sudo", "ip", "link", "set", selected_iface, "down"], check=True)
            subprocess.run(["sudo", "ip", "link", "set", selected_iface, "name", "wlan0"], check=True)
            subprocess.run(["sudo", "ip", "link", "set", "wlan0", "up"], check=True)

            print("✅ Interface renamed successfully.")
        except (IndexError, ValueError):
            print("❌ Invalid selection.")
        except subprocess.CalledProcessError:
            print("❌ Failed to rename interface. You may need to reboot or reconfigure.")
