import requests
import telebot
import json

bot = telebot.TeleBot("7888773252:AAH-DTbyTWpqnxhWedXXOKT2LJiOQXCaMhE")

# Replace with your Apps Script web app URL
APPS_SCRIPT_URL = "https://script.google.com/macros/s/AKfycbyW1OSo5rxzo9_8m2Zsw3a0d6M8Lo0EETJyQqS8JUeqp8joKDvWTC3RfTpuZDFnWjM0/exec"

def getGPA(index_number, user_id):
    try:
        # Send the userID along with the other parameters
        response = requests.get(APPS_SCRIPT_URL, params={'function': 'getGPA', 'index': index_number, 'userID': user_id})
        response.raise_for_status()  # Raise an error for bad HTTP status
        print(f"Response: {response.text}")  # Debugging line
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
        return json.dumps({"error": str(e)})

# def get_result(index_number):
#     try:
#         response = requests.get(APPS_SCRIPT_URL, params={'function': 'getResult', 'index': index_number})
#         response.raise_for_status()  # Raise an error for bad HTTP status
#         print(f"Response: {response.text}")  # Debugging line
#         return response.text
#     except requests.exceptions.RequestException as e:
#         print(f"Request error: {e}")
#         return f"Error: {str(e)}"
    
# start message
@bot.message_handler(commands=['start'])
def greet(message):
    bot.send_message(message.chat.id, "👋 Welcome to FAS20 Results Summary Bot! \n\n📊 Send me your index number with the /gpa command and I will tell you your academic standing. \n\nℹ️ Type /help for more information.")

# help message
@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id, "ℹ️ Send me your index number with the /gpa command and I will tell you your CGPA. If you have any queries, feel free to ask. 😊")

# handle /results <index> command
# @bot.message_handler(commands=['results'])
# def handle_results(message):
#     try:
#         index_number = message.text.split()[1]  # Extract the index number from the command
#         result = get_result(index_number)
#         bot.reply_to(message, result)
#     except IndexError:
#         bot.send_message(message.chat.id, "Please provide an index number with the /results command.")
#     except json.JSONDecodeError:
#         bot.send_message(message.chat.id, "Error decoding the response. Please try again later.")

# handle /gpa <index> command
@bot.message_handler(commands=['gpa'])
def handle_info(message):
    try:
        index_number = message.text.split()[1]  # Extract the index number from the command
        user_id = message.from_user.id  # Get the userID from the message
        info = getGPA(index_number, user_id)  # Pass userID to the getGPA function
        info_json = json.loads(info)  # Parse the JSON response
        
        if 'error' in info_json:
            bot.reply_to(message, "Index number not found. Please provide a valid index number.")
            return
        
        formatted_info = (
            f"👋 Hi {message.from_user.first_name}, here is the information for index number {index_number}:\n\n"
            f"📇 Index No: \t{info_json.get('index', 'N/A')}\n"
            f"👤 Name: \t{info_json.get('name', 'N/A')}\n"
            f"📚 Combination: \t{info_json.get('combB', 'N/A')} | {info_json.get('combA', 'N/A')}\n\n"
            f"📊 Level 03 Credits: \t{info_json.get('credits', 'N/A')}\n"
            f"📈 Level 03 GPA: \t{info_json.get('gpa', 'N/A')}\n"
            f"🏅 Level 03 Rank: \t{info_json.get('rank', 'N/A')}\n\n"
            "⚠️ Disclaimer:\n"
            "> This information is provided for general informational purposes only.\n"
            "> The data is based on result sheets published by the faculty office.\n"
            "> We do not guarantee the accuracy, completeness, or reliability of the information provided.\n"
            "> Please verify the information with official sources."
        )
        bot.reply_to(message, formatted_info)
    except IndexError:
        bot.send_message(message.chat.id, "Please provide an index number with the /gpa command.")
    except json.JSONDecodeError:
        bot.send_message(message.chat.id, "Error decoding the response. Please try again later.")

# run the bot
print("Starting bot polling...")
bot.polling()
