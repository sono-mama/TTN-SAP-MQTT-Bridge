# TTN-SAP-MQTT-Bridge

Python based MQTT Bridge to forward MQTT data from The Things Network to SAP IoT Service

The goal of this script is to subscribe to MQTT Data from your The Things Network console and publish it to your digital twins created in [SAP IoT Cockpit](https://help.sap.com/docs/SAP_CP_IOT_NEO/7436c3125dd5491f939689f18954b1e9/b74941c0cd0141db838e53b106c1d6f4.html?locale=en-US). 

Since you can not subscribe to MQTT topics directly from within SAP IoT Cockpit you need to have some way of forwarding the data. This script is based on the ideas outlined in this [SAP blog post](https://blogs.sap.com/2020/08/16/good-things-come-in-small-pieces-mqtt-from-python/).

This script needs to be adjusted acording to the amout of devices, sensors and capabilities you have but should give a general outine on how to forward the MQTT data.

In case of multiple devices it would probably be better to use a Router Device in the SAP Cockpit instead of adressing all devices directly from the bridge like I did. 
