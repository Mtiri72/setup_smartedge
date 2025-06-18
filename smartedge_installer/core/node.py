from smartedge_installer.core.base_installer import BaseInstaller
import subprocess
import os
import logging

class NodeInstaller(BaseInstaller):
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

    def validate_installation(self):
        self.logger.info("Validating Node setup...")
        # Check if nikss-ctl is available
        result = subprocess.run(["which", "nikss-ctl"], stdout=subprocess.PIPE)
        if result.returncode == 0:
            self.logger.info("✅ nikss-ctl is correctly installed.")
        else:
            self.logger.warning("❌ nikss-ctl was not found in PATH.")
