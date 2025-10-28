from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from googleapiclient.discovery import build
import random

# === ТВОЇ КЛЮЧІ ===
TOKEN = "7922312181:AAGMFWZXnx6gqoDYjwprogWKknvYfDnoYQ8"
YOUTUBE_API_KEY = "AIzaSyBOlCfpH5hRB7ww6iglaFweG--O0P42gVE"

# === Ініціалізація YouTube API ===
youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)

# === ФУНКЦІЯ ПОШУКУ НА YOUTUBE ===
def search_youtube(query):
    random_suffix = random.choice(["song", "track", "official music video", "hit", "clip"])
    search_query = f"{query} {random_suffix} -playlist -mix"

    # 1️⃣ шукаємо до 50 відео
    request = youtube.search().list(
        part="snippet",
        q=search_query,
        type="video",
        videoDuration="short",  # короткі треки (до ~4 хв)
        maxResults=50
    )
    response = request.execute()
    videos = response.get("items", [])
    if not videos:
        return "Нічого не знайдено 😞"

    # 2️⃣ отримуємо статистику
    video_ids = [v["id"]["videoId"] for v in videos]
    stats_request = youtube.videos().list(
        part="statistics,snippet,contentDetails",
        id=",".join(video_ids)
    )
    stats_response = stats_request.execute()

    # 3️⃣ фільтрація по переглядах >10 млн
    popular_videos = []
    for item in stats_response.get("items", []):
        stats = item.get("statistics", {})
        view_count = int(stats.get("viewCount", 0))
        title = item["snippet"]["title"]
        video_id = item["id"]
        url = f"https://www.youtube.com/watch?v={video_id}"

        if view_count > 10_000_000:
            popular_videos.append(f"{title}\n🎧 {url}")

    # 4️⃣ fallback якщо немає таких відео
    if not popular_videos:
        item = random.choice(stats_response.get("items", []))
        title = item["snippet"]["title"]
        url = f"https://www.youtube.com/watch?v={item['id']}"
        return f"{title}\n🎧 {url}"

    # 5️⃣ випадкова популярна пісня
    return random.choice(popular_videos)

# === КОМАНДА /start ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        ["🎲 Випадкова пісня", "🎧 Англійські пісні"],
        ["🇺🇦 Українські пісні", "🎉 Веселі українські"],
        ["🎤 Макс Корж", "💿 Фонк"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text("Привіт! Обери, що послухати 👇", reply_markup=reply_markup)

# === ОБРОБКА ПОВІДОМЛЕНЬ ===
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text

    if user_input == "🎲 Випадкова пісня":
        song = search_youtube(random.choice(["music", "song", "top hit"]))
        await update.message.reply_text(f"🎲 Випадкова пісня:\n{song}")

    elif user_input == "🎧 Англійські пісні":
        song = search_youtube(random.choice(["English pop", "rock hits", "rap song", "R&B hit"]))
        await update.message.reply_text(f"🇺🇸 Англійська пісня:\n{song}")

    elif user_input == "🇺🇦 Українські пісні":
        song = search_youtube(random.choice(["українська пісня", "українська музика", "український хіт"]))
        await update.message.reply_text(f"🇺🇦 Українська пісня:\n{song}")

    elif user_input == "🎉 Веселі українські":
        song = search_youtube(random.choice(["весела українська пісня", "гумористична пісня", "смішна українська пісня"]))
        await update.message.reply_text(f"🎉 Весела пісня:\n{song}")

    elif user_input == "🎤 Макс Корж":
        song = search_youtube("Макс Корж")
        await update.message.reply_text(f"🎤 Макс Корж:\n{song}")

    elif user_input == "💿 Фонк":
        song = search_youtube(random.choice(["phonk", "drift phonk", "gym phonk"]))
        await update.message.reply_text(f"💿 Фонк трек:\n{song}")

    else:
        song = search_youtube(user_input)
        await update.message.reply_text(f"🔍 Знайдено:\n{song}")

# === ЗАПУСК ===
if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Бот запущено! ✅")
    app.run_polling()
