import serial.tools.list_ports
import time
import sys
from Adafruit_IO import MQTTClient

AIO_FEED_IDS = ["bbc-temp","bbc-humi","bbc-gas",
                "bbc-infrared","bbc-led","bbc-buzzer",
                "bbc-lightsensor","bbc-door"]
AIO_USERNAME = "hoductri"
AIO_KEY = "aio_jVae40HZgvBWQAYHCUEFyYOWndvv"

def  connected(client):
    print("Ket noi thanh cong...")
    for feed in AIO_FEED_IDS:
        client.subscribe(feed)

def  subscribe(client , userdata , mid , granted_qos):
    print("Subcribe thanh cong...")

def  disconnected(client):
    print("Ngat ket noi...")
    sys.exit (1)

def  message(client , feed_id , payload):
    if feed_id == AIO_FEED_IDS[0]:
        print("Nhan du lieu DHT11 nhiet do: " + payload)
    elif feed_id == AIO_FEED_IDS[1]:
        print("Nhan du lieu DHT11 do am: " + payload)
    elif feed_id == AIO_FEED_IDS[2]:
        print("Nhan du lieu gas sensor: " + payload)
    elif feed_id == AIO_FEED_IDS[3]:
            print("Nhan du lieu infrared sensor: " + payload)
    elif feed_id == AIO_FEED_IDS[4]:
        print("Nhan du lieu den: " + payload)
    elif feed_id == AIO_FEED_IDS[5]:
        print("Nhan du lieu buzzer: " + payload)
    elif feed_id == AIO_FEED_IDS[6]:
        print("Nhan du lieu cam bien anh sang: " + payload)
    elif feed_id == AIO_FEED_IDS[7]:
        print("Nhan du lieu door: " + payload)
    ser.write((str(payload) + "#").encode())

client = MQTTClient(AIO_USERNAME , AIO_KEY)
client.on_connect = connected
client.on_disconnect = disconnected
client.on_message = message
client.on_subscribe = subscribe
client.connect()
client.loop_background()

def getPort():
    ports = serial.tools.list_ports.comports()
    N = len(ports)
    commPort = "None"
    for i in range(0, N):
        port = ports[i]
        strPort = str(port)
        if "USB Serial Device" in strPort:
            splitPort = strPort.split(" ")
            commPort = (splitPort[0])
    return commPort

isMicrobitConnected = False
if getPort() != "None":
    ser = serial.Serial(port=getPort(), baudrate=115200)
    isMicrobitConnected = True

def processData(data):
    data = data.replace("!", "")
    data = data.replace("#", "")
    splitData = data.split(":")
    print(splitData)
    if splitData[1] == "TEMP":
        client.publish(AIO_FEED_IDS[0], splitData[2])
    if splitData[1] == "HUMI":
        client.publish(AIO_FEED_IDS[1], splitData[2])
    if splitData[1] == "GAS":
        client.publish(AIO_FEED_IDS[2], splitData[2])
    if splitData[1] == "INFRARED":
        client.publish(AIO_FEED_IDS[3], splitData[2])
    if splitData[1] == "LAMP":
        client.publish(AIO_FEED_IDS[4], splitData[2])
    if splitData[1] == "BUZZER":
        client.publish(AIO_FEED_IDS[5], splitData[2])
    if splitData[1] == "LIGHT_SENSOR":
        client.publish(AIO_FEED_IDS[6], splitData[2])
    if splitData[1] == "DOOR":
        client.publish(AIO_FEED_IDS[7], splitData[2])

mess = ""
def readSerial():
    bytesToRead = ser.inWaiting()
    if (bytesToRead > 0):
        global mess
        mess = mess + ser.read(bytesToRead).decode("UTF-8")
        while ("#" in mess) and ("!" in mess):
            start = mess.find("!")
            end = mess.find("#")
            processData(mess[start:end + 1])
            if (end == len(mess)):
                mess = ""
            else:
                mess = mess[end+1:]

while True:
    if  isMicrobitConnected == True:
        readSerial()


