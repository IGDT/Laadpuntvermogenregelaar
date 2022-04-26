#schrijven van waarde 8 ampère naar register 1000
from pyModbusTCP.client import ModbusClient
import time

SERVER_HOST = "10.0.0.182"
SERVER_PORT = 502

c = ModbusClient()

c.host(SERVER_HOST)
c.port(SERVER_PORT)

while True:
    # open or reconnect TCP to server
    if not c.is_open():
        if not c.open():
            print("unable to connect to "+SERVER_HOST+":"+str(SERVER_PORT))

    # if open() is ok, read register (modbus function 0x03)
    if c.is_open():
        # read 10 registers at address 1000, store result in regs list
        print("connected to "+SERVER_HOST+":"+str(SERVER_PORT))
        regs = c.write_single_register(1000,8)
        if regs:
            print("Value written successful: "+str(regs))
    time.sleep(3)


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