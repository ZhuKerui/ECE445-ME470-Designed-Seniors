import pygatt
import time

device_addr = 'D4:22:DA:37:43:E7'
read_uuid = '0000fff1-0000-1000-8000-00805f9b34fb'
write_uuid = '0000fff2-0000-1000-8000-00805f9b34fb'

class BLE_Driver:
    def __init__(self, device_addr:str, read_uuid:str, write_uuid:str, read_handler):
        self.adapter = pygatt.GATTToolBackend()
        self.device_addr = device_addr
        self.read_uuid = read_uuid
        self.write_uuid = write_uuid
        self.read_handler = read_handler
        self.is_alive = False

    def start(self):
        self.adapter.start()
        try:
            self.device = self.adapter.connect(self.device_addr, address_type=pygatt.BLEAddressType.random)
        except:
            self.adapter.stop()
            self.is_alive = False
            print('Connection err')
            return
        self.device.subscribe(self.read_uuid, callback=self.read_handler)
        self.is_alive = True

    def write(self, msg:bytes):
        if self.is_alive:
            self.device.char_write(self.write_uuid, msg)

    def stop(self):
        if self.is_alive:
            self.device.disconnect()
            self.adapter.stop()

if __name__ == '__main__':

    def handle_data(handle:int, value:bytearray):
        """
        handle -- integer, characteristic read handle the data was received on
        value -- bytearray, the data returned in the notification
        """
        print("Received data: %s" % (value.decode('utf-8')))

    try:
        ble_driver = BLE_Driver(device_addr=device_addr, read_uuid=read_uuid, write_uuid=write_uuid, read_handler=handle_data)
        ble_driver.start()
        ble_driver.write("hello world".encode())
        time.sleep(20)
        ble_driver.stop()
    except Exception as e:
        print(e)