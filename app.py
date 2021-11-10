from logging import debug
from pywebio.output import *
from pywebio.input import *
from pywebio import start_server
from PIL import Image, ImageDraw, ImageFont
from datetime import date

import os, time


def main():
    
    # INPUTS -----------------------------------------------------------------------------------
    put_markdown("# Haas Zoom background generator")

    put_info("""Welcome to the Haas Zoom background generator. \nIf you encounter any problems, shoot me an email to 📧 felipe.gonzalez@berkeley.edu""")

    bg_info = input_group('About you...',[
        input("First name",       name='first_name', placeholder="Pete"), 
        input("Last name",        name='last_name',  placeholder="Johnson"), 
        input("Program and year", name='program',    placeholder=f"FTMBA {date.today().year + 1}")
    ])

    # OUTPUTS ----------------------------------------------------------------------------------
    img1 = generate_background(
        bg_info['first_name'], 
        bg_info['last_name'], 
        bg_info['program'], 
        "bg1.jpg"
    )

    img2 = generate_background(
        bg_info['first_name'], 
        bg_info['last_name'], 
        bg_info['program'], 
        "bg2.png"
    )

    put_text(f"Thanks {bg_info['first_name']}, your Zoom backgrounds are being generated...")
    
    put_processbar('bar')
    for i in range(1,11):
        set_processbar('bar', i/10)
        time.sleep(0.1)

    put_text("Done!")
    put_html('<p style="white-space: pre-wrap;">To save, right click image &rarr; Save image as...</p>')
    put_image(img1)
    put_text(" ")
    put_image(img2)


def generate_background(first, last, program, bg):
    path = f"{os.getcwd()}/{bg}"

    font_bold  = ImageFont.truetype("Roboto-Bold.ttf",  72)
    font_light = ImageFont.truetype("Roboto-Light.ttf", 36)

    try:
        with Image.open(path) as bg:
            d = ImageDraw.Draw(bg)

            d.text((123,125), first,    font=font_bold,  fill=(255,255,255))
            d.text((123,198), last,     font=font_bold,  fill=(255,255,255))
            d.text((123,281), program,  font=font_light, fill=(255,255,255))

            return(bg)

    except OSError:
        print("Cant generate background")


if __name__ == '__main__':
    import argparse
    from pywebio.platform.tornado_http import start_server as start_http_server
    from pywebio import start_server as start_ws_server

    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--port", type=int, default=8080)
    parser.add_argument("--http", action="store_true", default=False, help='Whether to enable http protocol for communicates')
    args = parser.parse_args()

    if args.http:
        start_http_server(main, port=args.port)
    else:
        # Since some cloud server may close idle connections (such as heroku),
        # use `websocket_ping_interval` to  keep the connection alive
        start_ws_server(main, port=args.port, websocket_ping_interval=30)