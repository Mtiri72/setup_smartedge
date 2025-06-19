from smartedge_installer.core.base_installer import BaseInstaller
from smartedge_installer.utils.logger import get_logger
import subprocess
import venv
import os
import logging
logger = get_logger("NodeInstaller")

class NodeInstaller(BaseInstaller):
    def __init__(self):
        super().__init__()
        logger.info("NodeInstaller: Initialized installer.")

    def run(self):
        print("\n➡️  Starting installation for: Node")
        logger.info("NodeInstaller: Starting installation sequence.")

        self.pre_checks()
        self.install_dependencies()
        self.setup_virtualenv_and_install_python_deps()
        self.configure_network()
        self.validate_installation()
        logger.info("NodeInstaller: ✅ Installation completed successfully.")

    def pre_checks(self):
        self.logger.info("Running pre-checks for Node...")
        # Ensure script is not run as root
        if os.geteuid() == 0:
            self.logger.warning("It is recommended to run the installer as a normal user with sudo access, not as root.")

    def install_dependencies(self):
        self.logger.info("Installing dependencies for Node...")

        apt_packages = [
            "net-tools", "screen", "python3-pip", "python3-venv", "iproute2", "ethtool",
            "make", "cmake", "gcc", "git", "libgmp-dev", "libelf-dev", "zlib1g-dev", "libjansson-dev"
        ]
        self.install_apt_dependencies(apt_packages)

        pip_packages = [
            "psutil"
        ]
        self.install_pip_dependencies(pip_packages)

        self.install_nikss()

    def install_nikss(self):
        self.logger.info("Installing NIKSS from source...")
        try:
            scripts_dir = os.path.join(os.path.dirname(__file__), "../scripts")
            install_script = os.path.join(scripts_dir, "install_nikss.sh")

            if not os.path.exists(install_script):
                self.logger.error(f"NIKSS installation script not found at {install_script}")
                return

            subprocess.run(["bash", install_script], check=True)
            self.logger.info("NIKSS installed successfully.")
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Failed to install NIKSS: {e}")

    def configure_network(self):
        self.logger.info("No specific network configuration needed for Node at this stage.")
        venv_python = os.path.expanduser("~/smartedge_program/.venv/bin/python")
        script_path = os.path.expanduser("~/setup_smartedge/smartedge_installer/scripts/node_interface_prompt.py")
        subprocess.run([venv_python, script_path])
        try:
            logger.info("NodeInstaller: Adding loopback alias lo:0 with IP 127.1.0.2/32")
            subprocess.run(
                ["sudo", "ip", "addr", "add", "127.1.0.2/32", "dev", "lo", "label", "lo:0"],
                check=True
            )
            logger.info("✅ Loopback alias lo:0 configured successfully.")
        except subprocess.CalledProcessError as e:
            logger.error(f"❌ Failed to configure loopback alias: {e}")

    def validate_installation(self):
        self.logger.info("Validating Node setup...")
        # Check if nikss-ctl is available
        result = subprocess.run(["which", "nikss-ctl"], stdout=subprocess.PIPE)
        if result.returncode == 0:
            self.logger.info("✅ nikss-ctl is correctly installed.")
        else:
            self.logger.warning("❌ nikss-ctl was not found in PATH.")
        self.post_install_prompt()

    def setup_virtualenv_and_install_python_deps(self):
        logger.info("NodeInstaller: Setting up Python venv and installing Python dependencies...")
        project_dir = os.path.expanduser("~/smartedge_program")
        venv_dir = os.path.join(project_dir, ".venv")

        if not os.path.exists(venv_dir):
            venv.create(venv_dir, with_pip=True)

        pip_path = os.path.join(venv_dir, "bin", "pip")

        # UPDATED: path to requirements inside setup_smartedge
        requirements_path = os.path.expanduser(
            "~/setup_smartedge/smartedge_installer/requirements/node.txt"
        )

        subprocess.run([pip_path, "install", "--upgrade", "pip"])
        subprocess.run([pip_path, "install", "-r", requirements_path])
