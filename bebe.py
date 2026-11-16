def fonction(T,V):
    return str(T) + "|" + str(len(str(V))) + "|" + str(V)

#A faire :
"""
fonction format
fonction lire le type et retourner le message


"""
def fmt_read(fmt) :
    """prend le format retourne une liste contenant les details du format(type, longeur, contenu) dans l'odre
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



