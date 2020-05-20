from multiprocessing import Process,Event
from bluedot.btcomm import BluetoothServer #start bluetooth server to allow phone to connect



def bluetooth_client(done_event):
    
    def data_received(data):
        print(data) # adds data to the queue and leaves

    s = BluetoothServer(data_received)#starts RFCOMM Server
    
    while not(done_event.wait(0.00001)):
        pass
       
    
    s.stop()
           

quit_event = Event()
p = Process(target=bluetooth_client, args=(quit_event))
_ = input("Hit enter to quit ...")
p.join()
