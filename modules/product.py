from tkinter import*
from PIL import Image,ImageTk
from tkinter import ttk
import sqlite3
from db.db_helper import db_connect, run_query, is_admin
from ui.ui_styles import FONT_GENERAL, FONT_PRODUCT_TITLE, APP_FONT
from ui.ui_utility import msg_manager, format_table, BaseWindow

class productClass(BaseWindow):
    def __init__(self,root, user_name, user_type):
        self.root=root
        self.user=user_name
        self.user_type = user_type
        self.setup_window("1100x500+320+220")
        self.set_title("Product")

        self.init_vars()

        self.build_table()
        self.fetch_cat_sup()
        
        self.build_form()
        self.build_search()
        

        
        self.show()
        #---------------------------------------

        #----------- variables -------------
    def init_vars(self):
        self.var_cat=StringVar()
        self.cat_list=[]
        self.sup_list=[]

        self.var_pid=StringVar()
        self.var_sup=StringVar()
        self.var_name=StringVar()
        self.var_price=StringVar()
        self.var_qty=StringVar()
        self.var_status=StringVar()
        self.var_searchby=StringVar()
        self.var_searchtxt=StringVar()

        product_Frame=Frame(self.root,bd=2,relief=RIDGE,bg="white")
        product_Frame.place(x=10,y=10,width=450,height=480)

        #------------ title --------------
    def build_form(self):
        frame = Frame(self.root, 
            bd=2, 
            relief=RIDGE, 
            bg="white")
        frame.place(x=10, y=10, width=450, height=480)

        Label(frame, text="Manage Product Details",
              font=FONT_PRODUCT_TITLE, 
              bg="#0f4d7d",
              fg="white").pack(side=TOP, fill=X)

        #-------------- Field config --------------
        fields = [
            ("Category", self.var_cat, self.cat_list, 60),
            ("Supplier", self.var_sup, self.sup_list, 110),
            ("Name", self.var_name, None, 160),
            ("Price", self.var_price, None, 210),
            ("Quantity", self.var_qty, None, 260),
            ("Status", self.var_status, ["Active", "Inactive"], 310),
        ]
        #--------------  Button config --------------
        actions = [
            ("Save", self.add, "#2196f3"),
            ("Update", self.update, "#4caf50"),
            ("Delete", self.delete, "#f44336"),
            ("Clear", self.clear, "#607d8b"),
        ]
        #-------------- Field setup --------------
        for label, var, values, y in fields:
            Label(frame, text=label, font=FONT_PRODUCT_TITLE,
                  bg="white").place(x=30, y=y)

            if values:
                ttk.Combobox(frame, textvariable=var,
                             values=values, state='readonly',
                             justify=CENTER,
                             font=FONT_GENERAL).place(x=150, y=y, width=200)
            else:
                Entry(frame, textvariable=var,
                      font=FONT_GENERAL,
                      bg="lightyellow").place(x=150, y=y, width=200)

        #-------------- button setup -----------------
        btn_x_offset = 10
        for text, cmd, color in actions:
            btn = Button(frame, text=text, command=cmd,
                   font=FONT_GENERAL, bg=color, fg="white",
                   cursor="hand2")
            self.restrict_admin(btn) if text == "Delete" else None
            btn.place(x=btn_x_offset, y=400, width=100, height=40)
            btn_x_offset += 110

        #---------- Search Frame -------------
    def build_search(self):
        frame = LabelFrame(self.root, text="Search Product",
                           font=(APP_FONT, 12, "bold"),
                           bd=2, relief=RIDGE, bg="white")
        frame.place(x=480, y=10, width=600, height=80)

        ttk.Combobox(frame, textvariable=self.var_searchby,
                     values=("Select", "category", "supplier", "name"),
                     state='readonly', justify=CENTER,
                     font=FONT_GENERAL).place(x=10, y=10, width=180)

        Entry(frame, textvariable=self.var_searchtxt,
              font=FONT_GENERAL, bg="lightyellow").place(x=200, y=10)

        Button(frame, text="Search", command=self.search,
               font=FONT_GENERAL, bg="#4caf50",
               fg="white", cursor="hand2").place(x=410, y=9, width=150, height=30)

        #------------ product details -------------
    def build_table(self):
        frame = Frame(self.root, bd=3, relief=RIDGE)
        frame.place(x=480, y=100, width=600, height=390)

        columns = ("pid", "category", "supplier", "name", "price", "qty", "status")
        names = ("P ID", "Category", "Supplier", "Name", "Price", "Quantity", "Status")
        widths = [90]+[100] * (len(columns)-1) 
        self.ProductTable = format_table(frame, columns, names, widths)
        self.ProductTable.bind("<ButtonRelease-1>", self.get_data)
