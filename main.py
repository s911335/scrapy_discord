import tkinter as tk
from PIL import ImageTk, Image
import requests
from io import BytesIO
from get_information import get_pokemon_data, get_pokemon_location
import time
from tkinter import tix

images =[]

def get_cell (index, pokemon_data) :

    names = locals()

    img_url = pokemon_data['pokemon_pic']
    response = requests.get(img_url)
    img_data = response.content

    img_r = Image.open(BytesIO(img_data))
    img_r = img_r.resize((50, 60))

    img = ImageTk.PhotoImage(img_r)
    images.append(img)

    canvas.create_image(50, 50 + 100 * index, image = img)

    pokemon_name = pokemon_data['pokemon_name']

    canvas.create_text(150, 50 + 100 * index, text = pokemon_name, 
        font=('微軟正黑體 15'), fill = "white")

    pokemon_lv = pokemon_data['pokemon_lv']

    canvas.create_text(250, 50 + 100 * index, text = 'LV  :' + pokemon_lv, 
        font=('微軟正黑體 15'), fill = "white")

    pokemon_cp = pokemon_data['pokemon_cp']

    canvas.create_text(350, 50 + 100 * index, text = 'CP  :' + pokemon_cp, 
        font=('微軟正黑體 15'), fill = "white")

    pokemon_url = pokemon_data['pokemon_url']
    
    names['button%s' % (i)] = tk.Button(win, text = "GPX", font ='微軟正黑體 15', fg = "black")
    names['button%s' % (i)].config(command = lambda : get_pokemon_location(pokemon_url))
    canvas.create_window(450, 50 + 100 * index, window = names['button%s' % (i)])
    
    return None

win=tk.Tk() 
win.title('寶可夢收集IV100飛人程式')


'''
windows framesize = 800 * 600
Don't allow resizing in the x or y direction
'''
win.geometry("520x500")
win.config(bg = "#323232")
win.resizable(0, 0)

frame = tk.Frame(win, width = 500, height = 5000)
frame.grid(row = 0, column = 0)

canvas=tk.Canvas(frame, bg = '#323232', width = 500, height = 500, 
    scrollregion = (0, 0, 500, 5000))
vbar=tk.Scrollbar(frame, orient = tk.VERTICAL)
vbar.pack(side = tk.RIGHT,fill = tk.Y)
vbar.config(command = canvas.yview)

canvas.config(width = 500,height = 500)
canvas.config(yscrollcommand = vbar.set)
canvas.pack(side = tk.LEFT,expand = True,fill = tk.BOTH)


pokemon_array = get_pokemon_data()

for i in range(0, len(pokemon_array)) :
    get_cell(i, pokemon_array[i])


win.mainloop()
