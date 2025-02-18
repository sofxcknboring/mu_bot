from dotenv import load_dotenv
import os
load_dotenv()

# Токен бота и провайдера:
BOT_TOKEN = os.getenv("BOT_TOKEN")
TEST_BOT_TOKEN = os.getenv("TEST_BOT_TOKEN")
PROVIDER_TOKEN = os.getenv("PROVIDER_TOKEN")
PROVIDER_TEST_TOKEN = os.getenv("PROVIDER_TEST_TOKEN")
V_PROVIDER_TOKEN = os.getenv("V_PROVIDER_TOKEN ")

# ID частного канала:
channel_id = os.getenv("CHANNEL_ID")

v_channel_id = os.getenv("TEST_CHANNEL_ID_2")

# Start message
start_message = f"""
Дарова
"""


# Product settings
product_title = "Товар"
product_description = """
Описание
"""
product_photo = ""

# Настройка цен для товара:
# online course -> подписка.
price = 599000 # 5990.00 RUB -> цена без учёта скидок.
hot_price = 499000 # 4990.00 RUB -> цена с учётом скидок.
discount = 200000 # 2000.00 RUB -> скидка для пользователей, которые уже покупали подписку.
# discount = 579999 # тест payment



# purchase reporting
# start_parameter и payload помогают уникально идентифицировать транзакцию и связать ее с процессом оплаты.
product_start_parameter="online-makeup-course"
product_payload="invoice-payload"
