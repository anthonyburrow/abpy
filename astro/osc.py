from urllib.request import urlretrieve
import json


def get_json(sn, save_local=True, destination='./'):
    if sn[:2] == 'SN':
        sn = 'SN%s' % sn.replace(' ', '')

    if destination[-1] != '/':
        destination += '/'

    print('Retrieving data for %s from Open Supernova Catalog...' % sn)

    fn = '%s%s.json' % (destination, sn)

    url = ('https://sne.space/astrocats/astrocats/supernovae/output/json/'
           '%s.json' % sn)
    try:
        urlretrieve(url, fn)
    except Exception:
        print('Error retrieving:\n  %s' % url)
        return

    with open(fn) as F:
        json_data = json.load(F)

    return json_data
