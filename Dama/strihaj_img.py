from PIL import Image, ImageTk

def strihaj(meno_suboru, ps, pr=1):
    obr = Image.open(meno_suboru)
    sir, vys = obr.width//ps, obr.height//pr
    #zoz = []
    i = 0
    for y in range(0, obr.height, vys):
        for x in range(0, obr.width, sir):
            #zoz.append(ImageTk.PhotoImage(obr.crop((x, y, x+sir, y+vys))))
            obr = obr.crop((x, y, x+sir, y+vys))
            i = i + 1
            obr.save(f'obrazky/piece{i}.png')
    #return zoznam
    
def return_transparent_img(obr):
        #transparent_color = obr.getpixel((0,0))
        datas = obr.getdata()
        
        new_data = []
        for item in datas:
            if item[0] >= 240 and item[1] >= 240 and item[2] >= 240:
                # replacing it with a transparent value 
                new_data.append((255, 255, 255, 0)) 
            else: 
                new_data.append(item) 
        obr.putdata(new_data)
        
        return obr

#obr = Image.open('obrazky/tcierna_dama.png')
#obr = return_transparent_img(obr)
#obr.save('obrazky/tcierna_dama.png')