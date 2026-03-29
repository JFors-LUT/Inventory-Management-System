from db.db_helper import run_query

# Invalid params should be rolled back
def test_regression_run_query_rolls_back_failed_insert(temp_db_path):
    
    bad_insert = run_query(("INSERT INTO category(name) VALUES(?)", ()))
    assert bad_insert["ok"] is False

    count = run_query(("SELECT COUNT(*) FROM category", ()), fetch=True)
    assert count["ok"] is True
    assert count["data"] == [(0,)]

