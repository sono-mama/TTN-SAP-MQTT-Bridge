import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import ssl
import json
from datetime import datetime

# Parameters The Things Network
ttn_hostname = "eu1.cloud.thethings.network"
ttn_port = 1883
ttn_auth = {
    'username':"", # YOUR USERNAME
    'password':"" # YOUR PASSWORD
    }
subscribe_topic = '#' # '#' = all topics

# Parameters SAP IoT Cockpit
device_id_list = {
    '':'',
    } # Dictionary to map the TTN device IDs to SAP Device Alternative IDs 'device_id':'alternative_id'
pem_cert_file_path = "./certificates/"
mqtt_server_url = "cp.iot.sap" # YOUR SAP IOT COCKPIT URL
mqtt_server_port = 8883
ack_topic_level = "ack/"
measures_topic_level = "measures/"

# Result Code List   
rcList = {                                                    
       0: "Connection successful",                               
       1: "Connection refused - incorrect protocol version",     
       2: "Connection refused - invalid client identifier",      
       3: "Connection refused - server unavailable",             
       4: "Connection refused - bad username or password",       
       5: "Connection refused",                                  
}                                                             

def send_message_to_sap(device_id, payload):
    client = None
    sensor_alt_id = None
    payload_int = None
    topic = measures_topic_level + device_id_list[device_id]

    if payload == False:
        payload_int = 0
    elif payload == True:
        payload_int = 1
    else:
        print("invalid payload")
         
    if device_id == "": # YOUR DEVICE ID
        sensor_alt_id = "" # CORRESPONDING ALT ID OF THE SENSOR BEING USED BY THE DEVICE
        client = sap_clients[0]
    # ADD OR DELETE DEPENDING ON NO OF DEVICES
    elif device_id == "":
        sensor_alt_id = "" 
        client = sap_clients[1]
    else:
        print("Invalid Device_ID. Can't send message.")

    message = f'{{ "capabilityAlternateId": "", "sensorAlternateId": "{sensor_alt_id}", "measures": [{{"occupancy": {payload_int}}}] }}'
    client.publish(topic, message) # YOUR CAPABILITY ID

def on_connect_ttn(client, userdata, flags, rc):  
    print(str(datetime.now()) + " | Connecting to MQTT Broker : " + ttn_hostname)
    print(str(datetime.now()) + " | Connected with result code {0}".format(str(rc)))
    print()
    print(str(datetime.now()) + " | Subscribing to MQTT Topics")
    print(str(datetime.now()) + " | Subscribing to " + subscribe_topic)
    client.subscribe(subscribe_topic)
    print()

def on_message_ttn(client, userdata, msg):
    global mqtt_topic
    mqtt_topic = msg.topic
    global mqtt_payload
    mqtt_payload = json.loads(msg.payload)
#   # Check your TTN uplink payload and adjust these fields acordingly 
    mqtt_payload_device = mqtt_payload['end_device_ids']['device_id']
    mqtt_payload_occupancy = mqtt_payload['uplink_message']['decoded_payload']['decoded']['occupied']

    print(str(datetime.now()) + " | Message received...")
    print(str(datetime.now()) + " | MQTT Topic: ")
    print("-------------------------")                                          
    print(mqtt_topic)
    print("-------------------------")                                          
    print(str(datetime.now()) + " | MQTT Payload: ")
    print("-------------------------")                                          
    print("Device ID: " + str(mqtt_payload_device))  
    print("Occupied: " + str(mqtt_payload_occupancy))
    print("-------------------------")                                          
    
    send_message_to_sap(mqtt_payload_device, mqtt_payload_occupancy)

def on_connect_sap(client, userdata, flags, rc):
    curr_client_id = client._client_id.decode('utf-8')
    print(str(datetime.now()) + " | " + rcList.get(rc, "Unknown server connection return code {}.".format(rc)) + " (" + curr_client_id + ")") 
    client.subscribe(ack_topic_level + curr_client_id, qos = 1)                                                  

def on_message_sap(client, userdata, msg):
    print(str(datetime.now()) + " | Response received...")
    print(str(datetime.now()) + " | MQTT Topic: ")
    print("-------------------------")                                          
    print(msg.topic)
    print("-------------------------")                                          
    print(str(datetime.now()) + " | Status: ")
    print("-------------------------")                                          
    print(json.loads(msg.payload)[0]['code'])
    print("-------------------------")                                          

# Connection to SAP IoT Cockpit

# TO DO: If you have multiple devices on your SAP IoT Cockpit using one router device might be the better way
sap_clients = []

for i in range(): # ADD RANGE
    client = mqtt.Client(device_id_list["" + str(i)], clean_session = False) # DEVICE ID PREFIX
    client.on_connect = on_connect_sap
    client.on_message = on_message_sap
    client.tls_set(certfile = pem_cert_file_path + "" + str(i) + ".pem", 
            cert_reqs = ssl.CERT_REQUIRED, tls_version = ssl.PROTOCOL_TLS,
            ciphers = None) # ADJUST ACORDING TO YOUR CERTIFICATE NAME
    print(str(datetime.now()) + " | Connecting to " + "" + str(i) + " on SAP IoT Cockpit")
    client.connect(mqtt_server_url, mqtt_server_port)
    client.loop_start()
    sap_clients.append(client)

# Connection to The Things Network
ttn_client = mqtt.Client(client_id = "mqtt_ttn", clean_session = False)
ttn_client.on_connect = on_connect_ttn
ttn_client.on_message = on_message_ttn
ttn_client.username_pw_set(ttn_auth["username"], ttn_auth["password"])
ttn_client.connect(ttn_hostname, ttn_port, 60)  
ttn_client.loop_forever()

