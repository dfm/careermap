import requests
import os

def get_dev_key():
    """ from Andy Casey """

    ads_dev_key_filename = os.path.abspath(os.path.expanduser('~/.ads/dev_key'))

    if os.path.exists(ads_dev_key_filename):
        with open(ads_dev_key_filename, 'r') as fp:
            dev_key = fp.readline().rstrip()

        return dev_key

    if 'ADS_DEV_KEY' in os.environ:
        return os.environ['ADS_DEV_KEY']

    raise IOError("no ADS API key found in ~/.ads/dev_key")

def get_author_locations(author):
    response = requests.post('http://adslabs.org/adsabs/api/search/',
                             params={'q':'author:{author}'.format(author=author),
                                     'dev_key':get_dev_key(),
                                     'db_f':'astronomy',
                                     'rows':200,
                                     'fields':'astronomy'})
    J = response.json()
    
    affiliatia = dict([(x.get('year'),aff) for x in J['results']['docs'] 
                                  for aff,auth in 
                                      zip(x.get('aff',[None]*len(x.get('author'))),
                                          x.get('author')) 
                                      if author in auth and aff is not None])

    return affiliatia
