from tkinter import *
import os
from config import IMAGE_DIR, BILL_DIR
from ui.ui_utility import msg_manager, BaseWindow, load_and_place_images
from ui.ui_styles import FONT_GENERAL, FONT_SALES_BTN, APP_FONT

#sales images
IMG_CAT2 = os.path.join(IMAGE_DIR, "cat2.jpg")

class salesClass(BaseWindow):
    def __init__(self, root):
        self.root = root
        self.setup_window("1100x500+320+220")
        #--------- image data ------
        self.image_layout = {
            "img1": {"path": IMG_CAT2, "pos": (700, 110), "resize": (450, 300), 
                     "border": 0, "relief": "flat" },
  }
        self.init_vars()
        self.build_title()
        self.build_search()
        self.build_list()
        self.build_bill_area()
        self.build_images()

        self.show()


    # ---------------- INIT ----------------

    def init_vars(self):
        self.bill_list = []
        self.var_invoice = StringVar()
        
    # ---------------- UI ----------------
    def build_title(self):
        self.lbl_title = Label(
            self.root,
            text="View Customer Bills",
            font=(APP_FONT, 30),
            bg="#184a45",
            fg="white",
            bd=3,
            relief=RIDGE
        )
        self.lbl_title.pack(side=TOP, fill=X, padx=10, pady=20)

    def build_search(self):
        lbl_invoice = Label(self.root, text="Invoice No.", font=FONT_GENERAL, bg="white").place(x=50, y=100)

        txt_invoice = Entry(self.root, textvariable=self.var_invoice,
              font=FONT_GENERAL, bg="lightyellow").place(x=160, y=100, width=180, height=28)

        btn_search = Button(self.root, text="Search", command=self.search,
               font=FONT_SALES_BTN, bg="#2196f3",
               fg="white", cursor="hand2").place(x=360, y=100, width=120, height=28)

        btn_clear = Button(self.root, text="Clear", command=self.clear,
               font=FONT_SALES_BTN, bg="lightgray",
               cursor="hand2").place(x=490, y=100, width=120, height=28)

    def build_list(self):
        frame = Frame(self.root, bd=3, relief=RIDGE)
        frame.place(x=50, y=140, width=200, height=330)

        scrolly = Scrollbar(frame, orient=VERTICAL)

        self.Sales_List = Listbox(
            frame,
            font=FONT_GENERAL,
            bg="white",
            yscrollcommand=scrolly.set
        )

        scrolly.config(command=self.Sales_List.yview)
        scrolly.pack(side=RIGHT, fill=Y)
        self.Sales_List.pack(fill=BOTH, expand=1)

        self.Sales_List.bind("<ButtonRelease-1>", self.get_data)

    def build_bill_area(self):
        frame = Frame(self.root, bd=3, relief=RIDGE)
        frame.place(x=280, y=140, width=410, height=330)

        Label(
            frame,
            text="Customer Bill Area",
            font=(APP_FONT, 20),
            bg="orange"
        ).pack(side=TOP, fill=X)

        scrolly = Scrollbar(frame, orient=VERTICAL)

        self.bill_area = Text(
            frame,
            bg="lightyellow",
            yscrollcommand=scrolly.set
        )

        scrolly.config(command=self.bill_area.yview)
        scrolly.pack(side=RIGHT, fill=Y)
        self.bill_area.pack(fill=BOTH, expand=1)

    def build_images(self):
        self.images, self.labels = load_and_place_images(self.root, self.image_layout)


    # -------------------------------------------------------
    def show(self):
        del self.bill_list[:]
        self.Sales_List.delete(0, END)

        for i in os.listdir(BILL_DIR):
            if i.split('.')[-1] == 'txt':
                self.Sales_List.insert(END, i)
                self.bill_list.append(i.split('.')[0])

    def get_data(self, ev):
        index_ = self.Sales_List.curselection()
        if not index_:
            return

        file_name = self.Sales_List.get(index_)
        self.bill_area.delete('1.0', END)

        file_path = os.path.join(BILL_DIR, file_name)
        with open(file_path, 'r') as fp:
            for i in fp:
                self.bill_area.insert(END, i)

    def search(self):
        if self.var_invoice.get() == "":
            msg_manager("Error", "Invoice no. should be required", self)
        else:
            if self.var_invoice.get() in self.bill_list:
                file_path = os.path.join(BILL_DIR, f"{self.var_invoice.get()}.txt")
                self.bill_area.delete('1.0', END)

                with open(file_path, 'r') as fp:
                    for i in fp:
                        self.bill_area.insert(END, i)
            else:
                msg_manager("Error", "Invalid Invoice No.", self)

    def clear(self):
        self.show()
        self.bill_area.delete('1.0', END)


if __name__ == "__main__":
    root = Tk()
    obj = salesClass(root)
    root.mainloop()
