import psutil
import subprocess


def prompt_for_wireless_interface_rename():
        print("\n🔧 Detecting wireless interfaces...\n")
        interfaces = psutil.net_if_addrs().keys()
        non_loopback = [iface for iface in interfaces if not iface.startswith("lo")]
        if not non_loopback:
            print("❌ No usable interfaces found.")
            return

        print("📡 Available interfaces:")
        for i, iface in enumerate(non_loopback, start=1):
            print(f"{i}. {iface}")

        try:
            selected_wlan = int(input("\nPlease select which interface to rename to 'wlan0': "))
            wlan_iface = list(non_loopback)[selected_wlan - 1]
            print(f"🔄 Renaming '{wlan_iface}' to 'wlan0'...")

            subprocess.run(["sudo", "ip", "link", "set", wlan_iface, "down"], check=True)
            subprocess.run(["sudo", "ip", "link", "set", wlan_iface, "name", "wlan0"], check=True)
            subprocess.run(["sudo", "ip", "link", "set", "wlan0", "up"], check=True)

            print("✅ Wireless interface renamed to 'wlan0'.")

            # Refresh interface list after renaming
            interfaces = psutil.net_if_addrs().keys()
            non_loopback = [iface for iface in interfaces if not iface.startswith("lo") and iface != "wlan0"]

            print("\n🌐 Available remaining interfaces:")
            for i, iface in enumerate(non_loopback, start=1):
                print(f"{i}. {iface}")

            selected_eth = int(input("\nPlease select which interface to rename to 'eth0': "))
            eth_iface = list(non_loopback)[selected_eth - 1]
            print(f"🔄 Renaming '{eth_iface}' to 'eth0'...")

            subprocess.run(["sudo", "ip", "link", "set", eth_iface, "down"], check=True)
            subprocess.run(["sudo", "ip", "link", "set", eth_iface, "name", "eth0"], check=True)
            subprocess.run(["sudo", "ip", "link", "set", "eth0", "up"], check=True)

            print("✅ Ethernet interface renamed to 'eth0'.")

        except (IndexError, ValueError):
            print("❌ Invalid selection.")
        except subprocess.CalledProcessError:
            print("❌ Failed to rename interface. You may need to reboot or reconfigure.")


if __name__ == "__main__":
    prompt_for_wireless_interface_rename()
