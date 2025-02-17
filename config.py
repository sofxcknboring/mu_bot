from dotenv import load_dotenv
import os
load_dotenv()

# Токен бота и провайдера:
BOT_TOKEN = os.getenv("BOT_TOKEN")
PROVIDER_TOKEN = os.getenv("PROVIDER_TOKEN")
PROVIDER_TEST_TOKEN = os.getenv("PROVIDER_TEST_TOKEN")

# ID частного канала:
channel_id = os.getenv("CHANNEL_ID")

# Start message
start_message = f"""
ТЕКСТ
"""


# Product settings
product_title = "123"
product_description = """
123
"""
product_photo = "https://img.freepik.com/free-vector/set-make-up-accessories-drawing_24640-46682.jpg"

# Настройка цен для товара:
# online course -> подписка.
price = 10000 # 5990.00 RUB -> цена без учёта скидок.
hot_price = 10000 # 4990.00 RUB -> цена с учётом скидок.
discount = 0 # 2000.00 RUB -> скидка для пользователей, которые уже покупали подписку.
# discount = 579999 # тест payment



# purchase reporting
# start_parameter и payload помогают уникально идентифицировать транзакцию и связать ее с процессом оплаты.
product_start_parameter="online-makeup-course"
product_payload="invoice-payload"
