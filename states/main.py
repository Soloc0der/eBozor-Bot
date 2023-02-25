from aiogram.dispatcher.filters.state import State, StatesGroup


class ShopState(StatesGroup):
    category = State()
    product = State()
    amount = State()
    cart = State()
    tolov = State()
    admin_panel = State()
    insert_category = State()
    
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
    
    
    