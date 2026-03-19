import os
from PIL import Image, ImageTk
from config import IMAGE_DIR
from tkinter import Label, RAISED, FLAT

def load_image(image_path, size=None):
    image = Image.open(image_path)
    if size:
        image = image.resize(size)
    return ImageTk.PhotoImage(image)

def create_image_label(root, image, x, y, bd, relief=FLAT):
    lbl = Label(root, image=image, bd=bd, relief=relief)
    lbl.place(x=x, y=y)
    return lbl

def load_and_place_images(root, image_layout):
    images = {}
    labels = {}
    for key, config in image_layout.items():
        img = load_image(config["path"], config["resize"])
        lbl = create_image_label(
            root,
            img,
            config["pos"][0],
            config["pos"][1],
            config.get("border", 2),
            relief=config.get("relief")
        )
        images[key] = img     
        labels[key] = lbl
    return images, labels