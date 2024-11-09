import logging
import yt_dlp as ytdl
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, CallbackContext
from telegram.ext import CallbackContext
import os
import tempfile
import ffmpeg

# Set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Replace with your bot's token
TELEGRAM_BOT_TOKEN = '7073381155:AAHsMLX0Us5PTTFi1tKqO2ODJGrcCU-psz4'

# Function to handle the /start command
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Welcome to the music bot! Send me a song title and I\'ll fetch it for you.')

# Function to search and download the song
def search_and_play(update: Update, context: CallbackContext) -> None:
    query = ' '.join(context.args)
    if not query:
        update.message.reply_text("Please provide a song name after the command.")
        return
    
    update.message.reply_text(f"Searching for: {query}...")

    # Search for the song on YouTube and get the best match URL
    ydl_opts = {
        'format': 'bestaudio/best',
        'noplaylist': True,
        'extractaudio': True,
        'outtmpl': 'downloads/%(id)s.%(ext)s',
        'quiet': True,
    }

    with ytdl.YoutubeDL(ydl_opts) as ydl:
        try:
            info_dict = ydl.extract_info(f"ytsearch:{query}", download=False)
            video = info_dict['entries'][0]
            video_url = video['url']
            video_title = video['title']
            update.message.reply_text(f"Found: {video_title}\nNow downloading...")
            # Download audio
            ydl.download([video_url])

            # Send the audio file to Telegram
            file_path = f"downloads/{video['id']}.mp3"
            update.message.reply_audio(open(file_path, 'rb'))
            os.remove(file_path)  # Clean up downloaded file

        except Exception as e:
            update.message.reply_text("Sorry, I couldn't find a song with that name.")
            logger.error(f"Error: {e}")

# Function to handle errors
def error(update: Update, context: CallbackContext) -> None:
    logger.warning(f"Update {update} caused error {context.error}")

# Main function to set up the bot
def main():
    updater = Updater(TELEGRAM_BOT_TOKEN, use_context=True)
    
    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Add command handlers
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("play", search_and_play))

    # Log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
