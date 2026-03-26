from tkinter import*
from PIL import Image,ImageTk
from tkinter import ttk
import sqlite3
import time
import os
import tempfile
from config import IMAGE_DIR, BILL_DIR
from db.db_helper import db_connect, run_query
from ui.ui_utility import msg_manager, format_table, setup_window, BaseWindow

from ui.ui_styles import FONT_TITLE, FONT_BILLING_PRIMARY, FONT_BILLING_SECONDARY


#billing images
IMG_LOGO = os.path.join(IMAGE_DIR, "logo1.png")

class billClass(BaseWindow):
    def __init__(self,root,user_name, user_type, launcher):
        self.root=root
        self.user=user_name
        self.user_type = user_type
        self.launcher = launcher

        self.setup_window("1350x700+110+80")
        self.set_title("Billing")
 
        self.init_variables()
        self.build_header()
        self.build_product_section()
        self.build_customer_section()
        self.build_calculator_cart_section()
        self.build_cart_widgets()
        self.build_bill_section()
        self.build_bill_buttons()

        self.show()
        self.update_date_time()

    def init_variables(self):
        self.cart_list = []
        self.chk_print = 0
        self.discount_percent = 5 # Discount percentage

        self.var_search = StringVar()
        self.var_cal_input = StringVar()

        #--------- customer info ------------
        self.var_cname = StringVar()
        self.var_contact = StringVar()
        #--------- product info ------------
        self.var_pid = StringVar()
        self.var_pname = StringVar()
        self.var_price = StringVar()
        self.var_qty = StringVar()
        self.var_stock = StringVar()


    def build_header(self):
        self.icon_title = PhotoImage(file=IMG_LOGO)
        #------------ title --------------
        Label(
            self.root,text="Inventory Management System",
            image=self.icon_title,
            compound=LEFT,
            font=FONT_TITLE,
            bg="#010c48",
            fg="white",anchor="w",
            padx=20
        ).place(x=0,y=0,relwidth=1,height=70)

            #------------ logout button -----------
        btn_logout = Button(
            self.root,
            text="Logout",
            command=self.logout,
            font=(FONT_BILLING_PRIMARY, 15, "bold"),
            bg="yellow",
            cursor="hand2"
        ).place(x=1150, y=10, height=50, width=150)

            #------------ clock -----------------   
        self.lbl_clock = Label(
            self.root,
            text="",
            font=(FONT_BILLING_PRIMARY, 15),
            bg="#4d636d",
            fg="white"
        )
        self.lbl_clock.place(x=0, y=70, relwidth=1, height=30)
    # ---------------- product frame -----------------
    def build_product_section(self):
        frame = Frame(self.root, bd=4, relief=RIDGE, bg="white")
        frame.place(x=6, y=110, width=410, height=550)

        Label(frame, text="All Products",
            font=(FONT_BILLING_SECONDARY, 20, "bold"),
            bg="#262626", fg="white").pack(side=TOP, fill=X)

        self.build_product_search(frame)
        self.build_product_table(frame)

    def build_product_search(self, parent):
        frame = Frame(parent, bd=2, relief=RIDGE, bg="white")
        frame.place(x=2, y=42, width=398, height=90)

        Label(frame, text="Search Product | By Name",
            font=(FONT_BILLING_PRIMARY, 15, "bold"),
            bg="white", fg="green").place(x=2, y=5)

        Entry(frame, textvariable=self.var_search,
            font=(FONT_BILLING_PRIMARY, 15),
            bg="lightyellow").place(x=128, y=47, width=150)

        Button(frame, text="Search", command=self.search,
            bg="#2196f3", fg="white").place(x=285, y=45, width=100)

        Button(frame, text="Show All", command=self.show,
            bg="#083531", fg="white").place(x=285, y=10, width=100)

    def build_product_table(self, parent):
        frame = Frame(parent, bd=3, relief=RIDGE)
        frame.place(x=2, y=140, width=398, height=375)

        

        columns=["pid", "name", "price", "qty", "status"] 
        names=["P ID", "Name", "Price", "Quantity", "Status"]
        widths=[40, 100, 100, 40, 90]
        self.product_Table = format_table(frame, columns, names, widths)

        self.product_Table.bind("<ButtonRelease-1>",self.get_data)
        
        lbl_note=Label(frame,text="Note: 'Enter 0 Quantity to remove product from the Cart'",
            font=(FONT_BILLING_SECONDARY,12),
            anchor="w",
            bg="white",
            fg="red"
        ).pack(side=BOTTOM,fill=X)

        #-------------- customer frame ---------------
    def build_customer_section(self):
        frame = Frame(self.root, bd=4, relief=RIDGE, bg="white")
        frame.place(x=420, y=110, width=530, height=70)

        Label(frame, text="Customer Details",
            font=(FONT_BILLING_SECONDARY, 15),
            bg="lightgray").pack(side=TOP, fill=X)

        Label(frame, text="Name",
            font=(FONT_BILLING_PRIMARY, 15),
            bg="white").place(x=5, y=35)

        Entry(frame, textvariable=self.var_cname,
            font=(FONT_BILLING_PRIMARY, 13),
            bg="lightyellow").place(x=80, y=35, width=180)

        Label(frame, text="Contact No.",
            font=(FONT_BILLING_PRIMARY, 15),
            bg="white").place(x=270, y=35)

        Entry(frame, textvariable=self.var_contact,
            font=(FONT_BILLING_PRIMARY, 15),
            bg="lightyellow").place(x=380, y=35, width=140)

    def build_calculator_cart_section(self):
        container = Frame(self.root, bd=2, relief=RIDGE, bg="white")
        container.place(x=420, y=190, width=530, height=360)

        self.build_calculator(container)
        self.build_cart(container)

    #--------------- calculator frame ---------------------
    def build_calculator(self, parent):
        frame = Frame(parent, bd=9, relief=RIDGE, bg="white")
        frame.place(x=5, y=10, width=268, height=340)

        Entry(frame, textvariable=self.var_cal_input,
            font=('arial', 15, 'bold'),
            state='readonly',
            justify=RIGHT).grid(row=0, columnspan=4)#, sticky="we")

        buttons = [
            ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('+', 1, 3),
            ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('-', 2, 3),
            ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('*', 3, 3),
            ('0', 4, 0), ('C', 4, 1), ('=', 4, 2), ('/', 4, 3),
        ]

        for (text, row, col) in buttons:
            action = (
                self.clear_cal if text == 'C' else
                self.perform_cal if text == '=' else
                lambda t=text: self.get_input(t)
            )

            Button(frame, text=text,
                font=('arial', 15, 'bold'),
                command=action,
                bd=5, width=4, pady=10).grid(row=row, column=col)
        #------------------ cart frame --------------------
    def build_cart(self, parent):
        frame = Frame(parent, bd=3, relief=RIDGE)
        frame.place(x=280, y=8, width=245, height=342)

        self.cartTitle = Label(
            frame,
            text="Cart \t Total Products: [0]",
            font=(FONT_BILLING_SECONDARY, 15),
            bg="lightgray"
        )
        self.cartTitle.pack(side=TOP, fill=X)

        self.CartTable = ttk.Treeview(
            frame,
            columns=("pid", "name", "price", "qty")
        )

        self.CartTable.heading("pid", text="P ID")
        self.CartTable.heading("name", text="Name")
        self.CartTable.heading("price", text="Price")
        self.CartTable.heading("qty", text="Quantity")
        self.CartTable["show"] = "headings"
        self.CartTable.column("pid", width=20)
        self.CartTable.column("name", width=100)
        self.CartTable.column("price", width=30)
        self.CartTable.column("qty", width=50)
        self.CartTable.pack(fill=BOTH, expand=1)
        self.CartTable.bind("<ButtonRelease-1>", self.get_data_cart)


  
        #-------------- add cart widgets frame ---------------

    def build_cart_widgets(self):
        frame = Frame(self.root, bd=2, relief=RIDGE, bg="white")
        frame.place(x=420, y=550, width=530, height=110)

        self.create_label_entry(frame, "Product Name", self.var_pname, 5, readonly=True, width=190)
        self.create_label_entry(frame, "Price Per Qty", self.var_price, 230, readonly=True, width=150)
        self.create_label_entry(frame, "Quantity", self.var_qty, 390, width=120)

        self.lbl_inStock = Label(
            frame,
            text="In Stock",
            font=(FONT_BILLING_PRIMARY, 15),
            bg="white"
        )
        self.lbl_inStock.place(x=5, y=70)

        Button(frame, text="Clear",
            command=self.clear_cart,
            font=(FONT_BILLING_PRIMARY, 15, "bold"),
            bg="lightgray").place(x=180, y=70, width=150)

        Button(frame, text="Add | Update",
            command=self.add_update_cart,
            font=(FONT_BILLING_PRIMARY, 15, "bold"),
            bg="orange").place(x=340, y=70, width=180)
    
    def create_label_entry(self, parent, text, var, x, readonly=False, width=150):
        Label(parent, text=text,
            font=(FONT_BILLING_PRIMARY, 15),
            bg="white").place(x=x, y=5)

        Entry(parent,
            textvariable=var,
            font=(FONT_BILLING_PRIMARY, 15),
            bg="lightyellow",
            state='readonly' if readonly else 'normal'
            ).place(x=x, y=35, width=width)

            #------------------- billing area -------------------
    def build_bill_section(self):
        frame = Frame(self.root, bd=2, relief=RIDGE, bg="white")
        frame.place(x=953, y=110, width=400, height=410)

        Label(frame, text="Customer Bill Area",
            font=(FONT_BILLING_SECONDARY, 20, "bold"),
            bg="#262626", fg="white").pack(side=TOP, fill=X)

        scroll = Scrollbar(frame, orient=VERTICAL)
        scroll.pack(side=RIGHT, fill=Y)

        self.txt_bill_area = Text(frame, yscrollcommand=scroll.set)
        self.txt_bill_area.pack(fill=BOTH, expand=1)

        scroll.config(command=self.txt_bill_area.yview)        

    #------------------- billing buttons -----------------------
    def build_bill_buttons(self):
        frame = Frame(self.root, bd=2, relief=RIDGE, bg="white")
        frame.place(x=953, y=520, width=400, height=140)

        self.lbl_amnt = Label(
            frame,
            text="Bill Amount\n[0]",
            font=(FONT_BILLING_SECONDARY,15,"bold"),
            bg="#3f51b5",
            fg="white"
        )

        self.lbl_amnt.place(x=2, y=5, width=120, height=70)

        self.lbl_discount = Label(frame,
            text="Discount\n[5%]",
            font=(FONT_BILLING_SECONDARY,15,"bold"),
            bg="#8bc34a",
            fg="white"
        )
        self.lbl_discount.place(x=124,y=5,width=120,height=70)

        self.lbl_net_pay = Label(frame,
            text="Net Pay\n[0]",
            font=(FONT_BILLING_SECONDARY,15,"bold"),
            bg="#607d8b",
            fg="white"
        )
        self.lbl_net_pay.place(x=246,y=5,width=160,height=70)

        self.btn_print = Button(frame, 
            text="Print", 
            command=self.print_bill,
            cursor="hand2",
            font=(FONT_BILLING_SECONDARY,15,"bold"),
            bg="lightgreen", 
            fg="white"
        )
        self.btn_print.place(x=2, y=80, width=120, height=50)

        self.btn_clear_all = Button(frame, 
            text="Clear All", 
            command=self.clear_all,
            cursor="hand2",
            font=(FONT_BILLING_SECONDARY,15,"bold"),
            bg="gray", fg="white"
        )
        self.btn_clear_all.place(x=124, y=80, width=120, height=50)

        self.btn_generate = Button(frame, 
            text="Generate Bill", 
            command=self.generate_bill,
            cursor="hand2",
            font=(FONT_BILLING_SECONDARY,15,"bold"),
            bg="#009688", 
            fg="white"
        )
        self.btn_generate.place(x=246, y=80, width=160, height=50)

    def get_input(self,num):
        xnum=self.var_cal_input.get()+str(num)
        self.var_cal_input.set(xnum)

    def clear_cal(self):
        self.var_cal_input.set('')

    def perform_cal(self):
        result=self.var_cal_input.get()
        self.var_cal_input.set(eval(result))

    def show(self):
        result = run_query((
            "SELECT pid, name, price, qty, status FROM product WHERE status='Active'", ()
        ), fetch=True)
        if result["ok"]:
            self.product_Table.delete(*self.product_Table.get_children())
            for row in result["data"]:
                self.product_Table.insert('', END, values=row)
        else:
            msg_manager("Error",f"Error due to: {result['error']}", self)

    def search(self):
        if not self.var_search.get():
            msg_manager("Error","Search input should be required", self)
            return

        sql = "SELECT pid, name, price, qty, status FROM product WHERE name LIKE ?"
        pattern = f"%{self.var_search.get()}%"
        result = run_query((sql, (pattern,)), fetch=True)

        if result["ok"]:
            if result["data"]:
                self.product_Table.delete(*self.product_Table.get_children())
                for row in result["data"]:
                    self.product_Table.insert('', END, values=row)
            else:
                msg_manager("Error","No record found!!!", self)
        else:
            msg_manager("Error",f"Error due to: {result['error']}", self)

    def get_data(self,ev):
        f=self.product_Table.focus()
        content=(self.product_Table.item(f))
        row=content['values']
        self.var_pid.set(row[0])
        self.var_pname.set(row[1])
        self.var_price.set(row[2])
        self.lbl_inStock.config(text=f"In Stock [{str(row[3])}]")
        self.var_stock.set(row[3])
        self.var_qty.set('1')
    
    def get_data_cart(self,ev):
        f=self.CartTable.focus()
        content=(self.CartTable.item(f))
        row=content['values']
        self.var_pid.set(row[0])
        self.var_pname.set(row[1])
        self.var_price.set(row[2])
        self.var_qty.set(row[3])
        self.lbl_inStock.config(text=f"In Stock [{str(row[4])}]")
        self.var_stock.set(row[4])
        
    def add_update_cart(self):
        if self.var_pid.get()=="":
            msg_manager("Error","Please select product from the list", self)
        elif self.var_qty.get()=="":
            msg_manager("Error","Quantity is required", self)
        elif int(self.var_qty.get())>int(self.var_stock.get()):
            msg_manager("Error","Invalid Quantity", self)
        else:
            #price_cal=int(self.var_qty.get())*float(self.var_price.get())
            #price_cal=float(price_cal)
            price_cal=self.var_price.get()
            cart_data=[self.var_pid.get(),self.var_pname.get(),price_cal,self.var_qty.get(),self.var_stock.get()]
            #---------- update cart --------------
            present="no"
            index_=0
            for row in self.cart_list:
                if self.var_pid.get()==row[0]:
                    present="yes"
                    break
                index_+=1
            if present=="yes":
                op=msg_manager("Confirm", "Product already present\nDo you want to Update|Remove from the Cart List", self)
                if op==True:
                    if self.var_qty.get()=="0":
                        self.cart_list.pop(index_)
                    else:
                        #self.cart_list[index_][2]=price_cal
                        self.cart_list[index_][3]=self.var_qty.get()
            else:
                self.cart_list.append(cart_data)
            self.show_cart()
            self.bill_update()

    def bill_update(self):
        self.bill_amnt=0
        self.net_pay=0
        self.discount=0
        for row in self.cart_list:
            self.bill_amnt=self.bill_amnt+(float(row[2])*int(row[3]))
        self.discount=round((self.bill_amnt*self.discount_percent)/100, 2)
        self.net_pay=round(self.bill_amnt-self.discount, 2)
        self.lbl_amnt.config(text=f"Bill Amount\n{str(self.bill_amnt)}")
        self.lbl_net_pay.config(text=f"Net Pay\n{str(self.net_pay)}")
        self.cartTitle.config(text=f"Cart \t Total Products: [{str(len(self.cart_list))}]")

    def show_cart(self):
        try:
            self.CartTable.delete(*self.CartTable.get_children())
            for row in self.cart_list:
                self.CartTable.insert('',END,values=row)
        except Exception as ex:
            msg_manager("Error",f"Error due to : {str(ex)}")

    def generate_bill(self):
        if self.var_cname.get()=="" or self.var_contact.get()=="":
            msg_manager("Error",f"Customer Details are required", self)
        elif len(self.cart_list)==0:
            msg_manager("Error",f"Please Add product to the Cart!!!", self)
        else:
            #--------- bill top -----------------
            self.bill_top()
            #--------- bill middle --------------
            self.bill_middle()
            #--------- bill bottom --------------
            self.bill_bottom()

            fp=open(f'{BILL_DIR}/{str(self.invoice)}.txt','w')
            fp.write(self.txt_bill_area.get('1.0',END))
            fp.close()
            msg_manager("Success", "Bill has been generated", self)
            self.chk_print=1

    def bill_top(self):
        self.invoice=int(time.strftime("%H%M%S"))+int(time.strftime("%d%m%Y"))
        bill_top_temp=f'''
\t\tXYZ-Inventory
\t Phone No. 9899459288 , Delhi-110053
{str("="*46)}
 Customer Name: {self.var_cname.get()}
 Ph. no. : {self.var_contact.get()}
 Bill No. {str(self.invoice)}\t\t\tDate: {str(time.strftime("%d/%m/%Y"))}
{str("="*46)}
 Product Name\t\t\tQTY\tPrice
{str("="*46)}
'''
        self.txt_bill_area.delete('1.0',END)
        self.txt_bill_area.insert('1.0',bill_top_temp)

    def bill_bottom(self):
        bill_bottom_temp=f'''
{str("="*46)}
 Bill Amount\t\t\t\tRs.{self.bill_amnt}
 Discount\t\t\t\tRs.{self.discount}
 Net Pay\t\t\t\tRs.{self.net_pay}
{str("="*46)}\n
'''
        self.txt_bill_area.insert(END,bill_bottom_temp)

    def bill_middle(self):
        try:
            updates = [] #list for batch update
            for row in self.cart_list:
                pid = row[0]
                name = row[1]
                bought_qty = int(row[3])
                current_qty = int(row[4])
                remaining_qty = current_qty - bought_qty
                status = "Inactive" if remaining_qty == 0 else "Active"
                price = float(row[2]) * bought_qty
                self.txt_bill_area.insert(END, f"\n {name}\t\t\t{bought_qty}\tRs.{price:.2f}")

                updates.append((remaining_qty, status, pid))

            con = db_connect()
            cur = con.cursor()
            try:
                for qty, status, pid in updates:
                    cur.execute("UPDATE product SET qty=?, status=? WHERE pid=?", (qty, status, pid))
                con.commit()
            except Exception as e:
                con.rollback()
                msg_manager("Error",f"Error updating products: {str(e)}", self)
                return
            finally:
                con.close()

            self.show()

        except Exception as ex:
            msg_manager("Error",f"Error due to: {str(ex)}", self)


    def clear_cart(self):
        self.var_pid.set("")
        self.var_pname.set("")
        self.var_price.set("")
        self.var_qty.set("")
        self.lbl_inStock.config(text=f"In Stock")
        self.var_stock.set("")
        self.lbl_amnt.config(self.lbl_amnt.config(text="Bill Amount\n[0]"))

    def clear_all(self):
        del self.cart_list[:]
        self.clear_cart()
        self.show()
        self.show_cart()
        self.var_cname.set("")
        self.var_contact.set("")
        self.chk_print=0
        self.txt_bill_area.delete('1.0',END)
        self.cartTitle.config(text=f"Cart \t Total Products: [0]")
        self.var_search.set("")
        
    def update_date_time(self):
        time_=time.strftime("%I:%M:%S")
        date_=time.strftime("%d-%m-%Y")
        self.lbl_clock.config(text=f"Welcome to Inventory Management System\t\t Date: {str(date_)}\t\t Time: {str(time_)}")
        self.lbl_clock.after(1000,self.update_date_time)

    def print_bill(self):
        if self.chk_print==1:
            msg_manager("Print","Please wait while printing", self)
            new_file=tempfile.mktemp('.txt')
            open(new_file,'w').write(self.txt_bill_area.get('1.0',END))
            os.startfile(new_file,'print')
        else:
            msg_manager("Print","Please generate bill to print the receipt", self)

if __name__=="__main__":
    from modules.login import LoginSystem
    
    root = Tk()
    #Module is not dashboard, False is passed to launch correct module after login
    obj = LoginSystem(root, dashboard=False)
    root.mainloop()