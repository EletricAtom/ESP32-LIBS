import network

# ESP32 Configuration as Access Point
ssid = "My_NetWorK_32"  # Wi-Fi network name
password = "phoenix_01"  # Password with at least 8 characters

ap = network.WLAN(network.AP_IF)  # Access Point mode
ap.active(True)  # Activate the Wi-Fi network
ap.config(essid=ssid, password=password, authmode=network.AUTH_WPA2_PSK)  # Set WPA2

print("Waiting for connections...")
while not ap.active():
    pass  # Wait until the network is active

print("Wi-Fi network is active!")
print("ESP32 IP:", ap.ifconfig()[0])  # Display the ESP32 IP

# Get the MAC address
mac_address = ap.config('mac')

# Convert to readable format (hexadecimal)
mac_str = ':'.join(['{:02X}'.format(b) for b in mac_address])

#Print the mac address for us
print("ESP32 MAC address:", mac_str)
