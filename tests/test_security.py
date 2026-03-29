from utility.security import hash_password


def test_hash_password_is_deterministic():
    password = "secret"
    h1 = hash_password(password)
    h2 = hash_password(password)

    assert h1 == h2


def test_hash_password_changes_with_input():
    h1 = hash_password("secret")
    h2 = hash_password("not secret")
    assert h1 != h2

