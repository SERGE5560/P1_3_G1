from microbit import *
import radio
radio.on()
radio.config(group=1)
while True:
    if button_a.was_pressed():
        type_msg = "0x03" 
        contenu = "1234:TEST" 
        longueur = len(contenu)
        
        msg_tlv = str(type_msg) + "|" + str(longueur) + "|" + contenu
        
        radio.send(msg_tlv)
        display.show(Image.YES)