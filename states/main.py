from aiogram.dispatcher.filters.state import State, StatesGroup


class ShopState(StatesGroup):
    category = State()
    product = State()
    amount = State()
    cart = State()
    tolov = State()
    admin_panel = State()
    insert_category = State()
    about = State()
    about_faq = State()
    sozlamalar = State()
    soz_photo = State()
    soz_name = State()
    soz_username = State()
    soz_phone = State()
    soz_loc = State()
    soz_loc_auto = State()
    soz_loc_write = State()
    
    
class Admin(StatesGroup):
    del_users = State()
    del_products_cat = State()
    del_products_pro = State()
    del_cats = State()
    del_all = State()

    reklama = State()
    photo_rek = State()
    text_rek = State()

    get_name = State()
    get_desc = State()
    get_photo = State()
    get_price = State()
    get_hm = State()
    get_cat_id = State()
    add_to_db = State()
    
    
    