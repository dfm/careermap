from astropy.utils.data import get_readable_fileobj
import json
datas = []
rooturl = 'http://bbq.dfm.io/~dfm/nonresearch/careermap/json/'
for fn in """accomazzi,_a.json
allan,_a.json
bauer,_a.json
ginsburg,_a.json
goodman,_a.json
kapadia,_a.json
pepe,_a.json
price-whelan,_a.json
viana,_a.json""".split('\n'):


    with get_readable_fileobj(rooturl+fn) as f:
        data = json.load(f)
        lon,lat = np.array([x['latlng'] for x in data]).T
        year = [x['year'] for x in data]
        size = np.array([np.sum((np.array(lat) == b)*(np.array(lon)==l)) for l,b in np.unique(zip(lon,lat))])
        lon,lat = np.array(np.unique(zip(lat,lon))).T
        L, = plot(lon,lat)
        scatter(lon,lat,s=size*100,c=L.get_color(),alpha=0.3)

