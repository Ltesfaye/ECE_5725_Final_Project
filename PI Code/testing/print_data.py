from bluedot.btcomm import BluetoothServer

def data_received(data):
    print(data)
    

s = BluetoothServer(data_received)

_= input("Press Enter to quit...")

s.stop()

