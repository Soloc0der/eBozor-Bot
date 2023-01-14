from dataclasses import dataclass
from aiogram.types import LabeledPrice
from typing import List
from data import config


@dataclass
class Product:
    title: str
    description: str
    start_parameter: str
    currency: str
    prices: List[LabeledPrice]
    provider_data: dict = None
    photo_url: int = None
    photo_size: int = None
    photo_width: int = None
    photo_heihgt: int = None
    need_name: bool = False
    need_phone_number: bool = False
    need_email: bool = False
    need_shipping_adsress: bool = False
    sent_phone_number_to_provider: bool = False
    sent_email_to_provider: bool = False
    is_flexible: bool = False


    provider_token = config.PROVIDER_TOKEN

    def generate_invoice(self):
        return self.__dict__
        
    
    

