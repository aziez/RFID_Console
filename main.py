import serial
from serial import *
import serial.tools.list_ports
import requests
import threading
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

PRESET_Value = 0xFFFF
POLYMONIAL = 0x8408

port = None
pos = None
no_reader = 'FF'
uid_str = None

url = 'https://fekdi.co.id/rfid'

# DATA RFID CARD
#scan
INVENTORY1 = f'06 {no_reader} 01 00 06' #Membaca TID
INVENTORY2 = f'04 {no_reader} 0F' #Membaca EPC

#Read EPC
readTagMem = f'12 {no_reader} 02 02 11 22 33 44 01 00 04 00 00 00 00 00 02'

#Change EPC
writeEpc = '0F 03 04 03 00 00 00 00 11 22 33 44 55 66'

#Set Data
setAddress = '05 03 24 00'

print("RFID READER CONSOLE APP \n")
port = str(input("Input COM Port : "))

serial = Serial(port, 57600, timeout=0.1)

pos = int(input("Input Possition RFID :"))


def crc(cmd):
    cmd = bytes.fromhex(cmd)
    uiCrcValue = PRESET_Value
    for x in range((len(cmd))):
        uiCrcValue = uiCrcValue ^ cmd[x]
        for y in range(8):
            if (uiCrcValue & 0x0001):
                uiCrcValue = (uiCrcValue >> 1) ^ POLYMONIAL
            else:
                uiCrcValue = uiCrcValue >> 1
    crc_H = (uiCrcValue >> 8) & 0xFF
    crc_L = uiCrcValue & 0xFF
    cmd = cmd + bytes([crc_L])
    cmd = cmd + bytes([crc_H])
    return cmd

def send_cmd(cmd):
    data_scan = crc(cmd)
    serial.write(data_scan)
    response = serial.read(512)
    response_hex = response.hex().upper()
    hex_list = [response_hex[i:i + 2] for i in range(0, len(response_hex), 2)]
    # print(hex_list)
    hex_space = ' '.join(hex_list)
    uid = hex_space[-6:]
    uid_str = uid.replace(" ", "")
    data_scan = {
        "pos": pos,
        "kode": uid_str
    }
    # print(data_scan)
    if(hex_space.find("FB") != -1):
        print("Kartu Tidak Terdeteksi")
    elif(hex_space.find("FE") != -1):
        print("Kartu tidak terdeteksi")
    elif(hex_space == ""):
        print("Data Kosong")
    else:
        print(f"UID Kartu : {uid_str}")
        sendApi = requests.get(url, params=data_scan, verify=False)
        print(sendApi)

def sendData():
    global thread
    send_cmd(INVENTORY1)
    thread = threading.Timer(1.0, sendData)
    thread.start()

sendData()




# if __name__ == '__main__':