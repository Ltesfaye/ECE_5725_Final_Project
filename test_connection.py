from threading import Thread


class test:

  def __init__(self):
    self.thread = Thread(target=self.print_val)
  
  def print_val(self):
    for _ in range(10):
      print("Hello")
  
  def start(self):
    self.thread.start()

    print('SUPPPPPPPP')

  

ex = test()
ex.start()
  