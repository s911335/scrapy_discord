import tkinter as tk
from scrapy import Scrapy

url = 'https://discord.com/api/v8/channels/259536527221063683/messages?limit=50'

headers = {
    'authority' : 'discord.com',
    'method' : 'GET',
    'path' : '/api/v8/channels/259536527221063683/messages?limit=50',
    'scheme' : 'https',
    'accept' : '*/*',
    'accept-encoding' : 'gzip, deflate, br',
    'accept-language' : 'en-US',
    'authorization' : 'MzgwNDcwNDgwMjIzNzMxNzEy.YEDUPw.9BUz5Jr2aD4HmIrAE5YQC39XHqs',
    'cookie' : '__cfduid=d05d266bf67ce5130d240a5a8b5f87dc11614774528; locale=en-US; _ga=GA1.2.438638126.1614774531; _gid=GA1.2.362112752.1614774531',
    'referer' : 'https://discord.com/channels/252776251708801024/259536527221063683',
    'user-agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_1_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.192 Safari/537.36'
}

location_headers = {
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

class View():
    def __init__(self):
        self.names = locals()
        self.setup_windows()
        self.setup_canvas()
        scrapy = Scrapy(url, headers=headers)
        scrapy.get_pokemon_data()
        self.index = 0
        for pokemon in scrapy.pokemon_array:
            self.get_cells(pokemon)
            self.index += 1
        self.win.mainloop()
        return None

    def setup_windows(self):
        self.win = tk.Tk() 
        self.win.title('寶可夢收集IV100飛人程式')
        self.win.geometry("520x500")
        self.win.config(bg = "#323232")
        self.win.resizable(0, 0)
        return None

    def setup_canvas(self):
        self.frame = tk.Frame(self.win, width = 500, height = 5000)
        self.frame.grid(row = 0, column = 0)
        self.canvas=tk.Canvas(self.frame, bg = '#323232', width = 500,
            height = 500, scrollregion = (0, 0, 500, 5000))
        vbar = tk.Scrollbar(self.frame, orient = tk.VERTICAL)
        vbar.pack(side = tk.RIGHT,fill = tk.Y)
        vbar.config(command = self.canvas.yview)
        self.canvas.config(width = 500, height = 500)
        self.canvas.config(yscrollcommand = vbar.set)
        self.canvas.pack(side = tk.LEFT, expand = True, fill = tk.BOTH)
        return None

    def get_cells(self, pokemon):
        self.canvas.create_image(50, 50 + 100 * self.index, image = pokemon.img)
        self.canvas.create_text(150, 50 + 100 * self.index, text = pokemon.name, 
            font=('微軟正黑體 15'), fill = "white")
        self.canvas.create_text(250, 50 + 100 * self.index, 
            text = 'LV  : ' + pokemon.lv, font=('微軟正黑體 15'), fill = "white")
        self.canvas.create_text(350, 50 + 100 * self.index,
            text = 'CP  : ' + pokemon.cp, font=('微軟正黑體 15'), fill = "white")
        self.names['button%s' % (self.index)] = tk.Button(self.win, text = "GPX",
            font ='微軟正黑體 15', fg = "black")
        self.names['button%s' % (self.index)].config(
            command = lambda : pokemon.get_loction(location_headers))
        self.canvas.create_window(
            450, 50 + 100 * self.index, 
            window = self.names['button%s' % (self.index)])
        return None

if __name__ == '__main__':
    view = View()
