import network


class Network:
    """
    Before each use of network, please add the statement “import network” to the top of the python file.
    WLAN(interface_id): Set to WiFi mode.
    network.STA_IF: Client, connecting to other WiFi access points.
    network.AP_IF: Access points, allowing other WiFi clients to connect.
    active(is_active): With parameters, it is to check whether to activate the network interface; Without
    parameters, it is to query the current state of the network interface.
    scan(ssid, bssid, channel, RSSI, authmode, hidden): Scan for wireless networks available nearby (only
    scan on STA interface), return a tuple list of information about the WiFi access point.
    bssid: The hardware address of the access point, returned in binary form as a byte object. You can use
    ubinascii.hexlify() to convert it to ASCII format.
    authmode: Access type
    AUTH_OPEN = 0
    AUTH_WEP = 1
    AUTH_WPA_PSK = 2
    AUTH_WPA2_PSK = 3
    AUTH_WPA_WPA2_PSK = 4
    AUTH_MAX = 6
    Hidden: Whether to scan for hidden access points
    False: Only scanning for visible access points
    True: Scanning for all access points including the hidden ones.
    isconnected(): Check whether ESP32 is connected to AP in Station mode. In STA mode, it returns True if it
    is connected to a WiFi access point and has a valid IP address; Otherwise it returns False.
    connect(ssid, password): Connecting to wireless network.
    ssid: WiFiname
    password: WiFipassword
    disconnect(): Disconnect from the currently connected wireless network.
    """

    sta_connection = None

    def sta_setup(self, ssid_router: str, password_router: str):
        self.sta_connection = network.WLAN(network.STA_IF)
        if not self.sta_connection.isconnected():
            print("connecting to", ssid_router)
            self.sta_connection.active(True)
            self.sta_connection.connect(ssid_router, password_router)
            while not self.sta_connection.isconnected():
                pass

        print("Connected, IP address:", self.sta_connection.ifconfig())

    def sta_disconnect(self):
        try:
            self.sta_connection.disconnect()
        except:
            print("Disconnect error")
