import threading
from tkinter import  *
from tkinter import ttk
import requests
import serial
from serial import *
import urllib3
from tkinter import  messagebox

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# VARIABLE
port = ""
pos = ""
no_reader = 'FF'
uid_str = None
start = True
thread = None
test_serial = None
console = None
epcValue = None
uidLatest = None
sendApi = None


# PRESET RFID
PRESET_Value = 0xFFFF
POLYMONIAL = 0x8408

# PROTOCOL SCANNER RFID
#scan
INVENTORY1 = f'06 {no_reader} 01 00 06' #Membaca TID
INVENTORY2 = f'04 {no_reader} 0F' #Membaca EPC

#Read EPC
readTagMem = f'12 {no_reader} 02 02 11 22 33 44 01 00 04 00 00 00 00 00 02'

#Change EPC
writeEpc = '0F 03 04 03 00 00 00 00 11 22 33 44 55 66'

#Set Data
setAddress = '05 03 24 00'

# API SENDER VARIABLE
url = 'https://fekdi.co.id/rfid'
data = {}

# VARIABLE GUI
btnScan = ttk.Button
btnSet = ttk.Button
textData = Text

lbPort = ttk.Label
lbPos = ttk.Label

lbDataPort = ttk.Label
lbDataPos = ttk.Label
lbDataUid = Label
lbSerial = Label
lbUidLatest = Label

enPort = ttk.Entry
enPos = ttk.Entry

portStatus = messagebox


# COMMUNICATION FUNCTION
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


def setReader():
    global  test_serial
    try:
        port = enPort.get()
        pos = enPos.get()
        test_serial = Serial(port, 57600, timeout=0.1)
        lbDataPort.configure(text=f"Port = {port}", background="green", foreground="white")
        lbDataPos.configure(text=f"Reader POS = {pos}")
        btnScan['state'] = 'normal'
    except serial.SerialException as e:
        portStatus.showerror("PORT TIDAK TERBUKA", e)
        enPort.delete(3, "end")
        enPort.focus()
        btnScan['state'] = 'disabled'
    except TypeError as e:
        print(f"Port Closed{e}")
        btnScan['state'] = 'disabled'
    else:
        return test_serial


def sendData():
    global thread
    send_cmd(INVENTORY1)
    thread = threading.Timer(0, sendData)
    thread.start()

def send_cmd(cmd):
    global console
    global sendApi
    data_scan = crc(cmd)
    test_serial.write(data_scan)
    response = test_serial.read(512)
    response_hex = response.hex().upper()
    hex_list = [response_hex[i:i + 2] for i in range(0, len(response_hex), 2)]
    hex_space = ' '.join(hex_list)
    uid = hex_space[-6:]
    uid_str = uid.replace(" ", "")
    uidLatest = uid_str
    data_scan = {
        "pos": pos,
        "kode": uid_str
    }
    if (hex_space.find("FB") != -1):
        textData.config(fg="black", font='Arial 15')
        textData.delete(1.0, "end")
        textData.insert(0.0,"Kartu Tidak Terdeteksi \n")
    elif (hex_space.find("FE") != -1):
        textData.delete(1.0, "end")
        textData.insert(0.0,"Kartu Tidak Terdeteksi \n")
    elif (hex_space == ""):
        btnSet["state"] = 'normal'
        textData.config(fg="black", font='Arial 15')
        textData.insert(0.0,"PORT COM TIDAK TERDETEKSI !!! \n")
        enPort.delete(3, "end")
        enPort.focus()
        btnScan.configure(text="START SCAN")
        thread.cancel()
    else:
        if (uidLatest == uid_str):
            lbUidLatest.configure(text=f"Latest UID = {uidLatest}")
            textData.insert(0.0, f"PASSS")
        else:
            sendApi = requests.get(url, params=data_scan, verify=False)
            lbUidLatest.configure(text=f"Latest UID = {uidLatest}")
            textData.config(fg="blue", font='Helvetica 15 bold')
            textData.delete(1.0, "end")
            textData.insert(0.0, f"UID : {uid_str}\n Status :{sendApi}  \n")


def triggerScan():
    global start

    if start:
        btnSet["state"] = 'disabled'
        btnScan.configure(text="STOP SCAN")
        textData.delete(0.0, 'end')
        sendData()
        start = False
    else:
        btnSet["state"] = 'normal'
        btnScan.configure(text="START SCAN")
        textData.delete(0.0, 'end')
        thread.cancel()
        start = True


# TKINKER GUI
main = Tk()

# FRAME WINDOW
frameConfig = ttk.LabelFrame(main)
frameConfig.configure(height=200, width=200, text="Konfigurasi RFID")
frameConfig.pack(side="top")

frameLatest = ttk.Frame(main)
frameLatest.configure(height=25, width = 50)
frameLatest.pack(side="top")

frameData = ttk.LabelFrame(main)
frameData.configure(width=200, height=200, text="DATA SCANNER")
frameData.pack(side="bottom")

framePort = ttk.Frame(frameData)
framePort.configure(height=100, width=100, borderwidth=3)
framePort.pack(side="left", anchor=SW)

framePos = ttk.Frame(frameData)
framePos.configure(height=100, width=100, borderwidth=3)
framePos.pack(side="right", anchor=SE)

frameReturn = ttk.Frame(main)
frameReturn.configure(height=200, width=350)
frameReturn.pack(side='top')

textData = Text(frameReturn, width=50, height=25, font="Helvetica 15")
textData.pack(side="left", anchor=W, pady=25, padx=25)

btnScan = ttk.Button(frameReturn)
btnScan.configure(text="START SCAN", padding=25, command=triggerScan)
btnScan['state'] = 'disabled'
btnScan.pack(side="right", anchor=E)


# KOMPONENT FRAME KONFIG
lbPort = ttk.Label(frameConfig, text="COM Port : ", font='Helvetica 15 bold', background="green", foreground="white")
lbPort.pack(side="left")

enPort = ttk.Entry(frameConfig, width=15, font="Arial 14 bold")
enPort.insert("0", port.upper())
enPort.pack(side="left", padx=10)

lbPos = ttk.Label(frameConfig, text="Reader POS : ", font='Helvetica 15 bold', background="green", foreground="white")
lbPos.pack(side="left")

enPos = ttk.Entry(frameConfig, width=10, font="Arial 14 bold")
enPos.insert("0", pos.upper())
enPos.pack(side="left", padx=10)

btnSet = ttk.Button(frameConfig)
btnSet.configure(text="Set Reader", padding=10, command=setReader)
btnSet.pack(side="bottom", padx=10, pady=10)

# KOMPONENT FRAME DATA RFID
lbDataPort = ttk.Label(framePort, text=f"Port = {port.upper()}", background="red", foreground="white", padding=10, font='Helvetica 15 bold')
lbDataPort.pack(anchor=SW)

lbDataPos = ttk.Label(framePos, text=f"Posisi = ", background="blue", foreground="white", padding=10, font='Helvetica 15 bold')
lbDataPos.pack(anchor=SE)

lbUidLatest = ttk.Label(frameLatest, text="Latest UID = ", background="blue", foreground="white", padding=10, font='Helvetica 15 bold')
lbUidLatest.pack(side="left", padx=10, pady=10)
main.geometry("800x400")

main.mainloop()