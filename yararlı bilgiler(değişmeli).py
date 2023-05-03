buyukAlfabe = "ABCÇDEFGĞHIİJKLMNOÖPRSŞTUÜVYZ"
kucukAlfabe = "abcçdefgğhıijklmnoöprsştuüvyz"
#verilen komut içerisindeki büyük harfleri(varsa) bulup küçük harfe çeviriyoruz

def lower(command:str):
    newText = str()
    for i in command:
        if i in command:
            if i in buyukAlfabe:
                index = buyukAlfabe.index(i)
                newText += kucukAlfabe[index]
            else:
                newText += i
    return newText
