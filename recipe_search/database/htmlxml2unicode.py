#!/usr/bin/python

import re
try:
  from htmlentitydefs import name2codepoint
except ImportError:
  name2codepoint = {}


#this function converts a python unicode string 
#to a new python unicode string in which special
#html and xml entities are converterd to their
#xml equivalents

convertHTMLEntities = True
convertXMLEntities = True
#escapeUnrecognizedEntities = True

XML_ENTITIES_TO_SPECIAL_CHARS = { "apos" : "'"
                                  ,
                                  "quot" : '"',
                                  "amp" : "&",
                                  "lt" : "<",
                                  "gt" : ">" }


def convertEntities(match):

  x = match.group(1)
  if convertHTMLEntities and x in name2codepoint:
    return unichr(name2codepoint[x])
  elif x in XML_ENTITIES_TO_SPECIAL_CHARS:
    if convertXMLEntities:
      return XML_ENTITIES_TO_SPECIAL_CHARS[x]
    else:
      return u'&%s;' % x
  elif len(x) > 0 and x[0] == '#':
    # Handle numeric entities
    if len(x) > 1 and x[1] == 'x':
      return unichr(int(x[2:], 16))
    else:
      return unichr(int(x[1:]))
    
  #elif escapeUnrecognizedEntities:
  #  return u'&amp;%s;' % x
  else:
    return u'&%s;' % x


def htmlxml2unicode(text):

  entity_re = re.compile("&(#\d+|#x[0-9a-fA-F]+|\w+);",re.UNICODE)
  return entity_re.sub(convertEntities,text,re.UNICODE)
    
  
