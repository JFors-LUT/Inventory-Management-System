from db.db_helper import is_admin, run_query
from modules.category import categoryClass
from ui.ui_utility import BaseWindow


class DummyVarr:
    def __init__(self, value=""):
        self._value = value

    def get(self):
        return self._value

    def set(self, value):
        self._value = value


class DummyWidget:
    def __init__(self):
        self.kwargs = {}

    def config(self, **kwargs):
        self.kwargs.update(kwargs)


def test_is_admin_helper():
    assert is_admin("Admin") is True
    assert is_admin("Employee") is False

    # Dashboard uses restrict_admin for employee window
def test_non_admin_employee_gui_is_restricted():
    window = BaseWindow()
    window.user_type = "Employee"
    widget = DummyWidget()

    window.restrict_admin(widget)

    assert widget.kwargs["state"] == "disabled"
    assert widget.kwargs["disabledforeground"] == "gray"
    assert widget.kwargs["cursor"] == "arrow"


def test_non_admin_cannot_delete_category(temp_db_path, monkeypatch):
    run_query(("INSERT INTO category(name) VALUES(?)", ("Phone",)))
    row = run_query(("SELECT cid FROM category WHERE name=?", ("Phone",)), fetch=True)
    cid = str(row["data"][0][0])

    calls = []

    def dummy_msg(kind, msg, _self):
        calls.append((kind, msg))
        return False

    monkeypatch.setattr("modules.category.msg_manager", dummy_msg)

    category = categoryClass.__new__(categoryClass)
    category.user_type = "Employee"
    category.var_cat_id = DummyVarr(cid)
    category.var_name = DummyVarr("Phone")

    category.delete()

    after = run_query(("SELECT COUNT(*) FROM category WHERE cid=?", (cid,)), fetch=True)
    assert after["data"][0][0] == 1
    assert ("Error", "Only admin can delete category") in calls


def test_admin_can_delete_category(temp_db_path, monkeypatch):
    run_query(("INSERT INTO category(name) VALUES(?)", ("Phone",)))
    row = run_query(("SELECT cid FROM category WHERE name=?", ("Phone",)), fetch=True)
    cid = str(row["data"][0][0])

    def dummy_msg(kind, _msg, _self):
        if kind == "Confirm":
            return True
        return None

    monkeypatch.setattr("modules.category.msg_manager", dummy_msg)

    category = categoryClass.__new__(categoryClass)
    category.user_type = "Admin"
    category.var_cat_id = DummyVarr(cid)
    category.var_name = DummyVarr("Phone")
    category.clear = lambda: None

    category.delete()

    after = run_query(("SELECT COUNT(*) FROM category WHERE cid=?", (cid,)), fetch=True)
    assert after["data"][0][0] == 0

