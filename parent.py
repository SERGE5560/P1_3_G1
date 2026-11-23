from microbit import *
import radio
radio.on()
radio.config(group=1)

options = ["1=OFf", "2=T", "3=H"]  # T = Température, H = Cœur, OFF = Éteint
index = 0
allume = False
en_app = False

# Début mini os Par David

def allumer_progressif():
    for lum in range(0, 10):
        ligne = str(lum) * 5
        display.show(Image(":".join([ligne] * 5)))
        sleep(80)


def eteindre_progressif():
    for lum in range(9, -1, -1):
        ligne = str(lum) * 5
        display.show(Image(":".join([ligne] * 5)))
        sleep(80)
    display.clear()


def allumer():
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
    global allume, en_app
    if allume:
        eteindre_progressif()
    allume = False
    en_app = False
    display.off()


def afficher_menu():
    display.clear()
    display.show(options[index])


def option_suivante():
    global index
    index = (index + 1) % len(options)
    afficher_menu()


def lancer_option():
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
    global en_app
    en_app = False
    afficher_menu()


# Démarre éteint (en attente d'un appui sur A) 
allume = False
en_app = False
display.off()

while True:
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

# Fin mini os

"""
while True:
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
            
"""