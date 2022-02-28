from telegram.ext.updater import Updater
from telegram.update import Update
from telegram.ext.callbackcontext import CallbackContext
from telegram.ext.commandhandler import CommandHandler
from telegram.ext.messagehandler import MessageHandler
from telegram.ext.filters import Filters
import logging
import wikipedia
import json
import dotenv
import os
import requests

dotenv.load_dotenv()

import logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger()
logger.setLevel(logging.INFO)
token = os.getenv('token')
updater = Updater(token,use_context=True)
def getjokes(api):        
    data = requests.get(api)
    jd = json.loads(data.text)
    return jd
api='https://v2.jokeapi.dev/joke/Any?blacklistFlags=nsfw,religious,political,racist,sexist,explicit&type=twopart' 



def start(update: Update, context: CallbackContext):
	update.message.reply_text(
		"Hello sir, Welcome to the Bot.Please write\
		/help to see the commands available.")

def help(update: Update, context: CallbackContext):
	update.message.reply_text("""Available Commands :-
	/youtube - To get the youtube URL
	/linkedin - To get the LinkedIn profile URL
	/gmail - To get gmail URL
	/geeks - To get the GeeksforGeeks URL""")


def gmail_url(update: Update, context: CallbackContext):
	update.message.reply_text(
		"Your gmail link here (I am not\
		giving mine one for security reasons)")


def help(update: Update, context: CallbackContext):
	update.message.reply_text(
		"""
		/wiki - To get the wikipedia search results,
		/help - To get the list of commands
		/joke - To get a random joke,
		/specific - To get a specific joke
		"""
	)



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

def unknown(update: Update, context: CallbackContext):
	update.message.reply_text(
		"Sorry '%s' is not a valid command" % update.message.text)


def unknown_text(update: Update, context: CallbackContext):
	update.message.reply_text(
		"Sorry I can't recognize you , you said '%s'" % update.message.text)


updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CommandHandler('wiki', wiki))
updater.dispatcher.add_handler(CommandHandler('joke', joke))
updater.dispatcher.add_handler(CommandHandler('specific', specific))
updater.dispatcher.add_handler(CommandHandler('help', help))
updater.dispatcher.add_handler(MessageHandler(Filters.text, unknown))
updater.dispatcher.add_handler(MessageHandler(
	Filters.command, unknown)) # Filters out unknown commands

# Filters out unknown messages.
updater.dispatcher.add_handler(MessageHandler(Filters.text, unknown_text))

updater.start_polling()
