# Telegram Exam Bot

This Python-based Telegram bot facilitates conducting timed exams by sending question images to participants and collecting their responses. It is designed to operate during specific hours, ensuring control over when exams are available.

## Features

- **Timed Question Delivery**: Sends exam questions as images and expects answers within a specified time limit.
- **Randomized Questions**: Delivers questions in a randomized order to each participant.
- **Time Restricted Access**: Restricts bot activity to configured active hours.
- **Response Logging**: Collects and logs all participant responses to a file.
- **Message Cleanup**: Deletes all bot-related messages post-exam to maintain a clean chat history.

## Installation

### Prerequisites

- Python 3.x
- pip (Python package installer)
- Access to a server or computer where the bot can run continuously
- Telegram account and a Bot Token from [BotFather](https://t.me/botfather)

### Setup

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/iman-zamani/Exam-Telegram-Bot.git
   cd Exam-Telegram-Bot
   ```

2. **Install Dependencies:**
   - The bot uses the `pyTelegramBotAPI` library. Installation is typically the same across operating systems but might require a virtual environment on some Linux distributions if `pip` is not configured globally.

   **For most users:**
   ```bash
   pip install pyTelegramBotAPI
   ```

   **For Linux users requiring a virtual environment:**
   ```bash
   python3 -m venv Exam-Bot-env
   source Exam-Bot-env/bin/activate
   pip3 install pyTelegramBotAPI
   ```

3. **Configuration:**
   Open `bot.py` and replace `"YOUR TOKEN"` with the token you received from BotFather.

4. **Prepare the Image Directory:**
   Ensure you have an `images` directory in the same folder as `bot.py`, with images named `1.png`, `2.png`, etc., up to the number of questions you plan to have in the exam. update the NUM_QUESTIONS in code accordingly

## Usage

To run the bot:

```bash
python bot.py
```

The bot will start polling for messages and will respond based on the commands and replies it receives.

## Customization

You can customize several aspects of the bot's behavior:

- **`NUM_QUESTIONS`**: Set the total number of questions in the exam.
- **`QUESTION_TIMEOUT`**: Duration (in seconds) each question remains active before moving to the next.
- **`ACTIVE_HOURS`**: Tuple representing the hours (in 24-hour format) during which the bot is active (e.g., `(10, 18)` for 10 AM to 6 PM).

## Important Notes

- **Image Deletion**: Post-exam, the bot will attempt to delete all messages containing questions and responses to keep the chat clean.
- **Data Handling**: All responses are saved locally in a text file named after the participant's name. Ensure that participant names are unique to avoid data overwriting.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
