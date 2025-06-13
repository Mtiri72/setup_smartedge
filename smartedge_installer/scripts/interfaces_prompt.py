import psutil
import subprocess

def prompt_for_interface_rename():
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

if __name__ == "__main__":
    prompt_for_interface_rename()
