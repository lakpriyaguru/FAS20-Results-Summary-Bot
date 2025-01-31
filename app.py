import requests
import telebot
import json
from dotenv import load_dotenv
import os
import logging
from datetime import datetime

# Load environment variables from the .env file
load_dotenv()

# Access environment variables using os.getenv
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
APPS_SCRIPT_URL = os.getenv('APPS_SCRIPT_URL')

bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

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

def getDean(level, user_id):
    try:
        response = requests.get(APPS_SCRIPT_URL, params={'function': 'getDean', 'level': level, 'userID': user_id})
        response.raise_for_status()  # Raise an error for bad HTTP status
        log_print(f"Response: {response.text}")  # Log the response
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
        return json.dumps({"error": str(e)})

def getResults(index_number, user_id):
    try:
        response = requests.get(APPS_SCRIPT_URL, params={'function': 'getResults', 'index': index_number, 'userID': user_id})
        response.raise_for_status()  # Raise an error for bad HTTP status
        log_print(f"Response: {response.text}")  # Log the response
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
        return json.dumps({"error": str(e)})
    
def format_dean_list(first_name, dean_json, level):
    records = dean_json.get("records", [])
    total_students = len(records)
    
    # Construct the table header
    table_header = f"| {'Rk':<2} | {'Idx':<6} | {'Name':<12} | {'Comb':<7} | {'GPA':<4} |\n"
    table_header += f"|{'-'*4}|{'-'*8}|{'-'*14}|{'-'*9}|{'-'*6}|\n"
    
    # Construct the table rows
    table_rows = ""
    for record in records:
        table_rows += f"| {record['rank']:<2} | {record['index']:<6} | {record['name'][:12]:<12} | {record['combB']:<7} | {record['gpa']:<4.2f} |\n"

    # Combine the parts
    formatted_dean = (
        f"👋 Hello *{first_name}*, here is the Dean's List for *Level {level}*:\n\n"
        f"🎓 *Total Students:* \t{total_students}\n\n"
        f"📋 *Dean's List Table:*\n"
        f"```\n{table_header}{table_rows}```\n"
        "⚠️ *Disclaimer:*\n"
        "_> This information is provided for general informational purposes only.\n"
        "> The data is based on result sheets published by the faculty office.\n"
        "> We do not guarantee the accuracy, completeness, or reliability of the information provided.\n"
        "> Please verify the information with official sources._"
    )
    
    return formatted_dean

def format_results_list(first_name, results_json, index_number):
    subjects = results_json.get("subjects", [])
    name = results_json.get("name", "N/A")
    total_subjects = len(subjects)
    
    # Construct the table header
    table_header = f"| {'Mod Code':<8} | {'Mod Name':<25} | {'Grade':<5} |\n"
    table_header += f"|{'-'*10}|{'-'*27}|{'-'*7}|\n"
    
    # Construct the table rows
    table_rows = ""
    for subject in subjects:
        table_rows += f"| {subject['subject']:<8} | {subject['name'][:25]:<25} | {subject['grade']:<5} |\n"

    # Combine the parts
    formatted_results = (
        f"👋 Hello *{first_name}*, here are the results summary for *{index_number}* - *{name}*:\n\n"
        f"📚 *Total Subjects:* \t{total_subjects}\n\n"
        f"📋 *Results Table:*\n"
        f"```\n{table_header}{table_rows}```\n"
        "⚠️ *Disclaimer:*\n"
        "_> This information is provided for general informational purposes only.\n"
        "> The data is based on result sheets published by the faculty office.\n"
        "> We do not guarantee the accuracy, completeness, or reliability of the information provided.\n"
        "> Please verify the information with official sources._"
    )
    
    return formatted_results

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
        bot.reply_to(message, "🤖 This bot was created by @lakpriyaguru. If you have any issues or questions, feel free to reach out. 😊 \n\n📜 Version History:\n- v1.0: Display Level 03 Academic Details \n- v2.0: Display Overall GPA Details \n- v2.1: Add Level 03 Dean List \n- v2.2: Updated the total repeat list \n\n🔗 Join the group to access the bot: https://t.me/+suBdxTEim85mZjM1")
        return
    bot.send_message(message.chat.id, "🤖 This bot was created by @lakpriyaguru. If you have any issues or questions, feel free to reach out. 😊 \n\n📜 Version History:\n- v1.0: Display Level 03 Academic Details \n- v2.0: Display Overall GPA Details \n- v2.1: Add Level 03 Dean List \n- v2.2: Updated the total repeat list")

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
                f"🔄 *Total Repeats:* \t{info_json.get('repeatTot', 'N/A')} (L1:{info_json.get('repeatL1', 'N/A')}, L2:{info_json.get('repeatL2', 'N/A')}, L3:{info_json.get('repeatL3', 'N/A')})\n\n"
                f"📈 *Overall GPA:* \t{float(info_json.get('gpa', 0.0)):.2f}\n"
                f"🏅 *Overall Rank:* \t{info_json.get('rank', 'N/A')}\n\n"
                "⚠️ *Disclaimer:*\n"
                "_> This information is provided for general informational purposes only.\n"
                "> The data is based on result sheets published by the faculty office.\n"
                "> We do not guarantee the accuracy, completeness, or reliability of the information provided.\n"
                "> Please verify the information with official sources._"
            )
            bot.send_message(chat_id=message.from_user.id, text=formatted_info, parse_mode='Markdown')
            # Send the message privately to the requesting user
            bot.reply_to(message, f"👋 Dear *{message.from_user.first_name}*, the requested summary for *{index_number}* - *{info_json.get('name', 'N/A')}* has been sent to you in a private message. 📩 Please check your inbox. 😊", parse_mode='Markdown')
    except IndexError:
        # Handle missing index number error
        bot.send_message(message.chat.id, "🚫 Please provide an index number with the /summary command. Example: /summary 202***.")
    except json.JSONDecodeError:
        # Handle invalid JSON response error
        bot.send_message(message.chat.id, "🚫 Error decoding the response. Please try again later. 😊")
    except Exception as e:
        # Catch other errors and notify the user
        bot.send_message(message.chat.id, f"🚫 An unexpected error occurred: {str(e)}. Please try again later. 😊")

