# Import necessary libraries
import board
import busio
import digitalio
import time
import adafruit_esp32spi.adafruit_esp32spi_socket as socket
from adafruit_esp32spi import adafruit_esp32spi
from adafruit_esp32spi import adafruit_esp32spi_wifimanager

# Define Wi-Fi connection details
wifi_ssid = "ESP32_AP"  # SSID of the ESP32 access point
wifi_password = "esp32password"  # Password for the ESP32 access point

# Initialize SPI bus and ESP32 pins
spi = busio.SPI(board.SCK, board.MOSI, board.MISO)
cs = digitalio.DigitalInOut(board.D5)
ready = digitalio.DigitalInOut(board.D6)
reset = digitalio.DigitalInOut(board.D9)
esp = adafruit_esp32spi.ESP_SPIcontrol(spi, cs, ready, reset)

# Initialize ESP32 SPI interface
esp.set_network(wifi_ssid, wifi_password)

# Initialize WiFi manager
wifi_manager = adafruit_esp32spi_wifimanager.ESPSPI_WiFiManager(esp)

# Connect to Wi-Fi
print("Connecting to Wi-Fi...")
wifi_manager.connect()

# Get the IP address of the central ESP32 node using mDNS
central_node_ip = socket.getaddrinfo("central-node.local", 80)[0][-1][0]
central_node_port = 80

# Define API endpoint for transmitting data to the central ESP32 node
central_node_url = "http://" + central_node_ip + ":" + str(central_node_port) + "/data"

print("Connected to Wi-Fi!")
print("Central node IP address:", central_node_ip)

# Main loop
while True:
    try:
        # Scan for nearby Wi-Fi Access Points
        ap_list = esp.scan_networks()
        
        # Process scan results
        for ap in ap_list:
            ssid = ap["ssid"]
            signal_strength = ap["rssi"]
            # Send data to central ESP32 node
            payload = {"ssid": ssid, "signal_strength": signal_strength}
            response = requests.post(central_node_url, json=payload)
            print("Data sent to central node:", response.text)
            response.close()
    except Exception as e:
        print("Error:", e)
        continue
