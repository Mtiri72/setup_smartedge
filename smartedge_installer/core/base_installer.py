import abc
from smartedge_installer.utils.logger import get_logger
import platform
import shutil
import subprocess
logger = get_logger("BaseInstaller")



class BaseInstaller(abc.ABC):
    def __init__(self):
        self.logger = get_logger(self.__class__.__name__)
        self.logger.info("Initialized installer.")

    def run(self):
        try:
            self.logger.info("Starting installation sequence.")
            self.pre_checks()
            self.install_dependencies()
            self.configure_network()
            self.validate_installation()
            self.logger.info("✅ Installation completed successfully.")
        except Exception as e:
            self.logger.error(f"❌ Installation failed: {e}")
            raise

    @abc.abstractmethod
    def pre_checks(self):
        """Perform pre-installation validation (e.g., OS, disk space)"""
        pass

    @abc.abstractmethod
    def install_dependencies(self):
        """Install APT or PIP dependencies"""
        pass

    @abc.abstractmethod
    def configure_network(self):
        """Configure IPs, routes, interfaces, etc."""
        pass

    @abc.abstractmethod
    def validate_installation(self):
        """Run validation checks to confirm SmartEdge can operate"""
        pass

    def check_ubuntu_version(self):
        dist = platform.freedesktop_os_release().get("VERSION_ID", "")
        if not dist.startswith("22.04") and not dist.startswith("24.04"):
            logger.warning("⚠️  This installer supports Ubuntu 22.04 or 24.04 LTS only.")
        else:
            logger.info(f"Ubuntu version check passed: {dist}")

    def check_disk_space(self, min_gb=2):
        total, used, free = shutil.disk_usage("/")
        free_gb = free // (2**30)
        if free_gb < min_gb:
            logger.error(f"❌ Not enough disk space. Required: {min_gb} GB, Available: {free_gb} GB")
            raise SystemExit(1)
        else:
            logger.info(f"Disk space check passed: {free_gb} GB available")

    def install_apt_dependencies(self, packages):
        logger.info(f"📦 Installing system packages: {', '.join(packages)}")
        try:
            subprocess.run(["sudo", "apt-get", "update"], check=True)
            subprocess.run(["sudo", "apt-get", "install", "-y"] + packages, check=True)
            logger.info("✅ System packages installed successfully.")
        except subprocess.CalledProcessError as e:
            logger.error(f"❌ Failed to install system packages: {e}")
            raise

