from PIL import Image, ImageDraw, ImageFont

font = ImageFont.truetype("/home/user/Desktop/dev/MoviePyPractise/skinny-condensed-font-jamie-woods-2022-02-08-22-29-16-utc/jamie_woods_bold.otf", size=50)


text = "MY TEXT"
mask = Image.new("RGBA", (400,100))

canvas_size = (ImageDraw.Draw(mask).textsize( text, font=font))

mask = Image.new("RGBA", canvas_size)

mdr = ImageDraw.Draw(mask)

mdr.text((0,0), text, fill=(255,255,255,255), font=font)
# print(mdr.textsize( text, font=font))
img = Image.open("/home/user/Desktop/dev/MoviePyPractise/banner.jpg")

w, h = canvas_size
img = img.crop((0,0,w,h)) #change so crops centre


bg = Image.new("RGBA", canvas_size)
bg.paste(img, (0,0), mask=mask)


bg.save("aa.png")
