import os
import random
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

TOKEN = os.environ["CHAT_VORONOK_TOKEN"]

quotes = [
    "Приехал чёрный воронок. Сообщение было ликвидировано во имя спокойствия народа.",
    "Вредоносный текст уничтожен.",
    "Материал изъят и отправлен в архив.",
    "Содержание расценено как диверсия. Приняты меры.",
    "Агитация не прошла цензуру. Сообщение удалено.",
    "Речь признана подрывной. Автор под наблюдением.",
]

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

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(MessageHandler(filters.ALL, handle_message))

app.run_polling()