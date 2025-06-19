import os
import subprocess
import venv
#import psutil
from smartedge_installer.core.base_installer import BaseInstaller
from smartedge_installer.utils.logger import get_logger

logger = get_logger("CoordinatorInstaller")


def prompt_for_interface_rename():
    #import psutil
    print("\n🔧 Detecting network interfaces...\n")
    interfaces = psutil.net_if_addrs().keys()
    interfaces = [iface for iface in interfaces if not iface.startswith("lo")]
    if not interfaces:
        print("❌ No active network interfaces found.")
        return

    print("📡 Available network interfaces:")
    for i, iface in enumerate(interfaces, start=1):
        print(f"{i}. {iface}")

    try:
        selected = int(input("\nPlease select which interface to rename to 'eth0': "))
        selected_iface = list(interfaces)[selected - 1]
        print(f"🔄 Renaming '{selected_iface}' to 'eth0'...")

        subprocess.run(["sudo", "ip", "link", "set", selected_iface, "down"], check=True)
        subprocess.run(["sudo", "ip", "link", "set", selected_iface, "name", "eth0"], check=True)
        subprocess.run(["sudo", "ip", "link", "set", "eth0", "up"], check=True)

        print("✅ Interface renamed successfully.")
    except (IndexError, ValueError):
        print("❌ Invalid selection.")
    except subprocess.CalledProcessError:
        print("❌ Failed to rename interface. You may need to reboot or reconfigure.")



