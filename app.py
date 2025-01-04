import requests
import telebot
import json

bot = telebot.TeleBot("7888773252:AAH-DTbyTWpqnxhWedXXOKT2LJiOQXCaMhE")
APPS_SCRIPT_URL = "https://script.google.com/macros/s/AKfycbyW1OSo5rxzo9_8m2Zsw3a0d6M8Lo0EETJyQqS8JUeqp8joKDvWTC3RfTpuZDFnWjM0/exec"

def get_gpa(index_number):
    try:
        # Send the userID along with the other parameters
        response = requests.get(APPS_SCRIPT_URL, params={'function': 'getGPA', 'index': index_number})
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

# about message
@bot.message_handler(commands=['about'])
def about(message):
    bot.send_message(message.chat.id, "🤖 This bot is created by @lakpriyaguru. If you have any problems or queries, feel free to ask. 😊 \n\n📜 Version History:\n- v1.0: Display Level 03 Academic Details")

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
        
        # Assuming getGPA returns a JSON string
        info = get_gpa(index_number)  # Pass userID to the getGPA function
        info_json = json.loads(info)  # Parse the JSON response
        
        # Check if the response contains error information
        if info_json.get('status') == 'error':
            bot.reply_to(message, "Index number not found. Please provide a valid index number.")
        else:
            # If the response is valid, format the information
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
        # Handle missing index number error
        bot.send_message(message.chat.id, "Please provide an index number with the /gpa command. Example: /gpa 202***.")
    except json.JSONDecodeError:
        # Handle invalid JSON response error
        bot.send_message(message.chat.id, "Error decoding the response. Please try again later.")
    except Exception as e:
        # Catch other errors and notify the user
        bot.send_message(message.chat.id, f"An unexpected error occurred: {str(e)}")


# run the bot
print("Starting bot polling...")
bot.polling()
