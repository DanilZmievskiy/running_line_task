from django.shortcuts import render
from django.http import FileResponse
from django.templatetags.static import static
from django.conf import settings

import os
import cv2
from PIL import ImageFont, ImageDraw, ImageColor, Image
import numpy as np


FONT_PATH = str(settings.BASE_DIR) + static('font/Arial.ttf')

def index(request):
    return render(request, "index.html")


def video_download(request):
    if request.method == "POST":
        text = request.POST['line_text']
        text_color = request.POST['text_color']
        bg_color = request.POST['bg_color']
        
        filename = create_running_line_video(text.strip(), text_color, bg_color)

        response =  FileResponse(open(filename, 'rb'), as_attachment=True, content_type='video/webm')
        os.remove(filename)

        return response


def create_running_line_video(text, text_color, bg_color, output_file = "running_line.mp4"):
    image_width=100
    image_height=100

    font_size = 64
    text_color = ImageColor.getcolor(text_color, "RGB")
    bg_color = ImageColor.getcolor(bg_color, "RGB")
    print(settings.BASE_DIR)
    print(FONT_PATH)

    font = ImageFont.truetype(FONT_PATH, font_size)
    text_width, text_height = font.getsize(text)

    num_frames = text_width + image_width

    fps = num_frames // 3

    rnd_key = np.random.randint(1000)
    output_file = settings.MEDIA_ROOT + '/running_line_' + str(rnd_key) + '.mp4'

    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    video_writer = cv2.VideoWriter(output_file, fourcc, fps, (image_width, image_height))

    for i in range(num_frames + 1):
        img = Image.new("RGB", (image_width, image_height), bg_color)
        draw = ImageDraw.Draw(img)

        x = image_width - i
        y = (image_height - text_height) // 2

        draw.text((x, y), text, font=font, fill=text_color)

        frame = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)

        video_writer.write(frame)

    video_writer.release()

    return output_file