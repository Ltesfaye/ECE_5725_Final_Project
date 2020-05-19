from bluedot.btcomm import BluetoothServer # used to start bluetooth client server to a callback function
from plotter import Plotter # used to plot and animate things
from multiprocessing import Process, Pipe,Event # used to launch python process on separate core




def bluetooth_client(conn,done_event):
    def data_received(data):
        conn.send(data) # adds data to the queue and leaves

    s = BluetoothServer(data_received)#starts RFCOMM Server

    while True:
        if done_event.wait(0.0001):
            conn.close()
            s.close()


    


def launch_program():
    import time
    st =time.time()
    quit_event = Event()
    parent_conn, child_conn = Pipe()
    p = Process(target=bluetooth_client, args=(child_conn,quit_event))
    p.start()

    while (time.time()-st)<40:
        print(parent_conn.recv())
    
    quit_event.set()
    
    # Wait for the worker to finish
    p.join()