from email.header import decode_header
import re

def decoder_content(sujet_brut):
    parties = decode_header(sujet_brut)
    sujet_decode = ""
    for texte, encodage in parties:
        if isinstance(texte, bytes):
            sujet_decode += texte.decode(encodage or "utf-8")
        else:
            sujet_decode += texte
    return sujet_decode

def clean_all_links(texte):
    return re.sub(r'https?://\S+', '', texte)