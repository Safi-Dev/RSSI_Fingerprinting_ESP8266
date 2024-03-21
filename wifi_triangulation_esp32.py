# Import necessary libraries
import board
import busio
import digitalio
import time
import math
import adafruit_esp32spi.adafruit_esp32spi_socket as socket
from adafruit_esp32spi import adafruit_esp32spi

# Define Wi-Fi AP details
ap_ssid = "ESP32_AP"  # SSID of the Wi-Fi network transmitted by the ESP32
ap_password = "esp32password"  # Password for the Wi-Fi network

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

# Dictionary to store AP data with their positions
ap_data = {}

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
    
    # Process received data
    data = data.decode().strip()
    ssid, signal_strength = data.split(",")
    signal_strength = int(signal_strength)
    
    # Store data with client position
    ap_data[client_address] = {"ssid": ssid, "signal_strength": signal_strength}
    print("Data received from", client_address, ":", ap_data[client_address])
    
    # Perform triangulation if data is available from at least three APs
    if len(ap_data) >= 3:
        # Triangulation algorithm is here although, I did take it from online and it looks pretty bad ngl (temporary)
        def distance(x1, y1, x2, y2):
            return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
        
        # Function to perform trilateration
        def trilaterate(ap1_pos, ap1_strength, ap2_pos, ap2_strength, ap3_pos, ap3_strength):
            # Extract AP positions
            x1, y1 = ap1_pos
            x2, y2 = ap2_pos
            x3, y3 = ap3_pos
            
            # Extract AP signal strengths
            r1 = ap1_strength
            r2 = ap2_strength
            r3 = ap3_strength
            
            # Calculate distances between APs and client
            d1 = r1
            d2 = r2
            d3 = r3
            
            # Calculate positions of potential intersection points
            A = 2 * x2 - 2 * x1
            B = 2 * y2 - 2 * y1
            C = d1 ** 2 - d2 ** 2 - x1 ** 2 + x2 ** 2 - y1 ** 2 + y2 ** 2
            D = 2 * x3 - 2 * x2
            E = 2 * y3 - 2 * y2
            F = d2 ** 2 - d3 ** 2 - x2 ** 2 + x3 ** 2 - y2 ** 2 + y3 ** 2
            
            # Calculate client position
            x = (C * E - F * B) / (E * A - B * D)
            y = (C * D - A * F) / (B * D - A * E)
            
            return x, y
        
        # Example usage:
        ap1_pos = (0, 0)
        ap1_strength = 10
        ap2_pos = (5, 0)
        ap2_strength = 8
        ap3_pos = (2.5, 4)
        ap3_strength = 6

client_pos = trilaterate(ap1_pos, ap1_strength, ap2_pos, ap2_strength, ap3_pos, ap3_strength)
print("Estimated client position:", client_pos)
    # Send response back to client (Wemos D1 Mini)
    client_socket.send("Data received".encode())
    
    # Close client socket
    client_socket.close()