class CoordinatorInstaller(BaseInstaller):
    def __init__(self):
        super().__init__()
        logger.info("CoordinatorInstaller: Initialized installer.")

    def run(self):
        print("\n➡️  Starting installation for: Coordinator")
        logger.info("CoordinatorInstaller: Starting installation sequence.")

        self.pre_checks()
        self.install_dependencies()
        self.setup_virtualenv_and_install_python_deps()
        self.configure_network()
        self.validate_installation()
        logger.info("CoordinatorInstaller: ✅ Installation completed successfully.")

    def pre_checks(self):
        logger.info("CoordinatorInstaller: Running pre-checks for Coordinator...")
        self.check_ubuntu_version()
        self.check_disk_space()

    def install_thrift(self):
        logger.info("CoordinatorInstaller: Installing Apache Thrift (C++ + Python)...")

        try:
            subprocess.run(["thrift", "--version"], check=True, stdout=subprocess.DEVNULL)
            logger.info("Apache Thrift is already installed.")
            return
        except (subprocess.CalledProcessError, FileNotFoundError):
            logger.info("Apache Thrift not found. Proceeding with installation...")

        deps = [
            "automake", "bison", "flex", "g++", "git",
            "libboost-all-dev", "libevent-dev", "libssl-dev",
            "libtool", "make", "pkg-config"
        ]
        subprocess.run(["sudo", "apt-get", "install", "-y"] + deps, check=True)

        smartedge_path = os.path.expanduser("~/smartedge_program")
        thrift_dir = os.path.join(smartedge_path, "ci")
        thrift_script = os.path.join(thrift_dir, "install-thrift.sh")

        if not os.path.exists(thrift_dir):
            os.makedirs(thrift_dir)

        # Write the script content into install-thrift.sh
        script_content = """#!/bin/sh

        THIS_DIR=$( cd \"$( dirname \"${BASH_SOURCE[0]}\" )\" && pwd )

        set -e

        # Clone thrift source
        cd $THIS_DIR
        git clone -b 0.13.0 https://github.com/apache/thrift.git thrift-0.13.0
        cd thrift-0.13.0
        ./bootstrap.sh
        ./configure --with-cpp=yes --with-c_glib=no --with-java=no --with-ruby=no --with-erlang=no --with-go=no --with-nodejs=no
        make -j2 && sudo make install
        cd lib/py
        sudo python3 setup.py install
        cd ../../..
        """
        with open(thrift_script, "w") as f:
            f.write(script_content)

        os.chmod(thrift_script, 0o755)

        subprocess.run(["sudo", "bash", thrift_script], check=True)
        logger.info("✅ Apache Thrift installed successfully.")

    def install_dependencies(self):
        logger.info("CoordinatorInstaller: Installing dependencies for Coordinator...")
        subprocess.run(["sudo", "apt-get", "update"])
        subprocess.run(["sudo", "apt-get", "install", "-y", "docker.io"])

        # Start Cassandra container
        subprocess.run(["sudo", "docker", "pull", "cassandra:latest"])
        # Start BMv2 container
        subprocess.run(["sudo", "docker", "pull", "p4lang/behavioral-model"])
        subprocess.run(["sudo", "apt-get", "install", "-y", "net-tools"])
        self.install_apt_dependencies(["docker.io", "net-tools", "python3-pip", "python3-venv", "screen"])
        self.install_thrift()
    
    def install_thrift(self):
        logger.info("CoordinatorInstaller: Installing Apache Thrift (C++ + Python)...")

        try:
            subprocess.run(["thrift", "--version"], check=True, stdout=subprocess.DEVNULL)
            logger.info("Apache Thrift is already installed.")
            return
        except (subprocess.CalledProcessError, FileNotFoundError):
            logger.info("Apache Thrift not found. Proceeding with installation...")

        deps = [
            "automake", "bison", "flex", "g++", "git",
            "libboost-all-dev", "libevent-dev", "libssl-dev",
            "libtool", "make", "pkg-config"
        ]
        subprocess.run(["sudo", "apt-get", "install", "-y"] + deps, check=True)

        smartedge_path = os.path.expanduser("~/smartedge_program")
        thrift_dir = os.path.join(smartedge_path, "ci")
        thrift_script = os.path.join(thrift_dir, "install-thrift.sh")

        if not os.path.exists(thrift_dir):
            os.makedirs(thrift_dir)

        # Write the script content into install-thrift.sh
        script_content = """#!/bin/sh

        THIS_DIR=$( cd \"$( dirname \"${BASH_SOURCE[0]}\" )\" && pwd )

        set -e

        # Clone thrift source
        cd $THIS_DIR
        git clone -b 0.13.0 https://github.com/apache/thrift.git thrift-0.13.0
        cd thrift-0.13.0
        ./bootstrap.sh
        ./configure --with-cpp=yes --with-c_glib=no --with-java=no --with-ruby=no --with-erlang=no --with-go=no --with-nodejs=no
        make -j2 && sudo make install
        cd lib/py
        sudo python3 setup.py install
        cd ../../..
        """
        with open(thrift_script, "w") as f:
            f.write(script_content)

        os.chmod(thrift_script, 0o755)

        subprocess.run(["sudo", "bash", thrift_script], check=True)
        logger.info("✅ Apache Thrift installed successfully.")
        
    

    def setup_virtualenv_and_install_python_deps(self):
        logger.info("CoordinatorInstaller: Setting up Python venv and installing Python dependencies...")
        project_dir = os.path.expanduser("~/smartedge_program")
        venv_dir = os.path.join(project_dir, ".venv")

        if not os.path.exists(venv_dir):
            venv.create(venv_dir, with_pip=True)

        pip_path = os.path.join(venv_dir, "bin", "pip")

        # UPDATED: path to requirements inside setup_smartedge
        requirements_path = os.path.expanduser(
            "~/setup_smartedge/smartedge_installer/requirements/coordinator.txt"
        )

        subprocess.run([pip_path, "install", "--upgrade", "pip"])
        subprocess.run([pip_path, "install", "-r", requirements_path])


    def configure_network(self):
        logger.info("CoordinatorInstaller: Configuring network for Coordinator...")
        venv_python = os.path.expanduser("~/smartedge_program/.venv/bin/python")
        script_path = os.path.expanduser("~/setup_smartedge/smartedge_installer/scripts/interface_prompt.py")
        subprocess.run([venv_python, script_path])
        try:
            logger.info("CoordinatorInstaller: Adding loopback alias lo:0 with IP 127.1.0.2/32")
            subprocess.run(
                ["sudo", "ip", "addr", "add", "127.1.0.2/32", "dev", "lo", "label", "lo:0"],
                check=True
            )
            logger.info("✅ Loopback alias lo:0 configured successfully.")
        except subprocess.CalledProcessError as e:
            logger.error(f"❌ Failed to configure loopback alias: {e}")


    def validate_installation(self):
        logger.info("CoordinatorInstaller: Validating Coordinator setup...")
        self.post_install_prompt()
        # Placeholder: to be implemented later as needed
