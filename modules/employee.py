from tkinter import*
from tkinter import ttk
from db.db_helper import run_query
from ui.ui_styles import FONT_GENERAL, APP_FONT
from ui.ui_utility import msg_manager, format_table, BaseWindow

class employeeClass(BaseWindow):
    def __init__(self,root):
        self.root=root
        self.setup_window("1100x500+320+220")

        self.init_variables()
        self.build_search()
        self.build_form()
        self.build_buttons()
        self.build_table()

        self.show()

        #------------ data & variables --------------

    def init_variables(self):
        self.var_searchby=StringVar()
        self.var_searchtxt=StringVar()
        self.var_emp_id=StringVar()
        self.var_gender=StringVar(value="Select")
        self.var_contact=StringVar()
        self.var_name=StringVar()
        self.var_dob=StringVar()
        self.var_doj=StringVar()
        self.var_email=StringVar()
        self.var_pass=StringVar()
        self.var_utype=StringVar(value="Admin")
        self.var_address=StringVar()
        self.var_salary=StringVar()


        #---------- UI -------------
    def build_search(self):
        self.frame = LabelFrame(self.root, 
            text="Search Employee", 
            font=(APP_FONT, 12, "bold"),
            bd=2, 
            relief=RIDGE, 
            bg="white")
        self.frame.place(x=250, y=20, width=600, height=70)

        #------------ options ----------------
        self.cmb_search=ttk.Combobox(self.frame,
            textvariable=self.var_searchby,
            values=("Select","Email","Name","Contact"),
            state='readonly',
            justify=CENTER,
            font=FONT_GENERAL)
        self.cmb_search.place(x=10,y=10,width=180)
        self.cmb_search.current(0)

        self.txt_search=Entry(self.frame,
            textvariable=self.var_searchtxt,
            font=FONT_GENERAL,
            bg="lightyellow")
        self.txt_search.place(x=200,y=10)

        self.btn_search=Button(self.frame,
            command=self.search,text="Search",
            font=FONT_GENERAL,
            bg="#4caf50",
            fg="white",
            cursor="hand2")
        self.btn_search.place(x=410,y=9,width=150,height=30)

    def build_form(self):
        self.title = Label(self.root,
            text="Employee Details",
            font=FONT_GENERAL,
            bg="#0f4d7d",
            fg="white")
        self.title.place(x=50,y=100,width=1000)

        #-------------- content ---------------
        #1st row, 2nd row, 3rd row, 4th row
        generic_fields = [
            ("Emp ID", self.var_emp_id, 50, 150),
            ("Contact", self.var_contact, 750, 150),
            ("Name", self.var_name, 50, 190),
            ("D.O.B.", self.var_dob, 350, 190),
            ("D.O.J.", self.var_doj, 750, 190),
            ("Email", self.var_email, 50, 230),
            ("Password", self.var_pass, 350, 230),
            ("Contact", self.var_contact, 750, 150),
            ("Salary", self.var_salary, 500, 270),
        ]
        for label, var, x, y in generic_fields:
            Label(self.root, 
                text=label, 
                font=FONT_GENERAL, 
                bg="white"
            ).place(x=x, y=y)
            #2nd row offset is 50px larger
            if label == "D.O.B." or label == "Password":
                Entry(self.root, 
                    textvariable=var, 
                    font=FONT_GENERAL,
                    bg="lightyellow"
                ).place(x=x + 150, y=y, width=180)
            else:
                Entry(self.root, 
                    textvariable=var, 
                    font=FONT_GENERAL,
                    bg="lightyellow"
                ).place(x=x + 100, y=y, width=180)

        # Combobox, select option
        self.lbl_gender=Label(
            self.root,
            text="Gender",
            font=FONT_GENERAL,
            bg="white")
        self.lbl_gender.place(x=350,y=150)

        self.cbox_gender = ttk.Combobox(self.root, textvariable=self.var_gender,
            values=("Select", "Male", "Female", "Other"),
            state='readonly', justify=CENTER,
            font=FONT_GENERAL
        )
        self.cbox_gender.place(x=500, y=150, width=180)

        self.lbl_utype=Label(
            self.root,
            text="User Type",
            font=FONT_GENERAL,
            bg="white")
        self.lbl_utype.place(x=750,y=230)

        self.cbox_utype = ttk.Combobox(self.root, textvariable=self.var_utype,
            values=("Admin", "Employee"),
            state='readonly', justify=CENTER,
            font=FONT_GENERAL
        )
        self.cbox_utype.place(x=850, y=230, width=180)

        # Address has larger box
        self.address_lbl = Label(self.root, 
            text="Address", 
            font=FONT_GENERAL, 
            bg="white")
        self.address_lbl.place(x=50, y=270)

        self.txt_address = Text(self.root, 
            font=FONT_GENERAL, 
            bg="lightyellow")
        self.txt_address.place(x=150, y=270, width=300, height=60)

    def build_buttons(self):
        actions = [
            ("Save", self.add, "#2196f3"),
            ("Update", self.update, "#4caf50"),
            ("Delete", self.delete, "#f44336"),
            ("Clear", self.clear, "#607d8b"),
        ]
        #initial position
        button_pos_x = 500
        for text, cmd, color in actions:
            Button(self.root, 
                text=text, 
                command=cmd,
                font=FONT_GENERAL, 
                bg=color, 
                fg="white",
                cursor="hand2"
            ).place(x=button_pos_x, y=305, width=110, height=28)
            #button offset
            button_pos_x += 120

    def build_table(self):
        frame = Frame(self.root, bd=3, relief=RIDGE)
        frame.place(x=0, y=350, relwidth=1, height=150)

        columns = ("eid","name","email","gender","contact","dob","doj","pass","utype","address","salary")
        names = ("EMP ID","Name","Email","Gender","Contact","D.O.B","D.O.J","Password","User Type","Address","Salary")
        widths = [90]+[100] * (len(columns)-1) 
        self.EmployeeTable = format_table(frame, columns, names, widths)

        self.EmployeeTable.bind("<ButtonRelease-1>", self.get_data)

