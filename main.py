import asyncio
import os
import random
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler

TOKEN = os.environ["CHAT_VORONOK_TOKEN"]
PING_CHAT_ID = int(os.environ["VORONOK_PING_CHAT_ID"])

quotes = [
    "Приехал чёрный воронок. Сообщение было ликвидировано во имя спокойствия народа.",
    "Вредоносный текст уничтожен.",
    "Материал изъят и отправлен в архив.",
    "Содержание расценено как диверсия. Приняты меры.",
    "Агитация не прошла цензуру. Сообщение удалено.",
    "Речь признана подрывной. Автор под наблюдением.",
]

# заглушка для render
class PingHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"OK")

def run_http_server():
    server = HTTPServer(("0.0.0.0", 8080), PingHandler)
    server.serve_forever()

# Запуск в фоне
threading.Thread(target=run_http_server, daemon=True).start()


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message
    if not message:
        return

    if message.video_note:
        return  # разрешаем голосовые и кружочки

    try:
        username = message.from_user.username
        mention = f"@{username}" if username else "неизвестный пользователь"
        text = f"{random.choice(quotes)}\n{mention} взят на карандаш."

        await message.delete()
        await context.bot.send_message(
            chat_id=message.chat.id,
            text=text
        )

    except Exception as e:
        print(f"Ошибка: {e}")

async def autoping(app):
    await app.bot.send_message(chat_id=PING_CHAT_ID, text="🕊 Бот включён.")

    while True:
        await asyncio.sleep(300)  # каждые 5 минут
        try:
            await app.bot.send_message(chat_id=PING_CHAT_ID, text="🕊 Пинг.")
        except Exception as e:
            print(f"Ошибка при пинге: {e}")

async def post_init(app):
    app.create_task(autoping(app))

app = (
    ApplicationBuilder()
    .token(TOKEN)
    .post_init(post_init)
    .build()
)

app.add_handler(MessageHandler(filters.ALL, handle_message))

app.run_polling()
