from tkinter import *
from db.db_helper import run_query
from ui.ui_utility import msg_manager, BaseWindow
from ui.ui_styles import FONT_GENERAL, APP_FONT
from utility.security import hash_password



class LoginSystem(BaseWindow):
    def __init__(self, root, dashboard=True):
        self.root = root
        self.setup_window("400x300+500+200")
        self.root.title("Login")
        self.launcher = dashboard

        # -------- variables --------
        self.var_email = StringVar()
        self.var_password = StringVar()

        # -------- UI --------
        self.build_ui()

    def build_ui(self):
        title = Label(
            self.root,
            text="Login System",
            font=(APP_FONT, 20),
            bg="#0f4d7d",
            fg="white"
        )
        title.pack(side=TOP, fill=X)

        frame = Frame(self.root, bd=2, relief=RIDGE, bg="white")
        frame.place(x=50, y=70, width=300, height=180)

        lbl_email = Label(frame, text="Email", font=FONT_GENERAL, bg="white")
        lbl_email.place(x=20, y=20)

        txt_email = Entry(
            frame,
            textvariable=self.var_email,
            font=FONT_GENERAL,
            bg="lightyellow"
        )
        txt_email.place(x=100, y=20, width=180)

        lbl_pass = Label(frame, text="Password", font=FONT_GENERAL, bg="white")
        lbl_pass.place(x=20, y=70)

        txt_pass = Entry(
            frame,
            textvariable=self.var_password,
            font=FONT_GENERAL,
            bg="lightyellow",
            show="*"
        )
        txt_pass.place(x=100, y=70, width=180)

        btn_login = Button(
            frame,
            text="Login",
            command=self.login,
            font=FONT_GENERAL,
            bg="#4caf50",
            fg="white",
            cursor="hand2"
        )
        btn_login.place(x=20, y=120, width=120, height=30)

        btn_exit = Button(
            frame,
            text="Exit",
            command=self.root.destroy,
            font=FONT_GENERAL,
            bg="#f44336",
            fg="white",
            cursor="hand2"
        )
        btn_exit.place(x=160, y=120, width=120, height=30)

    # -------- login logic --------
    def login(self):
        email = self.var_email.get().strip()
        password = self.var_password.get().strip()

        if not email or not password:
            msg_manager("Error", "All fields are required", self)
            return

        hashed = hash_password(password)

        result = run_query((
            "SELECT name, utype FROM employee WHERE email=? AND pass=?",
            (email, hashed)
        ), fetch=True)

        if not result["ok"]:
            msg_manager("Error", f"Error: {result['error']}", self)
            return

        if result["data"]:
            user_name, user_type = result["data"][0]

            msg_manager("Success", f"Welcome {user_name}", self)

            # ---- open main app ----
            self.root.destroy()

            from tkinter import Tk
            if self.launcher:
                from dashboard import IMS 

                new_root = Tk()
                app = IMS(new_root, user_name, user_type)
                new_root.mainloop()
            else:
                from billing import billClass 
                new_root = Tk()
                app = billClass(new_root, user_name, user_type, self.launcher)
                new_root.mainloop()

        else:
            msg_manager("Error", "Invalid email or password", self)


# -------- run standalone --------
if __name__ == "__main__":
    root = Tk()
    app = LoginSystem(root)
    root.mainloop()