

import json
import pprint




def ana_json(data):
    '''Analyze Json get album song details'''
    j=json.load(data)
    # pprint.pprint(j)
    adict = {}
    adict['cover'] = j['album']['picUrl']
    adict['number'] = j['album']['size']
    adict['albumname'] = j['album']['name']
    adict['artist'] = j['album']['artist']['name']
    for s in j['album']['songs']:
        sdict = {}
        sdict['id'] = s['id']
        sdict['songname'] = s['name']
        artists = []         
        for x in s['artists']:
            artists.append(x['name'])
        sdict['singer'] = ','.join(artists)
        # print(sdict)
        adict[s['no']] = sdict
    pprint.pprint(adict)
    return adict




    


if __name__ == "__main__":
    
    with open(r'M:\GH\xd\t.json','r',encoding='utf8') as f:
        ana_json(f)