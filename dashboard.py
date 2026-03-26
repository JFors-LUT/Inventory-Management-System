from tkinter import *
from PIL import Image, ImageTk
import time
import sqlite3
import os
from config import IMAGE_DIR, BILL_DIR

from ui.ui_utility import load_image, msg_manager, BaseWindow
from ui.ui_styles import BUTTON_MENU, FONT_TITLE_LBL, MENU_FONT, LABEL_CARD

from db.db_helper import db_connect
from modules.employee import employeeClass
from modules.supplier import supplierClass
from modules.category import categoryClass
from modules.product import productClass
from modules.sales import salesClass



class IMS(BaseWindow):
    def __init__(self, root, user_name, user_type):
        self.root = root
        self.setup_window("1350x700+110+80")
        self.user = user_name
        self.user_type = user_type
        self.set_title("IMS")
        self.launcher = True                    #login flag to identify between dashboard and billing for logout function
        
        self.init_data()
        self.build_header()
        self.build_menu()
        self.build_dashboard()
        self.build_footer()

        self.update_content()

    def init_data(self):
        #dashboard images
        self.IMG_LOGO = os.path.join(IMAGE_DIR, "logo1.png")
        self.IMG_MENU = os.path.join(IMAGE_DIR, "menu_im.png")
        self.IMG_SIDE = os.path.join(IMAGE_DIR, "side.png")

        self.dashboard_cards = {
            "product": {"text": "Total Product\n{ 0 }", "bg": "#607d8b", "pos": (300, 300)},
            "category": {"text": "Total Category\n{ 0 }", "bg": "#009688", "pos": (1000, 120)},
            "employee": {"text": "Total Employee\n{ 0 }", "bg": "#33bbf9", "pos": (300, 120)},
            "supplier": {"text": "Total Supplier\n{ 0 }", "bg": "#ff5722", "pos": (650, 120)},
            "sales": {"text": "Total Sales\n{ 0 }", "bg": "#ffc107", "pos": (650, 300)}
        }

        self.buttons = [
            ("Employee", self.employee),
            ("Supplier", self.supplier),
            ("Category", self.category),
            ("Products", self.product),
            ("Sales", self.sales),
            ("Exit", self.root.destroy)
        ]


    def build_header(self):
        self.icon_title = load_image(self.IMG_LOGO)
        # ------------- title --------------
        self.title_lbl = Label(
            self.root,
            text="Inventory Management System",
            image=self.icon_title,
            compound=LEFT,
            font=FONT_TITLE_LBL,
            bg="#010c48",
            fg="white",
            anchor="w",
            padx=20
        )
        self.title_lbl.place(x=0, y=0, relwidth=1, height=70)

        # ------------ logout button -----------
        self.btn_logout = Button(
            self.root,
            text="Logout",
            command=self.logout,
            font=(MENU_FONT, 15, "bold"),
            bg="yellow",
            cursor="hand2"
        )
        self.btn_logout.place(x=1150, y=10, height=50, width=150)

        # ------------ clock -----------------
        self.lbl_clock = Label(
            self.root,
            text="Welcome to IMS...",
            font=(MENU_FONT, 15),
            bg="#4d636d",
            fg="white"
        )
        self.lbl_clock.place(x=0, y=70, relwidth=1, height=30)

        # ---------------- left menu ---------------
    def build_menu(self):
        frame = Frame(self.root, bd=2, relief=RIDGE, bg="white")
        frame.place(x=0, y=102, width=200, height=565)

        self.MenuLogo = load_image(self.IMG_MENU, (200, 200))
        self.icon_side = PhotoImage(file=self.IMG_SIDE)
        Label(frame, image=self.MenuLogo).pack(side=TOP, fill=X)

        self.lbl_menu = Label(frame, 
            text="Menu", 
            font=(MENU_FONT, 20), 
            bg="#009688"
        )
        self.lbl_menu.pack(side=TOP, fill=X)

        for text, cmd in self.buttons:
            btn = Button(frame, 
                text=text, 
                command=cmd, 
                image=self.icon_side, 
                **BUTTON_MENU
            )
            self.restrict_admin(btn) if text == "Employee" else None
            btn.pack(side=TOP, fill=X)

        # ----------- content ----------------
    def build_dashboard(self):
        self.cards = {}

        for key, config in self.dashboard_cards.items():
            lbl = Label(self.root, text=config["text"], bg=config["bg"], **LABEL_CARD)
            lbl.place(x=config["pos"][0], y=config["pos"][1], height=150, width=300)
            self.cards[key] = lbl

        # ------------ footer -----------------
    def build_footer(self):
        self.lbl_footer = Label(
            self.root,
            text="IMS-Inventory Management System",
            font=(MENU_FONT, 12),
            bg="#4d636d", fg="white"
        )
        self.lbl_footer.pack(side=BOTTOM, fill=X)

    # -------------- functions ----------------
    def employee(self):
        self.new_win = Toplevel(self.root)
        self.new_obj = employeeClass(self.new_win, self.user, self.user_type)

    def supplier(self):
        self.new_win = Toplevel(self.root)
        self.new_obj = supplierClass(self.new_win, self.user, self.user_type)

    def category(self):
        self.new_win = Toplevel(self.root)
        self.new_obj = categoryClass(self.new_win, self.user, self.user_type)

    def product(self):
        self.new_win = Toplevel(self.root)
        self.new_obj = productClass(self.new_win, self.user, self.user_type)

    def sales(self):
        self.new_win = Toplevel(self.root)
        self.new_obj = salesClass(self.new_win, self.user, self.user_type)

    def update_content(self):
        con = db_connect()
        cur = con.cursor()

        try:
            cur.execute("select count (*) from product")
            product = cur.fetchall()
            self.cards["product"].config(text=f"Total Product\n[ {product[0][0]} ]")

            cur.execute("select count (*) from category")
            category = cur.fetchall()
            self.cards["category"].config(text=f"Total Category\n[ {category[0][0]} ]")

            cur.execute("select count (*) from employee")
            employee = cur.fetchall()
            self.cards["employee"].config(text=f"Total Employee\n[ {employee[0][0]} ]")

            cur.execute("select count (*) from supplier")
            supplier = cur.fetchall()
            self.cards["supplier"].config(text=f"Total Supplier\n[ {supplier[0][0]} ]")

            bill = len(os.listdir(BILL_DIR))
            self.cards["sales"].config(text=f"Total Sales\n[ {bill} ]")

            time_ = time.strftime("%I:%M:%S")
            date_ = time.strftime("%d-%m-%Y")
            self.lbl_clock.config(
                text=f"Welcome to Inventory Management System\t\t Date: {date_}\t\t Time: {time_}"
            )
            #con.close()
            self.lbl_clock.after(200, self.update_content)

        except Exception as ex:
            msg_manager("Error",f"Error due to : {str(ex)}", self)
        
        finally:
            con.close()




if __name__ == "__main__":
    from modules.login import LoginSystem

    root = Tk()
    obj = LoginSystem(root)
    root.mainloop()