#-----------------------------------------------------------------------------------------------------
    def fetch_cat_sup(self):
        self.cat_list.append("Empty")
        self.sup_list.append("Empty")
        con = db_connect()
        cur = con.cursor()
        try:
            cur.execute("select name from category")
            cat=cur.fetchall()
            if len(cat)>0:
                del self.cat_list[:]
                for i in cat:
                    self.cat_list.append(i[0])
            cur.execute("select name from supplier")
            sup=cur.fetchall()
            if len(sup)>0:
                del self.sup_list[:]
                for i in sup:
                    self.sup_list.append(i[0])
            self.clear()
            self.show()
        except Exception as ex:
            msg_manager("Error",f"Error due to : {str(ex)}", self)
        finally:
            con.close()

    
    def add(self):
        if not self.validate():
            return

        # Check if product exists
        result = run_query(("SELECT * FROM product WHERE name=?", (self.var_name.get(),)), fetch=True)
        if not result["ok"]:
            msg_manager("Error", f"Error due to: {result['error']}", self)
            return
        if result["data"]:
            msg_manager("Error", "Product already present", self)
            return

        # Insert new product
        insert_result = run_query((
            "INSERT INTO product(Category,Supplier,name,price,qty,status) VALUES (?,?,?,?,?,?)",
            (
                self.var_cat.get(),
                self.var_sup.get(),
                self.var_name.get(),
                self.var_price.get(),
                self.var_qty.get(),
                self.var_status.get(),
            )
        ))
        if insert_result["ok"]:
            msg_manager("Success", "Product Added Successfully", self)
            self.clear()
            self.show()
        else:
            msg_manager("Error", f"Error due to: {insert_result['error']}", self)


    def show(self):
        result = run_query(("SELECT * FROM product", ()), fetch=True)
        if result["ok"]:
            self.ProductTable.delete(*self.ProductTable.get_children())
            for row in result["data"]:
                self.ProductTable.insert('', END, values=row)
        else:
            msg_manager("Error", f"Error due to: {result['error']}", self)

    def get_data(self,ev):
        f=self.ProductTable.focus()
        content=(self.ProductTable.item(f))
        row=content['values']
        self.var_pid.set(row[0])
        self.var_cat.set(row[1])
        self.var_sup.set(row[2])
        self.var_name.set(row[3])
        self.var_price.set(row[4])
        self.var_qty.set(row[5])
        self.var_status.set(row[6])


    def update(self):
        if not self.var_pid.get():
            msg_manager("Error", "Please select product from list", self)
            return
        
        if not self.validate():
            return

        # Check if product exists
        result = run_query(("SELECT * FROM product WHERE pid=?", (self.var_pid.get(),)), fetch=True)
        if not result["ok"]:
            msg_manager("Error", f"Error due to: {result['error']}", self)
            return
        if not result["data"]:
            msg_manager("Error", "Invalid Product", self)
            return

        # Update product
        update_result = run_query((
            "UPDATE product SET Category=?, Supplier=?, name=?, price=?, qty=?, status=? WHERE pid=?",
            (
                self.var_cat.get(),
                self.var_sup.get(),
                self.var_name.get(),
                self.var_price.get(),
                self.var_qty.get(),
                self.var_status.get(),
                self.var_pid.get(),
            )
        ))
        if update_result["ok"]:
            msg_manager("Success", "Product Updated Successfully", self)
            self.show()
        else:
            msg_manager("Error", f"Error due to: {update_result['error']}", self)


    def delete(self):
        if not is_admin(self.user_type):
            msg_manager("Error", "Only admin can delete product", self)
            return  

        if not self.var_pid.get():
            msg_manager("Error", "Select Product from the list", self)
            return

        # Check if product exists
        result = run_query(("SELECT * FROM product WHERE pid=?", (self.var_pid.get(),)), fetch=True)
        if not result["ok"]:
            msg_manager("Error", f"Error due to: {result['error']}", self)
            return
        if not result["data"]:
            msg_manager("Error", "Invalid Product", self)
            return

        # Confirm deletion
        if msg_manager("Confirm", "Do you really want to delete?", self):
            delete_result = run_query(("DELETE FROM product WHERE pid=?", (self.var_pid.get(),)))
            if delete_result["ok"]:
                msg_manager("Delete", "Product Deleted Successfully", self)
                self.clear()
            else:
                msg_manager("Error", f"Error due to: {delete_result['error']}", self)


    def clear(self):
        self.var_cat.set("Select")
        self.var_sup.set("Select")
        self.var_name.set("")
        self.var_price.set("")
        self.var_qty.set("")
        self.var_status.set("Active")
        self.var_pid.set("")
        self.var_searchby.set("Select")
        self.var_searchtxt.set("")
        self.show()


    def search(self):
        if self.var_searchby.get() == "Select":
            msg_manager("Error", "Select Search By option", self)
            return
        if not self.var_searchtxt.get():
            msg_manager("Error", "Search input should be required", self)
            return

        sql = f"SELECT * FROM product WHERE {self.var_searchby.get()} LIKE ?"
        pattern = f"%{self.var_searchtxt.get()}%"
        result = run_query((sql, (pattern,)), fetch=True)
        if result["ok"]:
            if result["data"]:
                self.ProductTable.delete(*self.ProductTable.get_children())
                for row in result["data"]:
                    self.ProductTable.insert('', END, values=row)
            else:
                msg_manager("Error", "No record found!!!", self)
        else:
            msg_manager("Error", f"Error due to: {result['error']}", self)

    def validate(self):
        if not self.var_name.get().strip():
            msg_manager("Error", "Product name required", self)
            return False

        if not self.var_price.get().replace('.', '', 1).isdigit():
            msg_manager("Error", "Price must be a number", self)
            return False

        if float(self.var_price.get()) <= 0:
            msg_manager("Error", "Price must be positive", self)
            return False

        if not self.var_qty.get().isdigit():
            msg_manager("Error", "Quantity must be integer", self)
            return False

        if int(self.var_qty.get()) < 0:
            msg_manager("Error", "Quantity cannot be negative", self)
            return False
        
        if self.var_cat.get() == "Select" or self.var_sup.get() == "Select":
            msg_manager("Error", "Please select category and supplier", self)
            return False

        return True


if __name__=="__main__":
    root=Tk()
    obj=productClass(root)
    root.mainloop()