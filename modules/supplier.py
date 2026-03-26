from tkinter import*
from PIL import Image,ImageTk
from tkinter import ttk
import sqlite3
from db.db_helper import run_query, is_admin
from ui.ui_styles import FONT_GENERAL, FONT_TITLE_LBL
from ui.ui_utility import msg_manager, format_table, BaseWindow

class supplierClass(BaseWindow):
    def __init__(self,root,user_name, user_type):
        self.root=root
        self.user=user_name
        self.user_type = user_type
        self.setup_window("1100x500+320+220")
        self.set_title("Supplier")

        self.init_vars()
        self.build_title()
        self.build_search()
        self.build_form()
        self.build_buttons()
        self.build_table()

        self.show()

    # ---------------- INIT ----------------
    def init_vars(self):
        self.var_searchtxt = StringVar()
        self.var_sup_invoice = StringVar()
        self.var_name = StringVar()
        self.var_contact = StringVar()
        

    #-------------- title ---------------
    def build_title(self):
        Label(
            self.root,
            text="Supplier Details",
            font=FONT_TITLE_LBL,
            bg="#0f4d7d",
            fg="white"
        ).place(x=50, y=10, width=1000, height=40)
    #---------- Search Frame -------------
    def build_search(self):
        Label(self.root, text="Invoice No.", bg="white", font=FONT_GENERAL)\
            .place(x=700, y=80)

        Entry(self.root, textvariable=self.var_searchtxt,
              font=FONT_GENERAL, bg="lightyellow")\
            .place(x=850, y=80, width=160)

        Button(self.root, text="Search", command=self.search,
               font=FONT_GENERAL, bg="#4caf50", fg="white",
               cursor="hand2")\
            .place(x=980, y=79, width=100, height=28)
        
    #-------------- content ---------------
    def build_form(self):
        fields = [
            ("Invoice No.", self.var_sup_invoice, 80),
            ("Name", self.var_name, 120),
            ("Contact", self.var_contact, 160),
        ]

        for label, var, y in fields:
            Label(self.root, text=label, font=FONT_GENERAL, bg="white")\
                .place(x=50, y=y)

            Entry(self.root, textvariable=var,
                  font=FONT_GENERAL, bg="lightyellow")\
                .place(x=180, y=y, width=180)

        # Description is special
        Label(self.root, text="Description", font=FONT_GENERAL, bg="white")\
            .place(x=50, y=200)

        self.txt_desc = Text(self.root, font=FONT_GENERAL, bg="lightyellow")
        self.txt_desc.place(x=180, y=200, width=470, height=120)
        
        #-------------- buttons -----------------
    def build_buttons(self):
        actions = [
            ("Save", self.add, "#2196f3"),
            ("Update", self.update, "#4caf50"),
            ("Delete", self.delete, "#f44336"),
            ("Clear", self.clear, "#607d8b"),
        ]

        x_pos_shift = 180
        for text, cmd, color in actions:
            btn = Button(self.root, text=text, command=cmd,
                   font=FONT_GENERAL, bg=color, fg="white",
                   cursor="hand2")
            
            self.restrict_admin(btn) if text == "Delete" else None
            btn.place(x=x_pos_shift, y=370, width=110, height=35)
            x_pos_shift += 120
        #------------ supplier details -------------
    def build_table(self):
        frame = Frame(self.root, bd=3, relief=RIDGE)
        frame.place(x=700, y=120, width=380, height=350)

        columns = ("invoice", "name", "contact", "desc")
        names = ("Invoice", "Name", "Contact", "Description")
        widths = [90]+[100] * (len(columns)-1) 
        self.SupplierTable =format_table(frame, columns, names, widths)
        self.SupplierTable.bind("<ButtonRelease-1>",self.get_data)
