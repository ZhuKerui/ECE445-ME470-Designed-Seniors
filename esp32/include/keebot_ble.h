#include <BLEDevice.h>
#include <BLEServer.h>
#include <BLEUtils.h>
#include <BLE2902.h>
#include <Arduino.h>


// See the following for generating UUIDs:
// https://www.uuidgenerator.net/

#define SERVICE_UUID           "6E400001-B5A3-F393-E0A9-E50E24DCCA9E"   // UART service UUID
#define CHARACTERISTIC_UUID_RX "6E400002-B5A3-F393-E0A9-E50E24DCCA9E"   // Read Characteristic UUID
#define CHARACTERISTIC_UUID_TX "6E400003-B5A3-F393-E0A9-E50E24DCCA9E"   // Write Characteristic UUID


class Keebot_BLE {
    public:

    static void start(std::string name);
    static void start_broadcasting();
    static void send_data(uint8_t* data, size_t length);
    static bool deviceConnected;                    // Present connection status
    static bool oldDeviceConnected;                 // Last connection status

    private:

    static BLEServer *pServer;                      // The BLEServer pointer
    static BLEService *pService;                    // The BLEService for keebot application
    static BLECharacteristic * pTxCharacteristic;   // The BLECharacteristic pointer for sending data
    static BLECharacteristic * pRxCharacteristic;   // The BLECharacteristic pointer for receiving data

    class MyServerCallbacks: public BLEServerCallbacks {     // Create a server callback function for server events
        void onConnect(BLEServer* pServer);
        void onDisconnect(BLEServer* pServer);
    };

    class MyCallbacks: public BLECharacteristicCallbacks {      // Create a characteristic callback function for characteristic read events
        void onWrite(BLECharacteristic *pCharacteristic);       // The data is received by a write operation from the client to this characteristic
    };
};