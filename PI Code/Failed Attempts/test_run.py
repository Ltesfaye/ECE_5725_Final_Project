from multiprocessing import Process, Pipe
import time

def f(conn):
    time.sleep(2)
    conn.send([41, None, 'hello'])
    conn.send([42, None, 'hello'])
    conn.send([43, None, 'hello'])   
    conn.close()

def hang_wait():
    _= input("")
if __name__ == '__main__':
    parent_conn, child_conn = Pipe()
    st = time.time()
    p = Process(target=f, args=(child_conn,))
    p.start()
    hang_wait()
    for i in range(3):
        print(parent_conn.recv(), time.time()-st)   # prints "[42, None, 'hello']"
    
    p.join()
    