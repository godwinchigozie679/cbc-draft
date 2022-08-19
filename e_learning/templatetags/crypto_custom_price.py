from django import template
# Import for Cryptomarketcoinprice
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
from django.http import HttpResponse

import urllib.request
key = 'ab2b809bc5eeffc128f9d71326b3f4221e0b4d7d'


from django.template.loader import get_template
register = template.Library()

@register.inclusion_tag('crypto_price.html')
def show_crypto_price(count=10):
        
    # Crypto Currency Price
    try:
        url = "https://api.nomics.com/v1/currencies/ticker?key=b4a97e16f02c5a43372986e90650f1145742d7b5&interval=1h,&convert=USD&per-page=1-1000&page=1&rank=rank&status=active"
               
        crypto_datas = urllib.request.urlopen(url).read()
        data = json.loads(crypto_datas.decode('utf-8'))[:count]    
        
    except:
        return HttpResponse('Your Internet connection is probably off....')
    ######################################################
    
    return {'data': data }





