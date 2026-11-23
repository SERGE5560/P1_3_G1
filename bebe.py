from microbit import *
import radio
radio.on()
radio.config(group=1)


def formatting(T,V):
    return str(T) + "|" + str(len(str(V))) + "|" + str(V)
"""
fonction format
fonction lire le type et retourner le message
"""


def fmt_write(lst) :
    """
        pre : prend en paramètre la liste 'lst'.
        post : Reconstruit le message sous le format de base.
    """
    msg = ""
    for i in range(len(lst) - 1) :
        msg += str(i) + "|"  
    msg += str(lst[len(lst) - 1])
    
    return msg


def fmt_read(fmt) :
    """
        pre : prend le format sous forme de chaine de carractère
        post :retourne une liste contenant les details du format(type, longeur, contenu) dans l'odre
        dans le quel est venu le format
    """
    lst = []
    crt = ""
    fmt1 = str(fmt) + "|"
    for i in fmt1 :
        if i != "|" :
            crt = crt + i
        else :
            lst.append(crt)
            crt = ""
    return lst

def surveiller_bebe(compteur, ancien_etat):
    # 1. 7sab l'ampleur
    x = accelerometer.get_x()
    y = accelerometer.get_y()
    z = accelerometer.get_z()
    ampleur = abs(((x**2 + y**2 + z**2) ** 0.5) - 1000)
    if ampleur > 700:
        compteur += 3
    elif ampleur > 250:
        compteur += 1
    elif compteur > 0:
        compteur -= 1

<<<<<<< HEAD
def fmt_write(lst) :
    """
        pre : prend en paramètre la liste 'lst'.
        post : Reconstruit le message sous le format de base.
    """
    msg = ""
    for i in range(len(lst) - 1) :
        msg += str(i) + "|"  
    msg += str(lst[len(lst) - 1])
    
    return msg


=======
    if compteur > 35:
        compteur = 35

    if accelerometer.was_gesture("freefall"):
        compteur =35
        etat = "TRES_AGITE"
    elif compteur >= 25:
        etat ="TRES_AGITE"
    elif compteur >= 10:
        etat ="AGITE"
    else:
        etat ="ENDORMI"

    if etat != ancien_etat:
        radio.send(formatting("0x03", etat))
        if etat =="ENDORMI":
            music.stop()
            display.clear()
        elif etat =="AGITE":
            display.show(Image.HEART)
            music.play(["C4:4", "E4:4", "G4:4", "E4:4"], wait=False)
        elif etat =="TRES_AGITE":
            display.show(Image.HAPPY)
            music.play(music.ODE, wait=False)

    return compteur, etat
compteur = 0
ancien_etat = ""


    
>>>>>>> f3d0366808b7a7bf0e803321fd281f84436ace93
while True:

    compteur, ancien_etat = surveiller_bebe(compteur, ancien_etat)
    if button_a.was_pressed():
        type_msg = "0x03" 
        contenu="1234:TEST"
        msg_tlv = formatting(type_msg, contenu)  # David a minimiser le code en appelant la fonction formatting
        radio.send(msg_tlv)
        display.show(Image.YES)
        sleep(500)
        display.clear()