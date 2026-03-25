import os
from tkinter import *
from tkinter import ttk
from db.db_helper import db_connect, run_query
from config import IMAGE_DIR
from ui.ui_utility import load_and_place_images, msg_manager, BaseWindow

from ui.ui_styles import FONT_GENERAL, APP_FONT

#category images
IMG_CAT = os.path.join(IMAGE_DIR, "cat.jpg")
IMG_CATEGORY = os.path.join(IMAGE_DIR, "category.jpg")



class categoryClass(BaseWindow):
    def __init__(self,root):
        self.root=root
        self.setup_window("1100x500+320+220")

        #--------- image data ---------


        #------------ variables -------------
        self.var_cat_id=StringVar()
        self.var_name=StringVar()

        self.init_data()
        self.build_title()
        self.build_input_section()
        self.build_table()
        self.build_images()

        # Initial data load
        self.show()

    def init_data(self):
        self.image_layout = {
            "img1": {"path": IMG_CAT, "pos": (50, 220), "resize": (500, 250), "border": 2, "relief": "raised" },
            "img2": {"path": IMG_CATEGORY, "pos": (580, 220), "resize": (500, 250), "border": 2, "relief": "raised" }
            }

    def build_title(self):
        self.title_lbl = Label(
            self.root,
            text="Manage Product Category",
            font=(APP_FONT, 30),
            bg="#184a45",
            fg="white",
            bd=3,
            relief=RIDGE
        )
        self.title_lbl.pack(side=TOP, fill=X, padx=10, pady=20)

        #------------ category details -------------
    def build_input_section(self):

        self.lbl_mame = Label(self.root, 
            text="Enter Category Name", 
            font=(APP_FONT, 30), 
            bg="white"
        )
        self.lbl_mame.place(x=50, y=100)

        self.txt_mame = Entry(self.root, 
            textvariable=self.var_name, 
            bg="lightyellow", 
            font=(APP_FONT, 18)
        )
        self.txt_mame.place(x=50, y=170, width=300)

        self.add_btn = Button(self.root, 
            text="ADD", 
            command=self.add, 
            font=FONT_GENERAL, 
            bg="#4caf50", 
            fg="white", 
            cursor="hand2"
        )
        self.add_btn.place(x=360, y=170, width=150, height=30)

        self.delete_btn = Button(self.root, 
            text="DELETE", 
            command=self.delete, 
            font=FONT_GENERAL, 
            bg="red", 
            fg="white", 
            cursor="hand2"
        )
        self.delete_btn.place(x=520, y=170, width=150, height=30)

    def build_table(self):
        frame = Frame(self.root, bd=3, relief=RIDGE)
        frame.place(x=700, y=100, width=380, height=100)

        self.CategoryTable = ttk.Treeview(frame, columns=("cid", "name"), show="headings")
        self.CategoryTable.heading("cid", text="C ID")
        self.CategoryTable.heading("name", text="Name")
        self.CategoryTable.column("cid", width=90)
        self.CategoryTable.column("name", width=100)

        # Scrollbars
        scrolly = Scrollbar(frame, orient=VERTICAL, command=self.CategoryTable.yview)
        scrollx = Scrollbar(frame, orient=HORIZONTAL, command=self.CategoryTable.xview)
        self.CategoryTable.configure(yscrollcommand=scrolly.set, xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM, fill=X)
        scrolly.pack(side=RIGHT, fill=Y)
        self.CategoryTable.pack(fill=BOTH, expand=1)

        self.CategoryTable.bind("<ButtonRelease-1>", self.get_data)

    def build_images(self):
        image_layout = {
            "img1": {"path": IMG_CAT, "pos": (50, 220), "resize": (500, 250), "border": 2, "relief": "raised"},
            "img2": {"path": IMG_CATEGORY, "pos": (580, 220), "resize": (500, 250), "border": 2, "relief": "raised"}
        }
        self.images, self.labels = load_and_place_images(self.root, image_layout)

        #-------------------------------------------------- 

    def add(self):
        if self.var_name.get() == "":
            msg_manager("Error","Category Name must be required", self)
            return

        # Check if exist 
        res = run_query(("SELECT * FROM category WHERE name=?", (self.var_name.get(),)), fetch=True)
        if not res["ok"]:
            msg_manager("Error",res["error"], self)
            return
        if res["data"]:
            msg_manager("Error","Category already present", self)
            return

        
        res = run_query(("INSERT INTO category(name) VALUES(?)", (self.var_name.get(),)))
        if not res["ok"]:
            msg_manager("Error",res["error"], self)
            return

        msg_manager("Success", "Category Added Successfully", self)
        self.clear()
        self.show()

    def show(self):
        res = run_query(("SELECT * FROM category", ()), fetch=True)
        
        if not res["ok"]:
            msg_manager("Error",res["error"], self)
            return
        
        self.CategoryTable.delete(*self.CategoryTable.get_children())
        for row in res["data"]:
            self.CategoryTable.insert('', END, values=row)

    
    def clear(self):
        self.var_name.set("")
        self.show()

    def get_data(self,ev):
        f=self.CategoryTable.focus()
        content=(self.CategoryTable.item(f))
        row=content['values']
        self.var_cat_id.set(row[0])
        self.var_name.set(row[1])
    
    def delete(self):
        con = db_connect()
        cur = con.cursor()
        try:
            if self.var_cat_id.get()=="":
                msg_manager("Error","Category name must be required", self)
            else:
                cur.execute("Select * from category where cid=?",(self.var_cat_id.get(),))
                row=cur.fetchone()
                if row==None:
                    msg_manager("Error","Invalid Category Name", self)
                else:
                    op=msg_manager("Confirm", "Do you really want to delete?",self)
                    if op==True:
                        cur.execute("delete from category where cid=?",(self.var_cat_id.get(),))
                        con.commit()
                        msg_manager("Success", "Category Deleted Successfully", self)
                        self.clear()
                        self.var_cat_id.set("")
                        self.var_name.set("")
        except Exception as ex:
            msg_manager("Error",f"Error due to : {str(ex)}")
        finally:
            con.close()



if __name__=="__main__":
    root=Tk()
    obj=categoryClass(root)
    root.mainloop()