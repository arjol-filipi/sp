from PIL import ImageDraw, ImageFont,Image

import datetime
import qrcode

def krijoNje(name="",poz="",emKom=""):
    image = Image.new('RGB',(1000,620),(255,255,255))
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype("arial.ttf", 15)
    d_date = datetime.datetime.now()
    draw.text((50, 50), str(emKom), fill=('rgb(0,0,0)'), font=font)
    draw.text((50, 250), "Emri: "+name, fill=('rgb(0,0,0)'), font=font)
    draw.text((50, 350), "Pozicioni: "+str(poz), fill=('rgb(0,0,0)'), font=font)
    draw.text((250, 350), "Data e Leshimit"+d_date.strftime("%m/%d/%Y"), fill=('rgb(0,0,0)'), font=font)
    image.save(str(name)+".png")
    img = qrcode.make(str(name))
    img.save(str(name)+".bmp")
    return img
    til = Image.open(str(name)+".png")
    im = Image.open(str(name)+".bmp")
    im = im.resize((300,300),PIL.Image.ANTIALIAS)
    til.paste(im,(600,350))
    til.save(name+'.png')
    
    return name+'.png'
