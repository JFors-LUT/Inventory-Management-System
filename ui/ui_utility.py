import os
from PIL import Image, ImageTk
from config import IMAGE_DIR
from tkinter import DISABLED, Label, RAISED, FLAT, messagebox
from tkinter import ttk, Scrollbar, VERTICAL, HORIZONTAL, BOTTOM, RIGHT, BOTH, X, Y

class BaseWindow:
    def setup_window(self, geometry, bg="white", resizable=False, focus=True):
        self.root.geometry(geometry)
        self.root.config(bg=bg)
        self.root.resizable(resizable, resizable)
        if focus:
            self.root.focus_force()

    def set_title(self, module_name):
        self.root.title(f"{module_name} | {self.user}")

    def logout(self):
        print(self.launcher)
        if not msg_manager("Confirm", "Do you really want to logout?", self):
            return

        from modules.login import LoginSystem
        from tkinter import Tk

        self.root.destroy()

        new_root = Tk()
        LoginSystem(new_root, self.launcher)
        new_root.mainloop()
        
               
    def restrict_admin(self, widget):
        if self.user_type != "Admin":
            widget.config(
                state=DISABLED,
                disabledforeground="gray",
                cursor="arrow"
            )

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


def msg_manager(type, msg, self):
    if type == "Error":
        messagebox.showerror("Error", msg, parent=self.root)
        return       
    elif type == "Confirm":
        choice = messagebox.askyesno("Confirm", msg, parent=self.root)
        return choice
    else:
        messagebox.showinfo(type, msg, parent=self.root)
        return

def setup_window(self):
    self.root.geometry("1350x700+110+80")
    self.root.resizable(False, False)
    self.root.config(bg="white")

def format_table(frame, columns, names, widths, show="headings", ):

    newTable = ttk.Treeview(frame, columns=columns, show=show)
    i = 0
    for col in columns:
        newTable.heading(col, text=names[i])
        newTable.column(col, width=widths[i])
        i += 1
    scrolly = Scrollbar(frame, orient=VERTICAL, command=newTable.yview)
    scrollx = Scrollbar(frame, orient=HORIZONTAL, command=newTable.xview)
    newTable.configure(
        yscrollcommand=scrolly.set, 
        xscrollcommand=scrollx.set)
        


    scrollx.pack(side=BOTTOM, fill=X)
    scrolly.pack(side=RIGHT, fill=Y)
    newTable.pack(fill=BOTH, expand=1)        

    return newTable