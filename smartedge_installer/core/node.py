from smartedge_installer.core.base_installer import BaseInstaller

class NodeInstaller(BaseInstaller):
    def pre_checks(self):
        self.logger.info("Running pre-checks for Node...")

    def install_dependencies(self):
        self.logger.info("Installing dependencies for Node...")

    def configure_network(self):
        self.logger.info("Configuring network for Node...")

    def validate_installation(self):
        self.logger.info("Validating Node setup...")
