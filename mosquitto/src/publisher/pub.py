## @package mqtt_client
#  This script demonstrates a simple MQTT client using the paho.mqtt library.

import paho.mqtt.client as mqtt
import time

## Callback function that is triggered when the client receives a CONNACK response from the server.
#  @param client The instance of the client.
#  @param userdata A dictionary containing user-defined information.
#  @param flags Reserved for future use.
#  @param rc The connection result. 0 indicates a successful connection.
def on_connect(client, userdata, flags, rc):
    """Called when the client receives a CONNACK response from the server."""
    
    if rc == 0:
        print(f"Connected successfully with device name: {userdata['device_name']} and location: {userdata['location']}")
        client.publish("test/topic", f"Device {userdata['device_name']} at {userdata['location']} says Hello!")
    else:
        print(f"Failed to connect with result code: {rc}")

## Client initialization and setup.
if __name__ == '__main__':
    
    ## Create a new MQTT client instance.
    client = mqtt.Client()
    
    ## User-defined data to be utilized in the on_connect callback.
    #  @var device_data
    #  Contains device-specific attributes.
    device_data = {
        "device_name": "TemperatureSensor01",  ///< The name of the device.
        "location": "WarehouseA"               ///< The location of the device.
    }
    
    ## Set the userdata attribute of the client.
    #  This allows access to the device_data in the callback functions.
    client.user_data_set(device_data)
    
    ## Assign the on_connect callback function to the client.
    #  This function will be called when the client connects to the broker.
    client.on_connect = on_connect
    
    ## Connect the client to an MQTT broker.
    #  @param host The hostname or IP address of the broker.
    #  @param port The network port of the server host to connect to. Defaults to 1883.
    #  @param keepalive Maximum period in seconds between communications with the broker.
    client.connect("test.mosquitto.org", 1883, 60)
    
    ## Process network traffic, dispatch callbacks and handle reconnections.
    #  Blocks until an explicit client.loop_stop() is called.
    client.loop_forever()