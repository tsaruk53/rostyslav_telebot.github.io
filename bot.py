from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from googleapiclient.discovery import build
import random

# === ТВОЇ КЛЮЧІ ===
TOKEN = "7922312181:AAGMFWZXnx6gqoDYjwprogWKknvYfDnoYQ8"
YOUTUBE_API_KEY = "AIzaSyBOlCfpH5hRB7ww6iglaFweG--O0P42gVE"

# === Ініціалізація YouTube API ===
youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)

# === ЖАНРИ ДЛЯ ВИПАДКОВИХ ПІСЕНЬ ===
genres = ["pop", "rock", "hip-hop", "jazz", "classical", "indie", "electronic", "country", "metal", "latin"]

# === ФУНКЦІЯ ПОШУКУ НА YOUTUBE ===
def search_youtube(query, limit=3):
    request = youtube.search().list(
        part="snippet",
        q=query,
        type="video",
        maxResults=limit
    )
    response = request.execute()

    if not response["items"]:
        return "Нічого не знайдено 😞"

    result_text = ""
    for idx, item in enumerate(response["items"], start=1):
        title = item["snippet"]["title"]
        video_id = item["id"]["videoId"]
        url = f"https://www.youtube.com/watch?v={video_id}"
        result_text += f"{idx}. {title}\n🎧 {url}\n\n"

    return result_text.strip()

# === ФУНКЦІЯ ДЛЯ ВИПАДКОВОЇ ПІСНІ ===
def get_random_track():
    random_genre = random.choice(genres)
    return search_youtube(random_genre, limit=1)

# === КОМАНДА /start ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [["🔍 Пошук музики", "🎲 Випадкова пісня"]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text("Привіт! Обери, що зробити 👇", reply_markup=reply_markup)

# === ОБРОБКА ПОВІДОМЛЕНЬ ===
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text

    if user_input == "🔍 Пошук музики":
        await update.message.reply_text("Введи назву пісні або виконавця 🎵")
    elif user_input == "🎲 Випадкова пісня":
        song = get_random_track()
        await update.message.reply_text(f"🎲 Випадкова пісня:\n{song}")
    else:
        search_results = search_youtube(user_input, limit=3)
        await update.message.reply_text(f"🔍 Знайдено:\n{search_results}")

# === ОСНОВНИЙ КОД ===
if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Бот запущено! ✅")
    app.run_polling()