# handle /dean <level> command
@bot.message_handler(commands=['dean'])
def handle_dean(message):
    if message.chat.type not in ['group', 'supergroup'] and message.from_user.id != ADMIN_USER_ID:
        bot.reply_to(message, "🚫 This command is only available in groups. \n\n🔗 Please join the group to use the bot: https://t.me/+suBdxTEim85mZjM1")
        return
    try:
        user_id = message.from_user.id  # Get the user ID from the message object
        level = message.text.split()[1]  # Extract the level from the command
        
        log_print(f"Request: {{user_id: {user_id}, 'function': 'getDean', 'level': {level}}}")

        # Assuming getDean returns a JSON string   
        dean = getDean(level, user_id)  # Pass level to the getDean function

        dean_json = json.loads(dean)  # Parse the JSON response
        
        # Check if the response contains error information
        if dean_json.get('status') == 'error':
            bot.reply_to(message, "🚫 Level not found. Please provide a valid level. 📇")
        else:
            # If the response is valid, format the information
            formatted_message = format_dean_list(message.from_user.first_name, dean_json, level)
            bot.send_message(chat_id=message.from_user.id, text=formatted_message, parse_mode='Markdown')
            # Send the message privately to the requesting user
            bot.reply_to(message, f"👋 Dear *{message.from_user.first_name}*, the Dean's List for *Level {level}* has been sent to you in a private message. 📩 Please check your inbox. 😊", parse_mode='Markdown')
    except IndexError:
        # Handle missing level error
        bot.send_message(message.chat.id, "🚫 Please provide a level with the /dean command. Example: /dean *.")
    except json.JSONDecodeError:
        # Handle invalid JSON response error
        bot.send_message(message.chat.id, "🚫 Error decoding the response. Please try again later. 😊")
    except Exception as e:
        # Catch other errors and notify the user
        bot.send_message(message.chat.id, f"🚫 An unexpected error occurred: {str(e)}. Please try again later. 😊")

# make new group announcement
@bot.message_handler(commands=['new_update'])
def announcement(message):
    if message.chat.type in ['group', 'supergroup'] and message.from_user.id == ADMIN_USER_ID:
        announcement_message = bot.send_message(message.chat.id, "📢 New Update: The Level 3 repeat count has been updated! 🎉\n\nTry the /summary command followed by your index number to see the updated information. Example: /summary 202***")
        bot.pin_chat_message(message.chat.id, announcement_message.message_id)
    else:
        bot.reply_to(message, "🚫 This command is only available in groups and can only be used by the admin.")





# handle /results <index> command
@bot.message_handler(commands=['results'])
def handle_info(message):
    if message.chat.type not in ['group', 'supergroup'] and message.from_user.id != ADMIN_USER_ID:
        bot.reply_to(message, "🚫 This command is only available in groups. \n\n🔗 Please join the group to use the bot: https://t.me/+suBdxTEim85mZjM1")
        return
    try:
        index_number = message.text.split()[1]  # Extract the index number from the command
        user_id = message.from_user.id  # Get the user ID from the message object
        
        log_print(f"Request: {{'user_id': {user_id}, 'function': 'getResults', 'index_no': {index_number}}}")

        # Assuming getGPA returns a JSON string   
        info = getResults(index_number, user_id)  # Pass userID to the getGPA function

        info_json = json.loads(info)  # Parse the JSON response
        
        # Check if the response contains error information
        if info_json.get('status') == 'error':
            bot.reply_to(message, "🚫 Index number not found. Please provide a valid index number. 📇")
        else:
            formatted_message = format_results_list(message.from_user.first_name, info_json, index_number)
            bot.send_message(chat_id=message.from_user.id, text=formatted_message, parse_mode='Markdown')
            # Send the message privately to the requesting user
            bot.reply_to(message, f"👋 Dear *{message.from_user.first_name}*, the requested summary for *{index_number}* - *{info_json.get('name', 'N/A')}* has been sent to you in a private message. 📩 Please check your inbox. 😊", parse_mode='Markdown')
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