from smartedge_installer.constants import ROLE_CHOICES
from smartedge_installer.core.coordinator import CoordinatorInstaller
from smartedge_installer.core.access_point import AccessPointInstaller
from smartedge_installer.core.node import NodeInstaller

def main():
    print("\n🧠 SmartEdge Installer\n")
    print("Please select the role for this machine:\n")
    for key, label in ROLE_CHOICES.items():
        print(f"{key}. {label}")
    
    choice = input("\nEnter the number of the role to install: ").strip()
    
    installer = None
    if choice == "1":
        installer = CoordinatorInstaller()
    elif choice == "2":
        installer = AccessPointInstaller()
    elif choice == "3":
        installer = NodeInstaller()
    else:
        print("❌ Invalid choice. Exiting.")
        return

    print(f"\n➡️  Starting installation for: {ROLE_CHOICES[choice]}")
    installer.run()
