from smartedge_installer.core.base_installer import BaseInstaller

class AccessPointInstaller(BaseInstaller):
    def pre_checks(self):
        self.logger.info("Running pre-checks for Access Point...")

    def install_dependencies(self):
        self.logger.info("Installing dependencies for Access Point...")

    def configure_network(self):
        self.logger.info("Configuring network for Access Point...")

    def validate_installation(self):
        self.logger.info("Validating Access Point setup...")
