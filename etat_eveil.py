from microbit import *

etat = 0
while True:
    
    while etat == 0 :
        if microphone.current_event() == SoundEvent.LOUD :
            etat = 1
        display.show (etat)
        sleep(2000)
        display.clear()