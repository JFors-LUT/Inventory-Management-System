MENU_FONT = "times new roman"
APP_FONT = "goudy old style"


# ---- fonts ----
# ---- dashboard fonts ----
FONT_TITLE = (MENU_FONT, 40, "bold")
FONT_MENU_BTN = (MENU_FONT, 20, "bold")
FONT_MENU_LBL = (APP_FONT, 20, "bold")

# ---- default fonts ----
FONT_TITLE_LBL = (APP_FONT, 20, "bold")
FONT_GENERAL = (APP_FONT, 15)

# ---- sales button font -----
FONT_SALES_BTN = (APP_FONT, 15, "bold")

# ---- product title font ----
FONT_PRODUCT_TITLE = (APP_FONT, 18)

# ---- billing fonts ----
FONT_BILLING_PRIMARY = MENU_FONT
FONT_BILLING_SECONDARY = APP_FONT

# ---- colors ----
COLOR_PRIMARY = "#010c48"
COLOR_SECONDARY = "#4d636d"
COLOR_ACCENT = "#009688"
COLOR_WHITE = "white"
COLOR_WARNING = "yellow"

# ---- common styles ----
BUTTON_MENU = {
    "font": FONT_MENU_BTN,
    "bg": COLOR_WHITE,
    "bd": 3,
    "cursor": "hand2",
    "compound": "left",
    "anchor": "w",
    "padx": 5
}

LABEL_CARD = {
    "bd": 5,
    "relief": "ridge",
    "fg": "white",
    "font": FONT_MENU_LBL
}