from tkinter import  *
from tkinter import ttk
# VARIABLE
port = ""
pos = None
no_reader = 'FF'
uid_str = None



main = Tk()

btnScan = ttk.Button
btnSet = ttk.Button

lbPort = ttk.Label
lbPos = ttk.Label

lbDataPort = ttk.Label
lbDataPos = ttk.Label
lbDataUid = Label

enPort = ttk.Entry
enPos = ttk.Entry

# FRAME WINDOW
frameConfig = ttk.LabelFrame(main)
frameConfig.configure(height=200, width=200, text="Konfigurasi RFID")
frameConfig.pack(side="top")

frameData = ttk.LabelFrame(main)
frameData.configure(height=200, width=200, text="DATA Reader")
frameData.pack(side="top")

btnScan = ttk.Button(main)
btnScan.configure(text="START SCAN", padding=25)
btnScan.pack(side="top", padx=25, pady=25)


# KOMPONENT FRAME KONFIG
lbPort = ttk.Label(frameConfig, text="COM Port : ", font=("Helvetica", 10))
lbPort.pack(side="left")

enPort = ttk.Entry(frameConfig, width=10)
enPort.insert("0", port)
enPort.pack(side="left", padx=10)

lbPos = ttk.Label(frameConfig, text="Posisi Reader : ", font=("Arial", 10))
lbPos.pack(side="left")

enPort = ttk.Entry(frameConfig)
enPort.insert("0", port)
enPort.pack(side="left", padx=10, pady=10)

btnSet = ttk.Button(frameConfig)
btnSet.configure(text="Set Reader", padding=5)
btnSet.pack(side="bottom", padx=10, pady=10)

# KOMPONENT FRAME DATA RFID
lbDataPort = ttk.Label(frameData, text=f"PORT = {port}", foreground="blue", padding=10)
lbDataPort.pack(side="top", pady=25, padx=25)


main.geometry("600x400")


main.mainloop()