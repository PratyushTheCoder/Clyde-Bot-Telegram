from telegram.ext import CallbackContext, CommandHandler, MessageHandler, Filters
from telegram.ext.updater import Updater
from telegram.update import Update
import wikipedia
import requests
import json
from youtube_dl import YoutubeDL

def getjokes(api):        
    data = requests.get(api)
    jd = json.loads(data.text)
    return jd
api='https://v2.jokeapi.dev/joke/Any?blacklistFlags=nsfw,religious,political,racist,sexist,explicit&type=twopart' 

def gmail_url(update: Update, context: CallbackContext):
	update.message.reply_text(
		"Your gmail link here (I am not\
		giving mine one for security reasons)")


def wiki(update: Update, context: CallbackContext,):
	query =  "_".join(context.args)
	try:
		summary = wikipedia.summary(query, sentences=10)
		update.message.reply_text(f'Your Results are :-\n{summary}')
	except:
		update.message.reply_text("Sorry I can't find the results")

def joke(update: Update, context: CallbackContext):
	jokes=getjokes(api)
	update.message.reply_text(
		f"""
		Question: {jokes['setup']}
		Answer: {jokes['delivery']}
		"""
	)
def specific(update: Update, context: CallbackContext):
	word = "".join(context.args)
	api2=f'https://v2.jokeapi.dev/joke/Any?blacklistFlags=nsfw,religious,political,racist,sexist,explicit&type=twopart&contains={word}' 
	jokes=getjokes(api2)
	if jokes['error'] == True:
		update.message.reply_text(f"Sorry an error occured, Error Message {jokes['message']}")
	else:
		update.message.reply_text(
			f"""
			Question: {jokes['setup']}
			Answer: {jokes['delivery']}
			"""
		)	
def youtube(update: Update, context: CallbackContext):
    query =  "".join(context.args)
    ydl = YoutubeDL()
    ydl.add_default_info_extractors()
    try:
        info = ydl.extract_info(f'ytsearch:{query}', download=False)
        update.message.reply_text(f"""
        Title: {info["title"]}
        Description: {info["description"]}
        Uploader: {info["uploader"]}
        Upload Date: {info["upload_date"]}
        """)
    except:
        update.message.reply_text("Sorry I can't find the results")