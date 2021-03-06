import requests
import json
from bs4 import BeautifulSoup
from PIL import ImageTk, Image
from io import BytesIO

class Scrapy():
    def __init__(self, url, headers):
        self.response = requests.get(url, headers=headers)
        self.pokemon_array = []
        return None

    class Pokemon():
        def __init__(self, dic):
            data = dic["content"]
            data = data.split('\n')
            self.name = data[0].split('**')[1]
            self.number = data[0].split('<a:')[1].split(':')[1].split('>')[0]
            self.iv = data[0].split('IV')[1].split(' ')[0]
            self.cp = ' ' + data[0].split('**')[3].split('CP')[1]
            self.lv = ' ' + data[0].split('**')[5].split('L')[1]
            self.url = dic["embeds"][0]["description"].split('(')[1].split(')')[0]
            self.pic = 'https://cdn.discordapp.com/emojis/' + self.number + '.png?v=1'
            self.img = self.get_img()
            self.latitude = ''
            self.longitude = ''
            
        def get_img(self):
            pic_url = 'https://cdn.discordapp.com/emojis/' + self.number + '.png?v=1'
            response = requests.get(pic_url)
            img_data = response.content
            img_r = Image.open(BytesIO(img_data))
            img_r = img_r.resize((50, 50))
            img = ImageTk.PhotoImage(img_r)
            return img
        
        def get_loction(self, headers):
            request = requests.get(self.url, headers = headers)
            bs = BeautifulSoup(request.text, 'html.parser')
            location = str(bs.find_all('a')[1])
            self.latitude = location.split('lat=')[1].split('&amp')[0]
            self.longitude = location.split('lng=')[1].split('"')[0]
            self.write_gpx()
            return None

        def write_gpx(self):
            the_file = open("scrapy_result.gpx", 'w') 
            the_file.write('<?xml version="1.0"?>\n' +
                '<gpx version="1.1" creator="Xcode" >\n' +
                '<wpt lat=' + '"' + self.latitude + '"\n' +
                'lon=' + '"' + self.longitude + '"\n' +
                ' >\n' +
                '<name>Cupertino</name> \n' +
                '<time>2014-09-24T14:55:37Z</time>\n' +
                '</wpt>\n' +
                '</gpx>'
                )
            the_file.close()
            return None

    def get_pokemon_data(self):
        for dic in self.response.json():
            pokemon = self.Pokemon(dic)
            self.pokemon_array.append(pokemon)   
        return None

