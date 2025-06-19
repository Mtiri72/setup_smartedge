from smartedge_installer.core.base_installer import BaseInstaller
import subprocess
import os
import shutil
import venv
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
        subprocess.run(["sudo", "apt-get", "install", "-y", "docker.io"])
        subprocess.run(["sudo", "docker", "pull", "p4lang/behavioral-model"])
        subprocess.run(["sudo", "docker", "tag", "p4lang/behavioral-model", "bmv2se"])
        subprocess.run(["sudo", "apt-get", "install", "-y", "net-tools"])
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
        venv_python = os.path.expanduser("~/smartedge_program/.venv/bin/python")
        script_path = os.path.expanduser("~/setup_smartedge/smartedge_installer/scripts/wireless_interface_prompt.py")
        subprocess.run([venv_python, script_path])
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

        self.post_install_prompt()

    