#-----------------------------------------------------------------------------------------------------

    def add(self):
        if not self.var_sup_invoice.get():
            msg_manager("Error", "Invoice must be required", self)
            return

        if not self.validate():
            return
        
        # Check exist
        result = run_query(("SELECT * FROM supplier WHERE invoice=?", (self.var_sup_invoice.get(),)), fetch=True)
        if not result["ok"]:
            msg_manager("Error", f"Error due to: {result['error']}", self)
            return
        if result["data"]:
            msg_manager("Error", "Invoice no. is already assigned", self)
            return

        insert_result = run_query((
            "INSERT INTO supplier(invoice,name,contact,desc) VALUES (?,?,?,?)",
            (
                self.var_sup_invoice.get(),
                self.var_name.get(),
                self.var_contact.get(),
                self.txt_desc.get('1.0', END),
            )
        ))
        if insert_result["ok"]:
            msg_manager("Success", "Supplier Added Successfully", self)
            self.clear()
            self.show()
        else:
            msg_manager("Error", f"Error due to: {insert_result['error']}", self)


    def show(self):
        result = run_query(("SELECT * FROM supplier", ()), fetch=True)
        if result["ok"]:
            self.SupplierTable.delete(*self.SupplierTable.get_children())
            for row in result["data"]:
                self.SupplierTable.insert('', END, values=row)
        else:
            msg_manager("Error", f"Error due to: {result['error']}", self)


    def get_data(self,ev):
        f=self.SupplierTable.focus()
        content=(self.SupplierTable.item(f))
        row=content['values']
        self.var_sup_invoice.set(row[0])
        self.var_name.set(row[1])
        self.var_contact.set(row[2])
        self.txt_desc.delete('1.0',END)
        self.txt_desc.insert(END,row[3])

    def update(self):
        if not self.var_sup_invoice.get():
            msg_manager("Error", "Invoice must be required", self)
            return
        
        if not self.validate():
            return

        # Check if exists
        result = run_query(("SELECT * FROM supplier WHERE invoice=?", (self.var_sup_invoice.get(),)), fetch=True)
        if not result["ok"]:
            msg_manager("Error", f"Error due to: {result['error']}", self)
            return
        if not result["data"]:
            msg_manager("Error", "Invalid Invoice No.", self)
            return
        
        update_result = run_query((
            "UPDATE supplier SET name=?, contact=?, desc=? WHERE invoice=?",
            (
                self.var_name.get(),
                self.var_contact.get(),
                self.txt_desc.get('1.0', END),
                self.var_sup_invoice.get(),
            )
        ))
        if update_result["ok"]:
            msg_manager("Success", "Supplier Updated Successfully", self)
            self.show()
        else:
            msg_manager("Error", f"Error due to: {update_result['error']}", self)


    def delete(self):
        if not is_admin(self.user_type):
            msg_manager("Error", "Only admin can delete supplier", self)
            return

        if not self.var_sup_invoice.get():
            msg_manager("Error", "Invoice No. must be required", self)
            return

        # Check if  exists
        result = run_query(("SELECT * FROM supplier WHERE invoice=?", (self.var_sup_invoice.get(),)), fetch=True)
        if not result["ok"]:
            msg_manager("Error", f"Error due to: {result['error']}", self)
            return
        if not result["data"]:
            msg_manager("Error", "Invalid Invoice No.", self)
            return

        if msg_manager("Confirm", "Do you really want to delete?", self):
            delete_result = run_query(("DELETE FROM supplier WHERE invoice=?", (self.var_sup_invoice.get(),)))
            if delete_result["ok"]:
                msg_manager("Delete", "Supplier Deleted Successfully", self)
                self.clear()
            else:
                msg_manager("Error", f"Error due to: {delete_result['error']}", self)


    def clear(self):
        self.var_sup_invoice.set("")
        self.var_name.set("")
        self.var_contact.set("")
        self.txt_desc.delete('1.0',END)
        self.var_searchtxt.set("")
        self.show()

    def search(self):
        if not self.var_searchtxt.get():
            msg_manager("Error", "Invoice No. should be required", self)
            return

        result = run_query(("SELECT * FROM supplier WHERE invoice=?", (self.var_searchtxt.get(),)), fetch=True)
        if result["ok"]:
            if result["data"]:
                self.SupplierTable.delete(*self.SupplierTable.get_children())
                for row in result["data"]:
                    self.SupplierTable.insert('', END, values=row)
            else:
                msg_manager("Error", "No record found!!!", self)
        else:
            msg_manager("Error", f"Error due to: {result['error']}", self)

    def validate(self):
        if not self.var_name.get().strip():
            msg_manager("Error", "Name required", self)
            return False

        if not self.var_contact.get().isdigit():
            msg_manager("Error", "Contact must be numeric", self)
            return False

        return True

if __name__=="__main__":
    root=Tk()
    obj=supplierClass(root)
    root.mainloop()