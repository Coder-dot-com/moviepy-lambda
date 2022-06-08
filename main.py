from datetime import datetime
import math
import random
from moviepy.editor import *
from moviepy import video as v
import os
import pandas
from PIL import Image, ImageDraw, ImageFont


from pathlib import Path

import boto3
import os
import uuid
import traceback





# a .py


from moviepy.editor import *

from PIL import Image, ImageDraw, ImageFont



#Add the text

def wrap_text(text, text_max_width, font):
    text_lines = []
    text_line = []
    text = text.replace('\n', ' [br] ')
    words = text.split()
#As text is same calculate this once and then save the result so ready for next
    longest_line_length = 0

    for word in words:
        if word == '[br]':
            text_lines.append(' '.join(text_line))
            text_line = []
            continue
        text_line.append(word)
        w, h = font.getsize(' '.join(text_line))
        if w > text_max_width:
            text_line.pop()
            text_lines.append(' '.join(text_line))
            text_line = [word]
        
        
        final_line_width, h = font.getsize(' '.join(text_line))
        if final_line_width > longest_line_length:
            longest_line_length = final_line_width

    if len(text_line) > 0:
        text_lines.append(' '.join(text_line))

    return {'text_lines': text_lines, 'longest_line_width': longest_line_length}

def add_phrase(output, size=(1280,720), phrase="test", color="#000000" , stroke_width=0, stroke_fill="#ffffff", phrase_font_path=None,
phrase_font_size=100, wrap=True, right_shift=0, text_vert_position="bottom", mask=None, bg_color="#ffffff", text_alignment="center"):
    image = Image.new(mode='RGBA', size=size, color=0)

    W = int(image.size[0])
    H = int(image.size[1])
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype(phrase_font_path, phrase_font_size)

    text_max_width = int(0.8 * size[0])

    if wrap:
    
        wrapped_text = wrap_text(phrase, text_max_width, font)

        text_to_add  = wrapped_text['text_lines']
        longest_line_width = wrapped_text['longest_line_width']

    else:
        text_to_add = [phrase]
        line_width =  draw.textsize(phrase, font)[0]

    print(text_to_add)


    line_spacing = draw.textsize(text="y", font=font)[1] + 50
    
    total_text_height = line_spacing * len(text_to_add)
    

    line_space = 0
    if text_vert_position == "bottom":
        text_vert_coord = ((H-total_text_height)) * 0.90
    
    elif text_vert_position == "top":
        text_vert_coord = ((H-total_text_height)) * 0.05
    else:
        text_vert_coord = ((H-total_text_height)/2)



    for indx, x in enumerate(text_to_add):

        if text_alignment == "center":
            line_width  = draw.textsize(text=x, font=font)[0]
        else:
            line_width = longest_line_width

        if indx == (len(text_to_add) - 1):
            draw.text((((W-line_width+right_shift)/2), (line_space+text_vert_coord)), x , color, font=font, stroke_width=stroke_width, stroke_fill=stroke_fill)
        else:
            draw.text((((W-line_width)/2), (line_space+text_vert_coord)), x , color, font=font, stroke_width=stroke_width, stroke_fill=stroke_fill)
        
        line_spacing = draw.textsize(text=x, font=font)[1] + 50

        line_space += line_spacing
    # saving the image
    image.save(output)

    w, h = size
    if mask:

        img = Image.open(mask)
        img = img.resize((w,h)) #change so crops centre?
        mask = Image.open(output)

        bg = Image.new("RGBA", (w, h))
        bg.paste(img, (0,0), mask=mask)
        bg.save(output)
    
    if bg_color:
        bg = Image.new("RGBA", (w, h))
        line_space = -10
        for x in text_to_add:

            if text_alignment == "center":
                line_width  = draw.textsize(text=x, font=font)[0] + 20
            else:
                line_width = longest_line_width + 20


            width, height = draw.textsize(text=x, font=font)
            width += 20
            height += 20

            img = Image.new(size=(width, height), mode="RGBA", color=bg_color)
            if indx == (len(text_to_add) - 1):
                bg.paste(img, (int((W-line_width+right_shift)/2), int(line_space+text_vert_coord)))
            else:
                bg.paste(img, (int((W-line_width)/2), int(line_space+text_vert_coord)))
        


            text_img = Image.open(output)
            bg.paste(text_img, (0,0), mask=text_img)
            bg.save(output)
            line_spacing = draw.textsize(text=x, font=font)[1] + 50


            line_space += line_spacing 











