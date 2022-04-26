'''
#schrijven van waarde 8 ampère naar register 1000
from pyModbusTCP.client import ModbusClient
import time

SERVER_HOST = "10.0.0.182"                  #IP-adres van de laadpaal
SERVER_PORT = 502                           #Deze poort moet 502 zijn vanuit Mennekes

c = ModbusClient()

c.host(SERVER_HOST)
c.port(SERVER_PORT)

while True:
    if not c.is_open():
        if not c.open():
            print("Unable to connect to "+SERVER_HOST+":"+str(SERVER_PORT))

    if c.is_open():
        print("Connected to "+SERVER_HOST+":"+str(SERVER_PORT))
        regs = c.write_single_register(1000, 8)
        if regs:
            print("Value written successful: "+str(regs))
    time.sleep(3)
'''

# ander programma

''' Dit programma kan adresregister 1000 uitlezen en geeft 32 aan
from pyModbusTCP.client import ModbusClient
import time

SERVER_HOST = "10.0.0.182"
SERVER_PORT = 502

c = ModbusClient()

# uncomment this line to see debug message
#c.debug(True)

# define modbus server host, port
c.host(SERVER_HOST)
c.port(SERVER_PORT)

while True:
    # open or reconnect TCP to server
    if not c.is_open():
        if not c.open():
            print("unable to connect to "+SERVER_HOST+":"+str(SERVER_PORT))

    # if open() is ok, read register (modbus function 0x03)
    if c.is_open():
        # read 1 registers at address 1000, store result in regs list
        print("connected to "+SERVER_HOST+":"+str(SERVER_PORT))
        regs = c.read_holding_registers(1000, 1)
        print(regs)
        # if success display registers
        if regs:
            print("Register value: "+str(regs))

    # sleep 2s before next polling
    time.sleep(3)
'''
import serial
import time
from pyModbusTCP.client import ModbusClient

SERVER_HOST = "10.0.0.182"                  #IP-adres van de laadpaal
SERVER_PORT = 502                           #Deze poort moet 502 zijn vanuit Mennekes

c = ModbusClient()

c.host(SERVER_HOST)
c.port(SERVER_PORT)

ser = serial.Serial()

# DSMR 4.0/4.2 > 115200 8N1:
ser.baudrate = 115200
ser.bytesize = serial.EIGHTBITS
ser.parity = serial.PARITY_NONE
ser.stopbits = serial.STOPBITS_ONE

ser.xonxoff = 0
ser.rtscts = 0
ser.timeout = 12
ser.port = "/dev/ttyUSB0"
ser.close()

injectieWatt = 0
verbruikWatt = 0

while True:
    ser.open()
    checksum_found = False

    while not checksum_found:
        telegram_line = ser.readline()
        telegram_line = telegram_line.decode('ascii').strip()
        #print(telegram_line)                               #debug en alle telegrammen

        if telegram_line[0:9] == "1-0:1.7.0":               #verbruik uit telegrammen halen
            verbruikKw = telegram_line[10:15]
            verbruikWatt = float(verbruikKw) * 1000        #omzetten kw naar watt
            verbruikWatt = int(verbruikWatt)              #getal afronden
            #print("Verbruik: ", verbruikWatt, " Watt")     #in console printen

        if telegram_line[0:9] == "1-0:2.7.0":               #injectie uit telegrammen halen
            injectieKw = telegram_line[10:15]
            injectieWatt = float(injectieKw) * 1000         #omzetten kw naar watt
            injectieWatt = int(injectieWatt)                #getal afronden
            #print("Injectie: ", injectieWatt, " Watt")      #in console printen

            if 10 <= injectieWatt <= 20:
                print("laadpaal sturen naar 6A")
                if not c.is_open():
                    if not c.open():
                        print("Unable to connect to " + SERVER_HOST + ":" + str(SERVER_PORT))
                if c.is_open():
                    print("Connected to " + SERVER_HOST + ":" + str(SERVER_PORT))
                    regs = c.write_single_register(1000, 6)
                    if regs:
                        print("Value written successful: " + str(regs))
            elif 21 <= injectieWatt <= 30:
                print("laadpaal sturen naar 8A")
                if not c.is_open():
                    if not c.open():
                        print("Unable to connect to " + SERVER_HOST + ":" + str(SERVER_PORT))

                if c.is_open():
                    print("Connected to " + SERVER_HOST + ":" + str(SERVER_PORT))
                    regs = c.write_single_register(1000, 8)
                    if regs:
                        print("Value written successful: " + str(regs))
            elif 31 <= injectieWatt <= 40:
                print("laadpaal sturen naar 10A")
                if not c.is_open():
                    if not c.open():
                        print("Unable to connect to " + SERVER_HOST + ":" + str(SERVER_PORT))

                if c.is_open():
                    print("Connected to " + SERVER_HOST + ":" + str(SERVER_PORT))
                    regs = c.write_single_register(1000, 10)
                    if regs:
                        print("Value written successful: " + str(regs))
            elif injectieWatt > 41:
                print("laadpaal sturen naar 16A (maximaal)")
                if not c.is_open():
                    if not c.open():
                        print("Unable to connect to " + SERVER_HOST + ":" + str(SERVER_PORT))

                if c.is_open():
                    print("Connected to " + SERVER_HOST + ":" + str(SERVER_PORT))
                    regs = c.write_single_register(1000, 16)
                    if regs:
                        print("Value written successful: " + str(regs))
            else:
                print("te weinig vermogen")
                if not c.is_open():
                    if not c.open():
                        print("Unable to connect to " + SERVER_HOST + ":" + str(SERVER_PORT))

                if c.is_open():
                    print("Connected to " + SERVER_HOST + ":" + str(SERVER_PORT))
                    regs = c.write_single_register(1000, 0)
                    if regs:
                        print("Value written successful: " + str(regs))

    ser.close()