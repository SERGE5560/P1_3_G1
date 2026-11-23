from microbit import *
import radio
radio.on()
radio.config(group=1)
while True:
    doses_lait = gerer_lait(doses_lait)
    message_recu =radio.receive()
    if message_recu:
        parties =message_recu.split("|")
        if len(parties) == 3:
            type_msg=parties[0]
            longueur=parties[1]
            contenu=parties[2]
            
            display.scroll("T:" + type_msg)
            display.scroll("L:" + longueur)
            display.scroll("C:" + contenu)