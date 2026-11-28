from microbit import *
import radio
radio.on()
radio.config(group=1)



compteur = 0
ancien_etat = ""

#=======================
#Connection Radio
#========================

radio.on()
radio.config(group=1)


#===================================================
#            Variables Pour envoyer des messages
#===================================================

connexion_established = False
key = "KEYWORD"
connexion_key = None
nonce_list = set()
baby_state = 0
set_volume(100)


##		MINI OS

#============================================
#            Variables Menu
#============================================

options = ["1=OFf", "2=T", "3=H"]
index = 0
allume = False
en_app = False




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


##		LES OPTIONS

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

##		DEDIEE CONNEXION

def formatting(T,V):
    """
    pre: fonction format
    post: fonction lire le type et retourner le message
    """
    return str(T) + "|" + str(len(str(V))) + "|" + str(V)


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


def fmt_write(lst) :
    """
        pre : prend en paramètre la liste 'lst'.
        post : Reconstruit le message sous le format de base.
    """
    msg = ""
    for i in range(len(lst) - 1) :
        msg += str(i) + "|"  
    msg += str(lst[len(lst) - 1])

    compteur = 0
    ancien_etat = ""
    
    return msg

def unpack_data(encrypted_packet, key):
    """
    Déballe et déchiffre les paquets reçus via l'interface radio du micro:bit
    Cette fonction renvoit les différents champs du message passé en paramètre

    :param (str) encrypted_packet: Paquet reçu
           (str) key:              Clé de chiffrement
	:return (srt)type:             Type de paquet
            (int)length:           Longueur de la donnée en caractères
            (str) message:         Données reçue
    """
    packet = vignere(encrypted_packet, key, True)
    packet_split = packet.split("|")
    
    typ = packet_split[0]
    length = packet_split[1]
    message = packet_split[2]
    
    return typ, length, message

def receive_packet(packet_received, key):
    """
    Traite les paquets reçus via l'interface radio du micro:bit
    Cette fonction utilise la fonction unpack_data pour renvoyer les différents champs du message passé en paramètre
    Si une erreur survient, les 3 champs sont retournés vides

    :param (str) packet_received: Paquet reçue
           (str) key:              Clé de chiffrement
	:return (srt)type:             Type de paquet
            (int)lenght:           Longueur de la donnée en caractère
            (str) message:         Données reçue
    """
    try:
       packet = unpack_data(packet_received, key)
    
    except:
        return None
    
    return packet


#Calculate the challenge response
def calculate_challenge_response(challenge):
    """
    Calcule la réponse au challenge initial de connection envoyé par l'autre micro:bit

    :param (str) challenge:            Challenge reçu
	:return (srt)challenge_response:   Réponse au challenge
    """
    try:
        random.seed(int(challenge))
        challenge_response = str(random.randint(10000, 99999))
        return challenge_response
    except:
        return ""
    

def establish_connexion(key):
    """
    Etablissement de la connexion avec l'autre micro:bit
    Si il y a une erreur, la valeur de retour est vide

    :param (str) key:                  Clé de chiffrement
	:return (srt)challenge_response:   Réponse au challenge
    """





##		EXECUTION FINALE
while True:
    
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
    

    compteur, ancien_etat = surveiller_bebe(compteur, ancien_etat)
    if button_a.was_pressed():
        type_msg = "0x03" 
        contenu="1234:TEST"
        msg_tlv = formatting(type_msg, contenu) 
        radio.send(msg_tlv)
        display.show(Image.YES)
        sleep(500)
        display.clear()