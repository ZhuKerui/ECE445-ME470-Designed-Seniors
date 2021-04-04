#include "keebot_ble.h"

BLEServer *Keebot_BLE::pServer = NULL;
BLEService *Keebot_BLE::pService = NULL;
BLECharacteristic *Keebot_BLE::pTxCharacteristic = NULL;
BLECharacteristic *Keebot_BLE::pRxCharacteristic = NULL;
bool Keebot_BLE::deviceConnected = false;
bool Keebot_BLE::oldDeviceConnected = false;

void Keebot_BLE::start(std::string name) {
    // Create the BLE Device
    BLEDevice::init(name);
    // Create the BLE Server
    pServer = BLEDevice::createServer();
    // Setup the server callback function
    pServer->setCallbacks(new MyServerCallbacks());
    // Create the BLE Service
    pService = pServer->createService(SERVICE_UUID);
    // Create BLE TX Characteristic
    pTxCharacteristic = pService->createCharacteristic(CHARACTERISTIC_UUID_TX, BLECharacteristic::PROPERTY_NOTIFY);
    pTxCharacteristic->addDescriptor(new BLE2902());
    // Create BLE RX Characteristic
    pRxCharacteristic = pService->createCharacteristic(CHARACTERISTIC_UUID_RX, BLECharacteristic::PROPERTY_WRITE);
    pRxCharacteristic->setCallbacks(new MyCallbacks());     // Setup the characteristic callback function

    pService->start();                                      // Start the service
}

void Keebot_BLE::start_broadcasting() {
    pServer->getAdvertising()->start();                     // Start boardcasting
    deviceConnected = false;
    oldDeviceConnected = false;
}

void Keebot_BLE::send_data(uint8_t* data, size_t length) {
    pTxCharacteristic->setValue(data, length);              // Set the message
    pTxCharacteristic->notify();                            // Send the nodification to the client
}

void Keebot_BLE::MyServerCallbacks::onConnect(BLEServer* pServer) {     // Create a server callback function for server events
    Keebot_BLE::oldDeviceConnected = Keebot_BLE::deviceConnected;
    Keebot_BLE::deviceConnected = true;
}

void Keebot_BLE::MyServerCallbacks::onDisconnect(BLEServer* pServer) {
    Keebot_BLE::oldDeviceConnected = Keebot_BLE::deviceConnected;
    Keebot_BLE::deviceConnected = false;
}

void Keebot_BLE::MyCallbacks::onWrite(BLECharacteristic *pCharacteristic) {      // The data is received by a write operation from the client to this characteristic
    std::string rxValue = pCharacteristic->getValue();  // Get the written value in string
    uint8_t * pData = pCharacteristic->getData();       // Get the written value in uint8_t
    
    if (rxValue.length() > 0) {                         // Print the received data to the serial
        Serial.print("Received Value: ");
        for (int i = 0; i < rxValue.length(); i++)
            Serial.print(rxValue[i]);
        Serial.println();
    }
}