from db.db_helper import run_query

#Not tuple
def test_run_query_requires_tuple_command():
    #not tuple
    result = run_query("SELECT 1", fetch=True)
    assert result["ok"] is False
    assert "Command must be a tuple" in result["error"]

    #wrong length tuple
    result = run_query(("SELECT * FROM products",))
    assert result["ok"] is False
    assert "Command must be a tuple" in result["error"]


#Insert and fetch row
def test_run_query_returns_rows_when_fetch_true(temp_db_path):
    insert = run_query(
        (
            "INSERT INTO category(name) VALUES(?)", ("Phone",),
        )
    )
    assert insert["ok"] is True

    result = run_query(("SELECT name FROM category WHERE name=?", ("Phone",)), fetch=True)
    assert result["ok"] is True
    assert result["data"] == [("Phone",)]

