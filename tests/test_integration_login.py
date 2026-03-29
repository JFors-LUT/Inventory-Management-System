from db.db_helper import run_query
from utility.security import hash_password


def test_login_query_with_correct_password(temp_db_path):
    email = "alice@example.com"
    password = "pass123"
    hashed = hash_password(password)

    # insert test user
    run_query((
        "INSERT INTO employee(name,email,gender,contact,dob,doj,pass,utype,address,salary) "
        "VALUES (?,?,?,?,?,?,?,?,?,?)",
        ("Alice Bob", email, "Other", "0401234567", "1995-05-10",
         "2026-01-01", hashed, "Admin", "Lappeenranta", "4321")
    ))

    result = run_query((
        "SELECT name, utype FROM employee WHERE email=? AND pass=?",
        (email, hashed)
    ), fetch=True)

    assert result["ok"]
    assert result["data"] == [("Alice Bob", "Admin")]


class DummyVarr:
    def __init__(self, value):
        self._value = value

    def get(self):
        return self._value


class _FakeRoot:
    def __init__(self):
        self.destroy_called = False

    def destroy(self):
        self.destroy_called = True


class _FakeTk:
    def mainloop(self):
        return None

#username and type is passed from login to dashboard class and from there to employee class
def test_login_passes_user_to_dashboard(monkeypatch):
    from modules.login import LoginSystem
    import dashboard
    import tkinter

    captured = {}

    monkeypatch.setattr("modules.login.msg_manager", lambda *a, **k: None)
    monkeypatch.setattr(
        "modules.login.run_query",
        lambda *_, **__: {"ok": True, "data": [("Alice Bob", "Admin")]}
    )

    class DummyTk:
        def mainloop(self):
            pass

    monkeypatch.setattr(tkinter, "Tk", DummyTk)

    class DummyIMS:
        def __init__(self, root, user_name, user_type):
            captured["name"] = user_name
            captured["type"] = user_type

    monkeypatch.setattr(dashboard, "IMS", DummyIMS)

    login = LoginSystem.__new__(LoginSystem)
    login.root = type("R", (), {"destroy": lambda self: None})()
    login.var_email = DummyVarr("a")
    login.var_password = DummyVarr("b")
    login.launcher = True

    login.login()

    assert captured["name"] == "Alice Bob"
    assert captured["type"] == "Admin"

def test_dashboard_passes_user_to_employee(monkeypatch):
    import dashboard

    captured = {}

    monkeypatch.setattr(dashboard, "Toplevel", lambda _: object())

    class DummyEmployee:
        def __init__(self, _, name, user_type):
            captured["name"] = name
            captured["type"] = user_type

    monkeypatch.setattr(dashboard, "employeeClass", DummyEmployee)

    ims = dashboard.IMS.__new__(dashboard.IMS)
    ims.root = object()
    ims.user = "Alice Bob"
    ims.user_type = "Admin"

    dashboard.IMS.employee(ims)

    assert captured["name"] == "Alice Bob"
    assert captured["type"] == "Admin"
