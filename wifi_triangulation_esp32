# Import necessary libraries
import board
import busio
import digitalio
import time
import adafruit_esp32spi.adafruit_esp32spi_socket as socket
from adafruit_esp32spi import adafruit_esp32spi

# Define Wi-Fi AP details
ap_ssid = "ESP32_AP"  # SSID of the Wi-Fi network transmitted by the ESP32
# I RECOMMEND CHANGING THIS
ap_password = "esp32password"  # Password for the Wi-Fi network
# I RECOMMEND CHANGING THIS

# Define API endpoint for receiving data from Wemos D1 Mini boards
data_endpoint = "/data"

# Initialize SPI bus and ESP32 pins
spi = busio.SPI(board.SCK, board.MOSI, board.MISO)
cs = digitalio.DigitalInOut(board.D10)
ready = digitalio.DigitalInOut(board.D11)
reset = digitalio.DigitalInOut(board.D12)

# Initialize ESP32 SPI interface
esp = adafruit_esp32spi.ESP_SPIcontrol(spi, cs, ready, reset)

# Set up ESP32 as an access point
esp.set_mode(adafruit_esp32spi.MODE_AP)
esp.ap_config(ap_ssid, ap_password)

print("ESP32 Access Point SSID:", ap_ssid)
print("Waiting for connections...")

# Set up server to receive data from Wemos D1 Mini boards
socket.set_interface(esp)
server_socket = socket.socket()
server_socket.bind(('0.0.0.0', 80))
server_socket.listen(1)

print("Listening for data from Wemos D1 Mini boards...")

# Main loop
while True:
    client_socket, client_address = server_socket.accept()
    print("Client connected:", client_address)
    
    # Receive data from client (Wemos D1 Mini)
    data = client_socket.recv(1024)
    
    # Process received data (e.g., store in a database)
    print("Received data:", data)
    
    # Send response back to client (Wemos D1 Mini)
    client_socket.send("Data received".encode())
    
    # Close client socket
    client_socket.close()
