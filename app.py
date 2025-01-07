import requests
import telebot
import json
import logging
from datetime import datetime

bot = telebot.TeleBot("7888773252:AAH-DTbyTWpqnxhWedXXOKT2LJiOQXCaMhE")
APPS_SCRIPT_URL = "https://script.google.com/macros/s/AKfycby3Ic9yX5Xg_PyfbkqOd7Wk21cApgRD8Y7y-ZAxMuvD3sE3aztD7aPcgRtf8eWNV2ax/exec"
ADMIN_USER_ID = 558847311

# Configure logging
log_file = "output.log"  # Specify the log file name
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        logging.FileHandler(log_file),  # Log to a file
        logging.StreamHandler()        # Optionally log to console
    ]
)

# Redirect print() to logging.info
def log_print(*args, **kwargs):
    message = " ".join(map(str, args))
    logging.info(message)

def getSummary(index_number, user_id):
    try:
        response = requests.get(APPS_SCRIPT_URL, params={'function': 'getSummary', 'index': index_number, 'userID': user_id})
        response.raise_for_status()  # Raise an error for bad HTTP status
        log_print(f"Response: {response.text}")  # Log the response
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
        return json.dumps({"error": str(e)})

def getDean(level):
    try:
        response = requests.get(APPS_SCRIPT_URL, params={'function': f'getDean', 'level': level})
        response.raise_for_status()  # Raise an error for bad HTTP status
        log_print(f"Response: {response.text}")  # Log the response
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
        return json.dumps({"error": str(e)})

# start message
@bot.message_handler(commands=['start'])
def greet(message):
    if message.chat.type not in ['group', 'supergroup'] and message.from_user.id != ADMIN_USER_ID:
        bot.reply_to(message, "👋 Welcome to the FAS20 Results Summary Bot! \n\n📊 Send me your index number using the /summary command, and I will provide your academic standing. \n\nℹ️ Type /help for more information or /about to learn more about the bot. \n\n🔗 Join the group to access the bot: https://t.me/+suBdxTEim85mZjM1")
        return
    bot.send_message(message.chat.id, "👋 Welcome to the FAS20 Results Summary Bot! \n\n📊 Send me your index number using the /summary command, and I will provide your academic standing. \n\nℹ️ Type /help for more information or /about to learn more about the bot.")

# help message
@bot.message_handler(commands=['help'])
def help(message):
    if message.chat.type not in ['group', 'supergroup'] and message.from_user.id != ADMIN_USER_ID:
        bot.reply_to(message, "📊 Please send me your index number using the /summary command, and I will provide your GPA. If you have any questions, feel free to contact @lakpriyaguru. 😊 \n\n🔗 Join the group to access the bot: https://t.me/+suBdxTEim85mZjM1")
        return
    bot.send_message(message.chat.id, "📊 Please send me your index number using the /summary command, and I will provide your GPA. If you have any questions, feel free to contact @lakpriyaguru. 😊")

# about message
@bot.message_handler(commands=['about'])
def about(message):
    if message.chat.type not in ['group', 'supergroup'] and message.from_user.id != ADMIN_USER_ID:
        bot.reply_to(message, "🤖 This bot was created by @lakpriyaguru. If you have any issues or questions, feel free to reach out. 😊 \n\n📜 Version History:\n- v1.0: Display Level 03 Academic Details \n- v2.0: Display Overall GPA Details \n\n🔗 Join the group to access the bot: https://t.me/+suBdxTEim85mZjM1")
        return
    bot.send_message(message.chat.id, "🤖 This bot was created by @lakpriyaguru. If you have any issues or questions, feel free to reach out. 😊 \n\n📜 Version History:\n- v1.0: Display Level 03 Academic Details \n- v2.0: Display Overall GPA Details")

# handle /summary <index> command
@bot.message_handler(commands=['summary'])
def handle_info(message):
    if message.chat.type not in ['group', 'supergroup'] and message.from_user.id != ADMIN_USER_ID:
        bot.reply_to(message, "🚫 This command is only available in groups. \n\n🔗 Please join the group to use the bot: https://t.me/+suBdxTEim85mZjM1")
        return
    try:
        index_number = message.text.split()[1]  # Extract the index number from the command
        user_id = message.from_user.id  # Get the user ID from the message object
        
        log_print(f"Request: {{'user_id': {user_id}, 'function': 'getSummary', 'index_no': {index_number}}}")

        # Assuming getGPA returns a JSON string   
        info = getSummary(index_number, user_id)  # Pass userID to the getGPA function

        info_json = json.loads(info)  # Parse the JSON response
        
        # Check if the response contains error information
        if info_json.get('status') == 'error':
            bot.reply_to(message, "🚫 Index number not found. Please provide a valid index number. 📇")
        else:
            # If the response is valid, format the information
            formatted_info = (
                f"👋 Hello *{message.from_user.first_name}*, here is the summary for *{index_number}* - *{info_json.get('name', 'N/A')}*:\n\n"
                f"📇 *Index No:* \t{info_json.get('index', 'N/A')}\n"
                f"👤 *Name:* \t{info_json.get('name', 'N/A')}\n"
                f"📚 *Combination:* \t{info_json.get('combB', 'N/A').replace('_', ' ')} | {info_json.get('combA', 'N/A').replace('_', ' ')}\n\n"
                f"🎓 *Total Credits:* \t{info_json.get('credit', 'N/A')}\n"
                f"🔄 *Repeats:* \t{info_json.get('repeat', 'N/A')}\n\n"
                f"📈 *Overall GPA:* \t{info_json.get('gpa', 'N/A')}\n"
                f"🏅 *Overall Rank:* \t{info_json.get('rank', 'N/A')}\n\n"
                "⚠️ *Disclaimer:*\n"
                "_> This information is provided for general informational purposes only.\n"
                "> The data is based on result sheets published by the faculty office.\n"
                "> We do not guarantee the accuracy, completeness, or reliability of the information provided.\n"
                "> Please verify the information with official sources._"
            )
            bot.send_message(chat_id=message.from_user.id, text=formatted_info, parse_mode='Markdown')
            # Send the message privately to the requesting user
            bot.reply_to(message, "✅ GPA details have been sent to you in a private message. Please check your inbox. 😉")
    except IndexError:
        # Handle missing index number error
        bot.send_message(message.chat.id, "🚫 Please provide an index number with the /summary command. Example: /summary 202***.")
    except json.JSONDecodeError:
        # Handle invalid JSON response error
        bot.send_message(message.chat.id, "🚫 Error decoding the response. Please try again later. 😊")
    except Exception as e:
        # Catch other errors and notify the user
        bot.send_message(message.chat.id, f"🚫 An unexpected error occurred: {str(e)}. Please try again later. 😊")

# run the bot
# print("Starting Telegram Bot...")
log_print("Starting Telegram Bot...")
bot.polling()