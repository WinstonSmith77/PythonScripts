import requests

import certifi_win32

host='maps.infas-lt.de'
port=443
url = '/maps/05CA1656-C77F-4F11-AD88-724AEFBE79ED/prerelease/'

req = f'https://{host}{url}'


try:
    r = requests.get(req)
except requests.exceptions.RequestException as e:
    print(e)    


print(req)

print(certifi_win32.wincerts.where())