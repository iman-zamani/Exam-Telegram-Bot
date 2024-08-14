#Exam Bot

import telebot
from datetime import datetime
import threading
import os
import random

# Configuration Settings
TOKEN = "YOUR TOKEN"
IMAGE_DIR = "./images/"
NUM_QUESTIONS = 20
QUESTION_TIMEOUT = 60  # in seconds
ACTIVE_HOURS = (0, 24)  # Active all the time

bot = telebot.TeleBot(TOKEN)
user_data = {}
active_users = set()  # To track users who are currently taking or have taken the exam

# Checks if current time is within the allowed time range
def is_within_time():
    current_hour = datetime.now().hour
    return ACTIVE_HOURS[0] <= current_hour < ACTIVE_HOURS[1]

@bot.message_handler(commands=['start'])
def handle_start(message):
    chat_id = message.chat.id
    if chat_id in active_users:
        bot.send_message(chat_id, "You have already started the bot. You cannot start it again.")
        return
    
    if not is_within_time():
        bot.send_message(chat_id, "This bot is not active.")
        return

    active_users.add(chat_id)  # Mark the user as active
    user_data[chat_id] = {'name': None, 'responses': [], 'question_order': list(range(1, NUM_QUESTIONS + 1)), 'message_ids': []}
    random.shuffle(user_data[chat_id]['question_order'])
    msg = bot.send_message(chat_id, "Please enter your name (letters only):")
    user_data[chat_id]['message_ids'].append(msg.message_id)
    bot.register_next_step_handler(msg, handle_name)

def handle_name(message):
    chat_id = message.chat.id
    user_name = message.text.strip()
    # Check if the name contains only letters and spaces
    if not all(char.isalpha() or char.isspace() for char in user_name):
        msg = bot.send_message(chat_id, "Invalid name. Names should only contain alphabet characters and spaces. Please try again:")
        user_data[chat_id]['message_ids'].append(msg.message_id)
        bot.register_next_step_handler(msg, handle_name)
        return

    user_data[chat_id]['name'] = user_name
    send_image(chat_id, 0)  # Start with the first shuffled question


def send_image(chat_id, index):
    if index >= NUM_QUESTIONS:
        bot.send_message(chat_id, "The exam is finished.")
        save_responses(chat_id)
        return

    img_number = user_data[chat_id]['question_order'][index]
    photo_path = os.path.join(IMAGE_DIR, f"{img_number}.png")
    if os.path.exists(photo_path):
        msg = bot.send_photo(chat_id, photo=open(photo_path, 'rb'), reply_markup=telebot.types.ForceReply())
        user_data[chat_id]['message_ids'].append(msg.message_id)
        threading.Timer(QUESTION_TIMEOUT, check_response, args=(chat_id, index, msg.message_id)).start()
    else:
        msg = bot.send_message(chat_id, "Image not found.")
        user_data[chat_id]['message_ids'].append(msg.message_id)

def check_response(chat_id, index, message_id):
    if len(user_data[chat_id]['responses']) <= index:
        user_data[chat_id]['responses'].append('no answer')
        send_image(chat_id, index + 1)

@bot.message_handler(func=lambda message: message.reply_to_message and message.reply_to_message.message_id)
def handle_response(message):
    chat_id = message.chat.id
    msg_id = message.message_id  # Capture the user's response message ID
    user_data[chat_id]['message_ids'].append(msg_id)

    if not message.text.isdigit() or not (1 <= int(message.text) <= 4):
        msg = bot.send_message(chat_id, "Invalid response, please enter a number between 1-4:", reply_markup=telebot.types.ForceReply())
        user_data[chat_id]['message_ids'].append(msg.message_id)
        return

    index = len(user_data[chat_id]['responses'])
    user_data[chat_id]['responses'].append(message.text)
    send_image(chat_id, index + 1)

def save_responses(chat_id):
    name = user_data[chat_id]['name']
    filename = f"{name}.txt"
    responses = user_data[chat_id]['responses']
    question_order = user_data[chat_id]['question_order']
    with open(filename, 'w') as file:
        for idx, (response, q_no) in enumerate(zip(responses, question_order), 1):
            file.write(f"Q{q_no}.png --> Answer: {response}\n")
    delete_messages(chat_id)  # Delete all bot messages after saving responses

def delete_messages(chat_id):
    for msg_id in user_data[chat_id]['message_ids']:
        try:
            bot.delete_message(chat_id, msg_id)
        except Exception as e:
            print(f"Failed to delete message {msg_id}: {str(e)}")

if __name__ == '__main__':
    bot.polling(none_stop=True)
