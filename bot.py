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
def search_youtube(query):
    # створюємо пошук по ключових словах
    random_suffix = random.choice(["song", "track", "music", "official video", "hit", "clip"])
    search_query = f"{query} {random_suffix} -playlist -mix"

    # отримуємо список відео
    request = youtube.search().list(
        part="snippet",
        q=search_query,
        type="video",
        videoDuration="short",
        maxResults=50
    )
    response = request.execute()
    videos = response.get("items", [])

    if not videos:
        return "Нічого не знайдено 😞"

    # далі отримаємо статистику переглядів для кожного відео
    video_ids = [v["id"]["videoId"] for v in videos]
    stats_request = youtube.videos().list(
        part="statistics,snippet",
        id=",".join(video_ids)
    )
    stats_response = stats_request.execute()

    # відфільтруємо тільки відео з >100 млн переглядів
    popular_videos = []
    for item in stats_response.get("items", []):
        stats = item.get("statistics", {})
        if int(stats.get("viewCount", 0)) > 100_000_000:
            title = item["snippet"]["title"]
            video_id = item["id"]
            url = f"https://www.youtube.com/watch?v={video_id}"
            popular_videos.append(f"{title}\n🎧 {url}")

    if not popular_videos:
        return "Не знайшов пісень з 100+ млн переглядів 😞"

    # повертаємо випадкову популярну пісню
    return random.choice(popular_videos)


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
