# Import necessary libraries
import board
import busio
import digitalio
import adafruit_requests as requests
import adafruit_esp32spi.adafruit_esp32spi_socket as socket
from adafruit_esp32spi import adafruit_esp32spi

# Define Wi-Fi connection details
wifi_ssid = "YOUR_WIFI_SSID"
wifi_password = "YOUR_WIFI_PASSWORD"

# Define API endpoint for transmitting data to the central ESP32 node
central_node_url = "http://central_node_ip_address:port/data_endpoint"

# Initialize SPI bus and ESP32 pins
spi = busio.SPI(board.SCK, board.MOSI, board.MISO)
cs = digitalio.DigitalInOut(board.D5)
esp32_ready = digitalio.DigitalInOut(board.D6)
reset = digitalio.DigitalInOut(board.D9)
esp = adafruit_esp32spi.ESP_SPIcontrol(spi, cs, esp32_ready, reset)

# Initialize ESP32 SPI interface
requests.set_socket(socket, esp)

# Connect to Wi-Fi
print("Connecting to Wi-Fi...")
while not esp.is_connected:
    try:
        esp.connect_AP(wifi_ssid, wifi_password)
    except Exception as e:
        print("Error connecting to Wi-Fi:", e)
        continue
print("Connected to Wi-Fi!")

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
