from plotter import Plotter # used to plot and animate things
from multiprocessing import Process, Pipe,Event # used to launch python process on separate core




def bluetooth_client(conn,done_event):
    from bluedot.btcomm import BluetoothServer #start bluetooth client server 
    def data_received(data):
        conn.send(data) # adds data to the queue and leaves

    s = BluetoothServer(data_received)#starts RFCOMM Server
    
    # running = True # used to terminate this process

    while not(done_event.wait(0.00001)):
        pass
       
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
    
    print("Connection QUITTED")
    
    quit_event.set()
    
   
    # Wait for the worker to finish
    p.join()

    print("done")

launch_program()