from modules.product import productClass


class DummyVar:
    def __init__(self, value):
        self._value = value

    def get(self):
        return self._value


def test_product_validate_rejects_non_numeric_price(monkeypatch):
    # Prevent GUI message popups during validation.
    monkeypatch.setattr("modules.product.msg_manager", lambda *args, **kwargs: None)

    prod = productClass.__new__(productClass)
    prod.var_name = DummyVar("iPhone")
    prod.var_price = DummyVar("LUT")
    prod.var_qty = DummyVar("5")
    prod.var_cat = DummyVar("Smartphones")
    prod.var_sup = DummyVar("Apple Inc.")

    assert prod.validate() is False

def test_product_validate_rejects_non_numeric_quantity(monkeypatch):
    # Prevent GUI message popups during validation.
    monkeypatch.setattr("modules.product.msg_manager", lambda *args, **kwargs: None)

    prod = productClass.__new__(productClass)
    prod.var_name = DummyVar("iPhone")
    prod.var_price = DummyVar("1595")
    prod.var_qty = DummyVar("sixseven")
    prod.var_cat = DummyVar("Smartphones")
    prod.var_sup = DummyVar("Apple Inc.")

    assert prod.validate() is False


def test_product_validate_rejects_negative_quantity(monkeypatch):
    monkeypatch.setattr("modules.product.msg_manager", lambda *args, **kwargs: None)

    prod = productClass.__new__(productClass)
    prod.var_name = DummyVar("iPhone")
    prod.var_price = DummyVar("100")
    prod.var_qty = DummyVar("-1")
    prod.var_cat = DummyVar("Smartphones")
    prod.var_sup = DummyVar("Apple Inc.")

    assert prod.validate() is False

def test_product_validate_rejects_select_option(monkeypatch):
    monkeypatch.setattr("modules.product.msg_manager", lambda *args, **kwargs: None)

    prod = productClass.__new__(productClass)
    prod.var_name = DummyVar("iPhone")
    prod.var_price = DummyVar("100")
    prod.var_qty = DummyVar("-1")
    prod.var_caty = DummyVar("Select")
    prod.var_sup = DummyVar("Apple Inc.")

    assert prod.validate() is False



def test_product_validate_respects_correct_values_decimal(monkeypatch):
    monkeypatch.setattr("modules.product.msg_manager", lambda *args, **kwargs: None)

    prod = productClass.__new__(productClass)
    prod.var_name = DummyVar("iPhone")
    prod.var_price = DummyVar("11.99")
    prod.var_qty = DummyVar("2500")
    prod.var_cat = DummyVar("Smartphones")
    prod.var_sup = DummyVar("Apple Inc.")

    assert prod.validate() is True



