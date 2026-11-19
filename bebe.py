def fonction(T,V):
    return str(T) + "|" + str(len(str(V))) + "|" + str(V)

#A faire :
"""
fonction format
fonction lire le type et retourner le message


"""
def fmt_read(fmt) :
    """
        pre : prend le format sous forme de chaine de carractère
        post :retourne une liste contenant les details du format(type, longeur, contenu) dans l'odre
    dans le quel est venu le format
    """
    lst = []
    crt = ""
    fmt1 = str(fmt)
    fmt1 = fmt1 + "|"
    for i in fmt1 :
        if i != "|" :
            crt = crt + i
        else :
            lst.append(crt)
            crt = ""
    return lst

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
        sleep(500)
        display.clear()