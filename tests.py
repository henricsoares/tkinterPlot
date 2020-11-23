import random
from time import sleep
conection = False
while not conection:
    print('Trying to connect...')
    conection = bool(random.getrandbits(1))
    sleep(1)
print(conection)
