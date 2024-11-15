from flask import Flask, request
import os
import youtube_dl
from telegram import Bot
from telegram.ext import Updater, CommandHandler
import requests
 

query = 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'

ydl_opts = {
    'cookies': 'cookies.txt',  # Use the path to your cookies file
}

with youtube_dl.YoutubeDL(ydl_opts) as ydl:
    try:
        info_dict = ydl.extract_info(query, download=False)
        print(info_dict)
    except youtube_dl.utils.DownloadError as e:
        print(f"Error: {e}")

# Set up the Flask app
app = Flask(__name__)

# Telegram bot token and bot object
TOKEN = '7073593799:AAEBjG7JZeiV_2n5MMeRHpxEx1bI_hpY7p0'
bot = Bot(token="7073593799:AAEBjG7JZeiV_2n5MMeRHpxEx1bI_hpY7p0")

# Start Telegram Bot
def start(update, context):
    update.message.reply_text("Hello! Send /play <song_name> to play music.")

def play(update, context):
    if context.args:
        song_name = ' '.join(context.args)
        search_youtube(song_name, update)
    else:
        update.message.reply_text("Hello! Send /play <song_name> to play music.")

def search_youtube(song_name, update):
    # Use youtube-dl or yt-dlp to search for a song and get its URL
    query = f"ytsearch:{song_name}"
    ydl_opts = {
        'format': 'bestaudio/best',
        'quiet': True,
        'extractaudio': True,
        'outtmpl': 'downloads/%(id)s.%(ext)s',
    }
    
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(query, download=False)
        url = info_dict['entries'][0]['url']
        update.message.reply_text(f"Here is the music link: {url}")

class Updater:
    def __init__(self, token, update_queue=None):
        self.token = token
        self.update_queue = update_queue
        # other initialization code

# Register handlers with the bot
from telegram import Update
from telegram.ext import Application, CommandHandler

# Create an Application instance instead of an Updater instance
application = Application.builder().token("7073593799:AAEBjG7JZeiV_2n5MMeRHpxEx1bI_hpY7p0").build()

# Add handlers
application.add_handler(CommandHandler("start", start))
application.add_handler(CommandHandler('play', play))
# Run the application
application.run_polling()

    
    
    

# Flask route to interact with the web
@app.route('/webhook', methods=['POST'])
def webhook():
    json_str = request.get_data().decode('UTF-8')
    update = Update.de_json(json.loads(json_str), bot)
    dispatcher.process_update(update)
    return 'ok'

if __name__ == '__main__':
    from threading import Thread
    t = Thread(target=main)
    t.start()

    app.run(host="0.0.0.0", port=5001)
