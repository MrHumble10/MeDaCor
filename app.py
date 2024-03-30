from PIL import Image
from colorthief import ColorThief
# import cv2
import colorsys
from flask import Flask, render_template, redirect, url_for, abort, flash, request
import os
from collections import Counter
from werkzeug.utils import secure_filename

app = Flask("__name__")
app.config['SECRET_KEY'] = '123456789'
app.config["UPLOAD_FILE"] = './static/assets/uploaded_img'
NAME = 'uploaded_img'
IMG_FORMAT = ''
NUM_COLORS = 0

@app.route('/', methods=['GET', "POST"])
def home():
    try:
        os.mkdir(f"{os.path.join(os.path.abspath(os.path.dirname('__file__')))}/{app.config['UPLOAD_FILE']}")
    except FileExistsError:
        pass

    if not os.path.isfile(f'./static/assets/img/user_img.jpeg'):
        ct = ColorThief(f'./static/assets/img/img.jpg')
        img_address = f'./static/assets/img/img.jpg'
    else:
        ct = ColorThief(f'./static/assets/img/user_img.jpeg')
        img_address = f'./static/assets/img/user_img.jpeg'

    palette = ct.get_palette(color_count=11, quality=10)

    colors = []

    for color in palette:
        # print(color)
        colors.append(f"{color[0]:02X}{color[1]:02X}{color[2]:02X}")

    if request.method == "POST":
        selected_color = request.form.get('bg-color')
        #
        # from prettytable import PrettyTable
        #
        # # Assuming 'palette' contains the list of dominant colors
        # # total_pixels = image_width * image_height  # Get image dimensions
        # # image_width, image_height = "".join(ct.image.size).split(',')
        # # print(int(image_width)
        # # pt = PrettyTable(['Color', 'Count', 'Percentage'])
        # # for color, count in Counter(palette).items():
        # #     percentage = int(count / total_pixels * 100)
        # #     pt.add_row([color, count, percentage])
        # #
        # # print(pt)
        #

        return render_template('index.html', colors=colors, selected_color=selected_color,
                               img_address=img_address)
    return render_template('index.html', colors=colors,
                           img_address=img_address)


@app.route('/colors', methods=["GET", "POST"])
def color_changer():
    global IMG_FORMAT, NAME, NUM_COLORS
    if 'file' in request.files:
        file = request.files['file']
        NAME, IMG_FORMAT = secure_filename(file.filename).split('.')
        NAME = 'user_img'
        if file:
            file.save(os.path.join(os.path.abspath(os.path.dirname('__file__')),
                                   app.config['UPLOAD_FILE'], f"{NAME}.{IMG_FORMAT}"))

        ct = ColorThief(f'./static/assets/uploaded_img/{NAME}.{IMG_FORMAT}')
        img_address = f'./static/assets/uploaded_img/{NAME}.{IMG_FORMAT}'
        NUM_COLORS = NUM_COLORS = int(request.form['numColor'])
        palette = ct.get_palette(color_count=NUM_COLORS, quality=10)

    # plt.imshow([[palette[i-1] for i in range(30)]])
    # plt.show()
        colors = []
        for color in palette:
            # print(color)
            colors.append(f"{color[0]:02X}{color[1]:02X}{color[2]:02X}")
            # print(colorsys.rgb_to_hls(*color))
            # print(colorsys.rgb_to_hsv(*color))





        try:
            selected_color = request.form.get('bg-color')
        except KeyError:
            selected_color = colors[0]
        return render_template('new_img.html', colors=colors,
                                   selected_color=selected_color,
                                   img_address=img_address, is_selected_color=True)
    print(NUM_COLORS, NAME, IMG_FORMAT)
    ct = ColorThief(f'./static/assets/uploaded_img/{NAME}.{IMG_FORMAT}')
    img_address = f'./static/assets/uploaded_img/{NAME}.{IMG_FORMAT}'

    palette = ct.get_palette(color_count=NUM_COLORS, quality=10)

    # plt.imshow([[palette[i-1] for i in range(30)]])
    # plt.show()
    colors = []
    for color in palette:
        # print(color)
        colors.append(f"{color[0]:02X}{color[1]:02X}{color[2]:02X}")
        # print(colorsys.rgb_to_hls(*color))
        # print(colorsys.rgb_to_hsv(*color))
    selected_color = request.form.get('bg-color')

    return render_template('new_img.html', colors=colors,
                           selected_color=selected_color,
                           img_address=img_address)


# @app.route('/b', methods=["GET", "POST"])
# def n():
#     if request.method == "POST":
#         print(request.form.get('bg-color'))
#     return redirect(url_for('home'))
if __name__ == "__main__":
    app.run(port=5002, debug=True)
