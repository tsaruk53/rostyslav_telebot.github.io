from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from googleapiclient.discovery import build
import random

# === ТВОЇ КЛЮЧІ ===
TOKEN = "7922312181:AAGMFWZXnx6gqoDYjwprogWKknvYfDnoYQ8"
YOUTUBE_API_KEY = "AIzaSyBOlCfpH5hRB7ww6iglaFweG--O0P42gVE"

# === YouTube API ===
youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)

# === ЖАНРИ ===
genres = ["pop", "rock", "hip-hop", "jazz", "classical", "indie", "electronic", "country", "metal", "latin"]

# === ПОШУК НА YOUTUBE ===
def search_youtube(query, limit=3):
    request = youtube.search().list(
        part="snippet",
        q=f"{query} official music video -mix -playlist",
        type="video",
        videoDuration="short",  # тільки короткі (до 4 хв)
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

# === КАТЕГОРІЇ ===
def get_random_track():
    return search_youtube(random.choice(genres), 1)

def get_ukrainian_song():
    return search_youtube("українська пісня official video", 1)

def get_english_song():
    return search_youtube("english pop song official video", 1)

def get_funny_song():
    return search_youtube("весела українська пісня official video", 1)

def get_fonk_song():
    return search_youtube("phonk song official video", 1)

def get_makskorzh_song():
    return search_youtube("Макс Корж official video", 1)

# === /start ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        ["🎲 Випадкова пісня", "🎵 Українська", "🎧 Англійська"],
        ["😄 Веселі 🇺🇦", "🔥 Фонк", "🎤 Макс Корж"],
        ["🔍 Пошук музики"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text("Привіт! Обери, що послухати 🎶", reply_markup=reply_markup)

# === ОБРОБКА ПОВІДОМЛЕНЬ ===
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if text == "🔍 Пошук музики":
        await update.message.reply_text("Введи назву пісні або виконавця 🎵")
    elif text == "🎲 Випадкова пісня":
        await update.message.reply_text(f"🎲 Ось твоя пісня:\n{get_random_track()}")
    elif text == "🎵 Українська":
        await update.message.reply_text(f"🇺🇦 Українська пісня:\n{get_ukrainian_song()}")
    elif text == "🎧 Англійська":
        await update.message.reply_text(f"🇬🇧 Англійська пісня:\n{get_english_song()}")
    elif text == "😄 Веселі 🇺🇦":
        await update.message.reply_text(f"😂 Весела пісня:\n{get_funny_song()}")
    elif text == "🔥 Фонк":
        await update.message.reply_text(f"😎 Фонк-трек:\n{get_fonk_song()}")
    elif text == "🎤 Макс Корж":
        await update.message.reply_text(f"🎤 Випадкова пісня Макса Коржа:\n{get_makskorzh_song()}")
    else:
        search_results = search_youtube(text, 3)
        await update.message.reply_text(f"🔍 Знайдено:\n{search_results}")

# === ОСНОВНИЙ КОД ===
if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Бот запущено! ✅")
    app.run_polling()
