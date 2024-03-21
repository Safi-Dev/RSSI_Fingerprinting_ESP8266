# WiFi Triangulation Backpack

This project aims to create a portable system for triangulating the positions of Wi-Fi Access Points (APs) using Wemos D1 Mini boards mounted on a backpack. By collecting signal strength information from multiple APs at different locations, the system calculates the approximate position of each AP using triangulation techniques.

## Aim
The primary objective of this project is to create an effective and accurate method for mapping Wi-Fi APs in various environments. By deploying three Wemos D1 Mini boards on a backpack and a central ESP32 node, I aim to enable mobile Wi-Fi triangulation.

## Components
- x3 Wemos D1 Mini boards
- x1 ESP32 development board (central node)
- x1 Backpack with compartments or pockets for mounting
- Small breadboards or custom PCBs for mounting the Wemos D1 Minis
- Jumper wires
- x1 USB power bank for powering the Wemos D1 Minis and ESP32 node

## Usage

1. Mount the Wemos D1 Mini boards securely on the backpack at different points.
2. Connect each Wemos D1 Mini to a USB power bank for power supply.
3. Flash each Wemos D1 Mini with firmware to scan for nearby Wi-Fi APs and collect signal strength information.
4. Configure the central ESP32 node to receive data from the Wemos D1 Mini boards.
5. Process the collected data on the central ESP32 node using triangulation algorithms to determine the approximate positions of Wi-Fi APs.
6. Visualize the positions of Wi-Fi APs on a map using software interfaced with the central ESP32 node.

## Contributors
- [Safi-Dev](https://github.com/safi-dev) - Project Lead & Developer

## License
This project is licensed under the [CC BY-NC-SA 4.0](LICENSE.md) License
