#%%
import requests
import json
from urllib.request import urlopen
from bs4 import BeautifulSoup
import os

def get_pokemon_data() :

    pokemon_array = {}

    requests_url = 'https://discord.com/api/v8/channels/259536527221063683/messages?before=816653473776009241&limit=50'

    requests_headers = {
        'authority' : 'discord.com',
        'method' : 'GET',
        'path' : '/api/v8/channels/259536527221063683/messages?limit=50',
        'scheme' : 'https',
        'accept' : '*/*',
        'accept-encoding' : 'gzip, deflate, br',
        'accept-language' : 'en-US',
        'authorization' : 'MzgwNDcwNDgwMjIzNzMxNzEy.YD-HSQ.mPgoYWY8i7GmBTeFj0jCF7ANijU',
        'cookie' : '__cfduid=d05d266bf67ce5130d240a5a8b5f87dc11614774528; locale=en-US; _ga=GA1.2.438638126.1614774531; _gid=GA1.2.362112752.1614774531',
        'referer' : 'https://discord.com/channels/252776251708801024/259536527221063683',
        'user-agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_1_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.192 Safari/537.36'
    }

    response = requests.get(requests_url, headers = requests_headers)

    response_pokemon = response.json()

    for i in range(0, len(response_pokemon)):
        
        data = response_pokemon[i]["content"]
        pokemon_data = data.split('\n')
        pokemon_name = pokemon_data[0].split('**')[1]
        pokemon_number = pokemon_data[0].split('<a:')[1].split(':')[0]
        pokemon_iv = pokemon_data[0].split('IV')[1].split(' ')[0]
        pokemon_cp = pokemon_data[0].split('**')[3]
        pokemon_lv = pokemon_data[0].split('**')[5]
        pokemon_url = response_pokemon[i]["embeds"][0]["description"].split('(')[1].split(')')[0]
        pokemon_pic_url_num = (
            pokemon_data[0].split('<a:')[1].split(':')[1].split('>')[0]
            )
        pokemon_pic_url = ('https://cdn.discordapp.com/emojis/' +
            pokemon_pic_url_num + '.png?v=1')
        
        pokemon_array[i] = {
            'pokemon_name' : pokemon_name, 
            'pokemon_number' : pokemon_number, 
            'pokemon_iv' : pokemon_iv, 
            'pokemon_cp' : pokemon_cp,
            'pokemon_lv' : pokemon_lv, 
            'pokemon_url' : pokemon_url,
            'pokemon_pic' : pokemon_pic_url
            }
    return pokemon_array
    
def get_pokemon_location(pokemon_url) :
    
    pokemon_headers = {
        'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding' : 'gzip, deflate',
        'Accept-Language' : 'en-US,en;q=0.9',
        'Cache-Control' : 'max-age=0',
        'Connection' : 'keep-alive',
        'Cookie' : 'sessionid=mpwumnnza7zan8807pwu41mw1s0lwffk; csrftoken=w1xhSG0xEMDPmHTw4XEiruwjjwvcDC1wYBJtdsPbAncg2Rc7BiOodUluXxvLF1YL',
        'Host' : 'api.pokedex100.com',
        'Upgrade-Insecure-Requests' : '1',
        'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_1_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.192 Safari/537.36'
    }

    request = requests.get(pokemon_url, headers = pokemon_headers)
    bs = BeautifulSoup(request.text, 'html.parser')
    location = str(bs.find_all('a')[1])
    location_latitude = location.split('lat=')[1].split('&amp')[0]
    location_longitude = location.split('lng=')[1].split('"')[0]

    the_file = open(os.path.expanduser("scrapy_result.gpx"), 'w') 
    the_file.write('<?xml version="1.0"?>\n' +
            '<gpx version="1.1" creator="Xcode" >\n' +
                    '<wpt lat=' + '"' + str(location_latitude) + '"\n' +
                        'lon=' + '"' + str(location_longitude) + '"\n' +
                        ' >\n' +
                    '<name>Cupertino</name> \n' +
                '<time>2014-09-24T14:55:37Z</time>\n' +
            '</wpt>\n' +
            '</gpx>'
        )
    the_file.close()
    
    return None


pokemon_array = get_pokemon_data()


#%%