# end a.py














     
s3_client = boto3.client('s3')

BASE_DIR = Path(__file__).resolve().parent

csv_file = f"{BASE_DIR}/quotes/inspiration_quotes.csv"

df = pandas.read_csv(csv_file) 
list_of_quotes = df['Quote'].tolist()

list_of_quotes = (list_of_quotes[0:25])

clip_dir=f"{BASE_DIR}/processed_clips"

#Now need to concatenate with fade transition


print('BASE_DIR', BASE_DIR)

def create_video():

    os.chdir(clip_dir)

    total_video_duration=0

    video_clips_list = []


    for item in os.listdir(clip_dir):
        try:
            file_path = os.path.abspath(item)
            print(file_path)
            print(item)
            file_name = (os.path.splitext(item)[0])

            video = VideoFileClip(file_path)
            video.duration
            total_video_duration += video.duration

            print(video.duration, "seconds")
            print("Size:", video.size)

            video = video.resize(newsize=(1280,720))

            video = video.crossfadein(1)
            video = video.crossfadeout(1)


            video_clips_list.append(video)
        except Exception as e:
            print(e)


        # video.write_videofile(f"home/user/Desktop/dev/MoviePyPractise/processed_clips/{file_name}.mp4",fps=25)

    final = concatenate_videoclips(video_clips_list)



    txt_clips = []

    #Here add name 

    name = None

    total_text_duration = 0


    if name:


        for num in range(0,4):
            txt_image_path = f"{BASE_DIR}/tmp/name_{num}.png"
            txt_image_path = f"/tmp/name_{num}.png"

            font_path = f'{BASE_DIR}/maxwell-sans-bold-2022-02-08-22-29-23-utc/Maxwell Sans Bold/MAXWELL_SANS_BOLD.otf'
            font_size = 200

            image = Image.new(mode='RGBA', size=(1,1), color=0)

            draw = ImageDraw.Draw(image)
            font = ImageFont.truetype(font_path, font_size)

            left_shift = (draw.textsize('.', font)[0]) * num 
            # left_shift = 0
            add_phrase(phrase=f"{name}{('.'*num)}", output=txt_image_path, phrase_font_path=font_path, phrase_font_size=font_size, wrap=True, right_shift=left_shift
            , text_alignment='center')
            print("generating name")
            txt_clip = ImageClip(txt_image_path).set_duration(5)
            # txt_clip = (TextClip( f"{name}{('.'*num)}{(' '*(3-num))}",font='Courier-Bold', fontsize=70,color='black', stroke_color='white', stroke_width=3, size=(1200, None), transparent=True, method='caption', align='center').set_duration(7-num) )
            txt_clip = txt_clip.crossfadein(1.0)
            txt_clip = txt_clip.crossfadeout(1.0)
            txt_clip = txt_clip.set_position('center')

            txt_clip = txt_clip.set_start(num)

            total_text_duration += txt_clip.duration

            txt_clips.append(txt_clip)

            os.remove(txt_image_path)
            
        name_clip = CompositeVideoClip(txt_clips)
        txt_clips = [name_clip]

    else:
        txt_clips = []

    def random_quote():

        quote =  (random.choice(list_of_quotes).replace('"', '').replace('”', '').replace('“', '')).split('. ')


        print("random quote after split")
        print([x.capitalize() for x in quote])
        quote = '. '.join([x.capitalize() for x in quote])
        return quote

    font_size = 100
    font_path = f'{BASE_DIR}/skinny-condensed-font-jamie-woods-2022-02-08-22-29-16-utc/jamie_woods_regular.otf'


    texts_added = []

    while total_text_duration < total_video_duration:

        txt_image_path = f"{BASE_DIR}/tmp/text_{total_text_duration}.png"
        txt_image_path = f"/tmp/text_{total_text_duration}.png"

        text_to_add = random_quote()
        print("Text to add")
        print(text_to_add)
        while len(text_to_add) > 250 or text_to_add in texts_added:
            text_to_add = random_quote()


        print("generating text")
        add_phrase(phrase=f"{text_to_add}", output=txt_image_path, phrase_font_path=font_path)
        
        duration = 5 + int(len(text_to_add)/50 * 2.5)
        total_text_duration += duration 

        txt_clip = ImageClip(txt_image_path).set_duration(duration)


        txt_clip = txt_clip.set_position('center')

        texts_added.append(text_to_add)

        txt_clips.append(txt_clip)

        os.remove(txt_image_path)




    txt_clips.pop(-1)
    print(txt_clips)
    extend_last_txt = txt_clips.pop(-1)



    txt_clips = [clip.crossfadein(1.0).crossfadeout(1.0) for clip in txt_clips]
    texts_final = concatenate_videoclips(txt_clips).set_position('center')

    remaining_time = final.duration - texts_final.duration
    extend_last_txt = extend_last_txt.set_duration(remaining_time)

    extend_last_txt = extend_last_txt.crossfadein(1).crossfadeout(3)

    texts_final = concatenate_videoclips([texts_final, extend_last_txt]).set_position('center')
    texts_final = texts_final.subclip(0, final.duration)

    

    audioclip = AudioFileClip(f"{BASE_DIR}/Lost In Nowhere(With Forest SFX).mp3")

    print("texts duration")
    print(texts_final.duration)


    final = CompositeVideoClip([final, texts_final]) # Overlay text on video



    audioclip = CompositeAudioClip([audioclip])


    #Make sure audioclips are correct duration
    audioclips_list = [audioclip]
    while audioclip.duration < final.duration:
        print('audioclip.duration', audioclip.duration)
        audioclips_list.append(audioclip)
        audioclip = concatenate_audioclips(audioclips_list)


    if audioclip.duration >= final.duration:
        audioclip = audioclip.subclip(0, final.duration)


    audioclip = audioclip.audio_fadein(5)
    audioclip = audioclip.audio_fadeout(5)

    print("audio and final duration")
    print(audioclip.duration, final.duration)

    final.audio = audioclip



    # final = final.subclip(final.duration - 2, final.duration)

    final = final.subclip(int(final.duration/2), final.duration)


    print(final.duration)
    print(total_video_duration)

    #try and except this

    os.chdir('/tmp')

    # final = final.subclip(90, 110)
    final.write_videofile("/tmp/final.mp4",fps=20,threads=1024,logger=None,codec="mpeg4",preset="ultrafast",
    ffmpeg_params=['-b:v','10000k'])

    print("finished writing")
def handler(event=None, context=None):
    # for record in event['Records']:
        # bucket = record['s3']['bucket']['name']
        # key = str(record['s3']['object']['key'] )
        try:

            create_video()
            print("Created video")

            s3_client.upload_file('/tmp/final.mp4', '{}'.format("processed-user-videos"), "a.mp4")


        except Exception as b:
                print(" exception", b)
                # print("upload path", upload_path)
                print("traceback output")
                traceback.print_exc()



#Start time

# print(datetime.now())
# handler("", "")
# print(datetime.now())


# video = VideoFileClip("home/user/Desktop/dev/MoviePyPractise/grand-canyon-time-lapse-2022-02-08-22-43-06-utc.mp4").subclip(1,3)

# # Make the text. Many more options are available.
# txt_clip = ( TextClip("My Holidays 2013",fontsize=70,color='white')
#              .set_position('center')
#              .set_duration(10) )

# result = CompositeVideoClip([video, txt_clip]) # Overlay text on video
# result.write_videofile("myHolidays_edited.mp4",fps=25)