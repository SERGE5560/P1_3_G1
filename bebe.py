from microbit import *
import radio
radio.on()
radio.config(group=1)



compteur = 0
ancien_etat = ""


##		MINI OS

options = ["1=OFf", "2=T", "3=H"]
index = 0
allume = False
en_app = False

connexion_established = False
key = "KEYWORD"
connexion_key = None
nonce_list = set()
baby_state = 0
set_volume(100)




def allumer_progressif():
    """
    pre: _
    post: s'occupe de simuler un allumage à intensité progressive de LEDs du microbit
    """
    for lum in range(0, 10):
        ligne = str(lum) * 5
        display.show(Image(":".join([ligne] * 5)))
        sleep(80)


def eteindre_progressif():
    """
    pre: _
    post: s'occupe de simuler une instinstion à intensité dégressive de LEDs du microbit
    """
    for lum in range(9, -1, -1):
        ligne = str(lum) * 5
        display.show(Image(":".join([ligne] * 5)))
        sleep(80)
    display.clear()


def allumer():
    """
    pre: il set les drapeaux liés à l'allumage et au menu   
    post: s'occupe de l'allumage complet des LEDs du micobit et de l'affichage du menu
    """
    global allume, index, en_app
    allume = True
    en_app = False
    index = 0
    display.on()
    allumer_progressif()
    sleep(1000)
    display.show(Image.HAPPY)
    sleep(2000)
    afficher_menu()


def eteindre():
    """
    pre: il set les drapeaux liés à l'allumage et au menu   
    post: s'occupe de l'instinction complet des LEDs du micobit
    """
    global allume, en_app
    if allume:
        eteindre_progressif()
    allume = False
    en_app = False
    display.off()


def afficher_menu():
    """
    pre: prend le options qui sont dans la liste "option"  
    post: s'occupe de l'affichage de ces option
    """
    display.clear()
    display.show(options[index])


def option_suivante():
    """
    pre: _   
    post: s'occupe du passage d'une option à une autre
    """
    global index
    index = (index + 1) % len(options)
    afficher_menu()


def lancer_option():
    """
    pre: _   
    post: il permet de lanncer l'option courant
    """
    global en_app
    choix = options[index]

    if choix == "1=OFf":
        eteindre()
    elif choix == "2=T":
        en_app = True
        display.clear()
        display.scroll(str(temperature()) + "C", wait=False, delay=120)
    elif choix == "3=H":
        en_app = True
        display.clear()
        display.show(Image.HEART)


def retour_menu():
    """
    pre: _   
    post: il permet de quitter de l'interieur d'une option vers le menu
    """
    global en_app
    en_app = False
    afficher_menu()


##		ORIENTE CONNECTION

def formatting(T,V):
    """
    pre: fonction format
    post: fonction lire le type et retourner le message
    """
    return str(T) + "|" + str(len(str(V))) + "|" + str(V)


def fmt_write(lst) :
    """
        pre : prend en paramètre la liste 'lst'.
        post : Reconstruit le message sous le format de base.
    """
    msg = ""
    for i in range(len(lst) - 1) :
        msg += str(lst[i]) + "|"  
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

<<<<<<< HEAD
##		LES OPTIONS
=======
>>>>>>> e03687cd0f9316ba99fb1fd71de361908e5dd917

def surveiller_bebe(compteur, ancien_etat):
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
=======
<<<<<<< Updated upstream

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
=======
>>>>>>> Stashed changes
>>>>>>> e03687cd0f9316ba99fb1fd71de361908e5dd917
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
=======
compteur = 0
ancien_etat = ""
>>>>>>> e03687cd0f9316ba99fb1fd71de361908e5dd917
    
    return msg


##		EXECUTION FINALE
while True:
<<<<<<< Updated upstream
    
# Démarre éteint (en attente d'un appui sur A)
    if not allume:
        if button_a.was_pressed():
            allumer()

    elif en_app:
        if accelerometer.was_gesture("shake") or (button_a.is_pressed() and button_b.is_pressed()):
            retour_menu()
            sleep(200)

    else:
        if button_a.was_pressed():
            option_suivante()
        elif button_b.was_pressed():
            lancer_option()

    sleep(50)
    

=======
>>>>>>> Stashed changes
    compteur, ancien_etat = surveiller_bebe(compteur, ancien_etat)
    if button_a.was_pressed():
        type_msg = "0x03" 
        contenu="1234:TEST"
        msg_tlv = formatting(type_msg, contenu) 
        radio.send(msg_tlv)
        display.show(Image.YES)
        sleep(500)
        display.clear()