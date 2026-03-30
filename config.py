import os
# ------------------ BASE PATH SETUP ------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

ASSETS_DIR = os.path.join(BASE_DIR, "assets")
IMAGE_DIR = os.path.join(ASSETS_DIR, "images")

DATA_DIR = os.path.join(BASE_DIR, "data")
BILL_DIR = os.path.join(DATA_DIR, "bill")
DB_DIR = os.path.join(DATA_DIR, "db")

DB_PATH = os.path.join(DB_DIR, "ims.db")


# ----------- MK BILL DIRECTORY ------------
os.makedirs(BILL_DIR, exist_ok=True)