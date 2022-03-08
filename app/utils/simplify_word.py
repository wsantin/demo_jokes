import re, string
from unicodedata import normalize

def delete_diacritics(word):
    # -> NFD y eliminar diacríticos
    if word==None:
        word=''
    word = re.sub(
            r"([^n\u0300-\u036f]|n(?!\u0303(?![\u0300-\u036f])))[\u0300-\u036f]+", r"\1", 
            normalize( "NFD", word), 0, re.I
        )
    # -> NFC
    word = normalize( 'NFC', word)

    return( word )

def delete_punctuation ( text ):
  return re.sub('[%s]' % re.escape(string.punctuation), '', text)

def filter_only_letters_lowercase(word):
    """
    Esta funcion filta el string pasado devolviendo 
    
    solo las letras en minusculas y la ñ

    imputs:

        - word : String
    return:
        - String
    """

    wordTwo = ''
    for i in word:
        if (97<=ord(i)<=122) or (ord(i)==241):
            wordTwo = wordTwo + i

    return( wordTwo )