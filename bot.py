from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from spotipy import Spotify
from spotipy.oauth2 import SpotifyClientCredentials
import random

# Spotify API налаштування
SPOTIFY_CLIENT_ID = "9a4f559d233d4529a98777969954fc54"
SPOTIFY_CLIENT_SECRET = "a6e14fe3e6104e269041e42644a0fa8c"

spotify = Spotify(auth_manager=SpotifyClientCredentials(
    client_id=SPOTIFY_CLIENT_ID,
    client_secret=SPOTIFY_CLIENT_SECRET
))

# Функція для випадкової пісні
def get_random_track():
    genres = ["pop", "rock", "hip-hop", "jazz", "classical", "indie", "electronic", "country", "metal", "latin"]
    random_genre = random.choice(genres)

    results = spotify.search(q=f"genre:{random_genre}", type="track", limit=50)
    if results['tracks']['items']:
        track = random.choice(results['tracks']['items'])
        return f"{track['name']} - {track['artists'][0]['name']}\nСлухати: {track['external_urls']['spotify']}"
    else:
        return "Не вдалося знайти випадкову пісню 😞"

# Telegram-бот
TOKEN = "7922312181:AAGMFWZXnx6gqoDYjwprogWKknvYfDnoYQ8"

# Стартова команда
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        ["🔍 Пошук музики", "🎲 Випадкова пісня"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text(
        "Привіт! Яку пісню хочеш послухати сьогодні:", reply_markup=reply_markup
    )

# Обробка повідомлень
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text

    if user_input == "🔍 Пошук музики":
        await update.message.reply_text("Напишіть назву пісні або виконавця для пошуку.")
    elif user_input == "🎲 Випадкова пісня":
        random_song = get_random_track()
        await update.message.reply_text(f"🎲 Випадкова пісня:\n{random_song}")
    else:
        # Пошук за введеним текстом
        results = spotify.search(q=user_input, type="track", limit=3)
        if results['tracks']['items']:
            search_results = "🔍 Знайдено:\n"
            for idx, track in enumerate(results['tracks']['items']):
                search_results += (
                    f"{idx + 1}. {track['name']} - {track['artists'][0]['name']}\n"
                    f"Слухати: {track['external_urls']['spotify']}\n\n"
                )
            await update.message.reply_text(search_results)
        else:
            await update.message.reply_text("Нічого не знайдено 😞")

# Основний код
if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()

    # Обробники
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Бот запущено!")
    app.run_polling()