#-----------------------------------------------------------------------------------------------------
    def add(self):
        if not self.var_emp_id.get():
            msg_manager("Error","Employee ID must be required", self)
            return
        if not self.var_salary.get().isdigit():
            msg_manager("Error","Salary should be a number", self)
            return

        # Check if employee exists
        result = run_query(("SELECT * FROM employee WHERE eid=?", (self.var_emp_id.get(),)), fetch=True)
        if not result["ok"]:
            msg_manager("Error",f"Error due to: {result['error']}", self)
            return
        if result["data"]:
            msg_manager("Error","This Employee ID is already assigned", self)
            return

        # Insert new employee
        insert_result = run_query((
            "INSERT INTO employee(eid,name,email,gender,contact,dob,doj,pass,utype,address,salary) "
            "VALUES (?,?,?,?,?,?,?,?,?,?,?)",
            (
                self.var_emp_id.get(),
                self.var_name.get(),
                self.var_email.get(),
                self.var_gender.get(),
                self.var_contact.get(),
                self.var_dob.get(),
                self.var_doj.get(),
                self.var_pass.get(),
                self.var_utype.get(),
                self.txt_address.get('1.0', END),
                self.var_salary.get(),
            )
        ))
        if insert_result["ok"]:
            msg_manager("Success", "Employee Added Successfully", self)
            self.clear()
            self.show()
        else:
            msg_manager("Error",f"Error due to: {insert_result['error']}", self)

    def show(self):
        result = run_query(("SELECT * FROM employee", ()), fetch=True)
        if result["ok"]:
            self.EmployeeTable.delete(*self.EmployeeTable.get_children())
            for row in result["data"]:
                self.EmployeeTable.insert('', END, values=row)
        else:
            msg_manager("Error",f"Error due to: {result['error']}", self)




    def get_data(self,ev):
        f=self.EmployeeTable.focus()
        content=(self.EmployeeTable.item(f))
        row=content['values']
        self.var_emp_id.set(row[0])
        self.var_name.set(row[1])
        self.var_email.set(row[2])
        self.var_gender.set(row[3])
        self.var_contact.set(row[4])
        self.var_dob.set(row[5])
        self.var_doj.set(row[6])
        self.var_pass.set(row[7])
        self.var_utype.set(row[8])
        self.txt_address.delete('1.0',END)
        self.txt_address.insert(END,row[9])
        self.var_salary.set(row[10])

    
    def update(self):
        if not self.var_emp_id.get():
            msg_manager("Error","Employee ID must be required", self)
            return
        
        if not self.var_salary.get().isdigit():
            msg_manager("Error","Salary should be a number", self)
            return

        # Check if employee exists
        result = run_query(("SELECT * FROM employee WHERE eid=?", (self.var_emp_id.get(),)), fetch=True)
        if not result["ok"]:
            msg_manager("Error",f"Error due to: {result['error']}", self)
            return
        if not result["data"]:
            msg_manager("Error","Invalid Employee ID", self)
            return

        # Update employee
        update_result = run_query((
            "UPDATE employee SET name=?,email=?,gender=?,contact=?,dob=?,doj=?,pass=?,utype=?,address=?,salary=? "
            "WHERE eid=?",
            (
                self.var_name.get(),
                self.var_email.get(),
                self.var_gender.get(),
                self.var_contact.get(),
                self.var_dob.get(),
                self.var_doj.get(),
                self.var_pass.get(),
                self.var_utype.get(),
                self.txt_address.get('1.0', END),
                self.var_salary.get(),
                self.var_emp_id.get(),
            )
        ))
        if update_result["ok"]:
            msg_manager("Success", "Employee Updated Successfully", self)
            self.show()
        else:
            msg_manager("Error",f"Error due to: {update_result['error']}", self)

    def delete(self):
        if not self.var_emp_id.get():
            msg_manager("Error","Employee ID must be required", self)
            return

        # Check if employee exists
        result = run_query(("SELECT * FROM employee WHERE eid=?", (self.var_emp_id.get(),)), fetch=True)
        if not result["ok"]:
            msg_manager("Error",f"Error due to: {result['error']}", self)
            return
        if not result["data"]:
            msg_manager("Error","Invalid Employee ID", self)
            return

        # Confirm deletion
        if msg_manager("Confirm", "Do you really want to delete?", self):
            delete_result = run_query(("DELETE FROM employee WHERE eid=?", (self.var_emp_id.get(),)))
            if delete_result["ok"]:
                msg_manager("Delete", "Employee Deleted Successfully", self)
                self.clear()
            else:
                msg_manager("Error",f"Error due to: {delete_result['error']}", self)


    def clear(self):
        self.var_emp_id.set("")
        self.var_name.set("")
        self.var_email.set("")
        self.var_gender.set("Select")
        self.var_contact.set("")
        self.var_dob.set("")
        self.var_doj.set("")
        self.var_pass.set("")
        self.var_utype.set("Admin")
        self.txt_address.delete('1.0',END)
        self.var_salary.set("")
        self.var_searchby.set("Select")
        self.var_searchtxt.set("")
        self.show()

    def search(self):
        if self.var_searchby.get() == "Select":
            msg_manager("Error","Select Search By option", self)
            return
        if not self.var_searchtxt.get():
            msg_manager("Error","Search input should be required", self)
            return

        sql = f"SELECT * FROM employee WHERE {self.var_searchby.get()} LIKE ?"
        pattern = f"%{self.var_searchtxt.get()}%"
        result = run_query((sql, (pattern,)), fetch=True)
        if result["ok"]:
            if result["data"]:
                self.EmployeeTable.delete(*self.EmployeeTable.get_children())
                for row in result["data"]:
                    self.EmployeeTable.insert('', END, values=row)
            else:
                msg_manager("Error","No record found!!!", self)
        else:
            msg_manager("Error",f"Error due to: {result['error']}", self)

if __name__=="__main__":
    root=Tk()
    obj=employeeClass(root)
    root.mainloop()