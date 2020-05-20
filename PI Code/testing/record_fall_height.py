from bluedot.btcomm import BluetoothServer

fall_height = 0
def data_received(data):
    global fall_height
    print('fall_height',fall_height)
    temp = data.split(',')
    if(temp[0]=='##'):
        try:
            fall_height = float(temp[2])
        except:
            pass
    

s = BluetoothServer(data_received)

_= input("Press Enter to quit...")

s.stop()
