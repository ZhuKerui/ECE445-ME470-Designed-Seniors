import pygatt
from time import sleep
from PyQt5.QtCore import QObject, QThread

device_addr = 'D4:22:DA:37:43:E7'
read_uuid = '0000fff1-0000-1000-8000-00805f9b34fb'
write_uuid = '0000fff2-0000-1000-8000-00805f9b34fb'

class BLE_Driver(QThread):
    def __init__(self, device_addr:str, read_uuid:str, write_uuid:str, read_handler, parent:QObject=None):
        super(BLE_Driver, self).__init__(parent=parent)

        self.adapter = pygatt.GATTToolBackend()
        self.adapter.start()
        self.device_addr = device_addr
        self.read_uuid = read_uuid
        self.write_uuid = write_uuid
        self.read_handler = read_handler
        self.data = None
        self.__new_data = False
        self.__alive = False
        self.__connected = False

    def run(self):
        self.__alive = True
        while self.__alive:
            try:
                self.device = self.adapter.connect(self.device_addr, address_type=pygatt.BLEAddressType.random)
                self.__connected = True
                self.device.subscribe(self.read_uuid, callback=self.read_handler)
                while self.__alive:
                    if not self.__new_data:
                        sleep(0.01)
                        continue
                    self.device.char_write(self.write_uuid, self.data)
                    self.__new_data = False
            except:
                print('Connection err')
            self.__connected = False

    def write(self, msg:bytes):
        if msg is not None:
            self.data = msg
            self.__new_data = True

    def stop(self):
        if self.__alive:
            self.__alive = False
            if self.__connected:
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
        sleep(20)
        ble_driver.stop()
    except Exception as e:
        print(e)