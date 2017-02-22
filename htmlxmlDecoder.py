

from UnicodeDammit import UnicodeDammit as ud

def htmlDecoder(text, overrideEncodings=[]):

    #consider instead returning a UnicodeDammit object with variables
    #dammit.unicode,
    #dammit.originalEncoding,
    #dammit.declaredHTMLEncoding

    if isinstance(text, unicode):
        return text
    else:

        dammit = ud(text, overrideEncodings,smartQuotesTo='html',isHTML=True )
        return dammit.unicode, dammit.originalEncoding, dammit.declaredHTMLEncoding



def xmlDecoder(text, overrideEncodings=[]):
    
    if isinstance(text, unicode):
        return text
    else:
        dammit = ud(text, overrideEncodings,smartQuotesTo='html',isHTML=True )
        return dammit.unicode


