import os
from tkinter import *
from PIL import Image,ImageTk
from tkinter import ttk,messagebox
import sqlite3
from data.db.db_helper import db_connect
from config import IMAGE_DIR
from ui.ui_utility import load_and_place_images

from ui.ui_styles import FONT_GENERAL, APP_FONT

#category images
IMG_CAT = os.path.join(IMAGE_DIR, "cat.jpg")
IMG_CATEGORY = os.path.join(IMAGE_DIR, "category.jpg")



class categoryClass:
    def __init__(self,root):
        self.root=root
        self.root.geometry("1100x500+320+220")
        self.root.config(bg="white")
        self.root.resizable(False,False)
        self.root.focus_force()

        #--------- image data ---------
        image_layout = {
            "img1": {"path": IMG_CAT, "pos": (50, 220), "resize": (500, 250), "border": 2, "relief": "raised" },
            "img2": {"path": IMG_CATEGORY, "pos": (580, 220), "resize": (500, 250), "border": 2, "relief": "raised" }
            }

        #------------ variables -------------
        self.var_cat_id=StringVar()
        self.var_name=StringVar()
        #--------------- title ---------------------
        lbl_title=Label(self.root,text="Manage Product Category",font=(APP_FONT,30),bg="#184a45",fg="white",bd=3,relief=RIDGE).pack(side=TOP,fill=X,padx=10,pady=20)
        
        lbl_mame=Label(self.root,text="Enter Category Name",font=(APP_FONT,30),bg="white").place(x=50,y=100)
        txt_mame=Entry(self.root,textvariable=self.var_name,bg="lightyellow",font=(APP_FONT,18)).place(x=50,y=170,width=300)

        btn_add=Button(self.root,text="ADD",command=self.add,font=FONT_GENERAL,bg="#4caf50",fg="white",cursor="hand2").place(x=360,y=170,width=150,height=30)
        btn_delete=Button(self.root,text="Delete",command=self.delete,font=FONT_GENERAL,bg="red",fg="white",cursor="hand2").place(x=520,y=170,width=150,height=30)

        #------------ category details -------------
        cat_frame=Frame(self.root,bd=3,relief=RIDGE)
        cat_frame.place(x=700,y=100,width=380,height=100)

        scrolly=Scrollbar(cat_frame,orient=VERTICAL)
        scrollx=Scrollbar(cat_frame,orient=HORIZONTAL)\
        
        self.CategoryTable=ttk.Treeview(cat_frame,columns=("cid","name"),yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM,fill=X)
        scrolly.pack(side=RIGHT,fill=Y)
        scrollx.config(command=self.CategoryTable.xview)
        scrolly.config(command=self.CategoryTable.yview)
        self.CategoryTable.heading("cid",text="C ID")
        self.CategoryTable.heading("name",text="Name")
        self.CategoryTable["show"]="headings"
        self.CategoryTable.column("cid",width=90)
        self.CategoryTable.column("name",width=100)
        
        self.CategoryTable.pack(fill=BOTH,expand=1)
        self.CategoryTable.bind("<ButtonRelease-1>",self.get_data)
        self.show()

        #----------------- images ---------------------
        self.images, self.labels = load_and_place_images(self.root, image_layout)
        #-------------------------------------------------- 

    def add(self):
        con = db_connect()
        cur = con.cursor()
        try:
            if self.var_name.get()=="":
                messagebox.showerror("Error","Category Name must be required",parent=self.root)
            else:
                cur.execute("Select * from category where name=?",(self.var_name.get(),))
                row=cur.fetchone()
                if row!=None:
                    messagebox.showerror("Error","Category already present",parent=self.root)
                else:
                    cur.execute("insert into category(name) values(?)",(
                        self.var_name.get(),
                    ))
                    con.commit()
                    messagebox.showinfo("Success","Category Added Successfully",parent=self.root)
                    self.clear()
                    self.show()
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}")

    def show(self):
        con = db_connect()
        cur = con.cursor()
        try:
            cur.execute("select * from category")
            rows=cur.fetchall()
            self.CategoryTable.delete(*self.CategoryTable.get_children())
            for row in rows:
                self.CategoryTable.insert('',END,values=row)
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}")

    
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
                messagebox.showerror("Error","Category name must be required",parent=self.root)
            else:
                cur.execute("Select * from category where cid=?",(self.var_cat_id.get(),))
                row=cur.fetchone()
                if row==None:
                    messagebox.showerror("Error","Invalid Category Name",parent=self.root)
                else:
                    op=messagebox.askyesno("Confirm","Do you really want to delete?",parent=self.root)
                    if op==True:
                        cur.execute("delete from category where cid=?",(self.var_cat_id.get(),))
                        con.commit()
                        messagebox.showinfo("Delete","Category Deleted Successfully",parent=self.root)
                        self.clear()
                        self.var_cat_id.set("")
                        self.var_name.set("")
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}")



if __name__=="__main__":
    root=Tk()
    obj=categoryClass(root)
    root.mainloop()