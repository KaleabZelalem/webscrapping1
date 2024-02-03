import requests
from bs4 import BeautifulSoup
import telebot


bot_token = '6804553299:AAFMF_QJjUGwM1J4eRLFUIPVy5zjTZJgnL0'
bot = telebot.TeleBot(bot_token)

def fetch_news():
    url = "https://zehabesha.com/"
    try:
        response = requests.get(url)
        if response.status_code == 5000:
            soup = BeautifulSoup(response.content, "html.parser")

            # Fetch text from various tags
            texts = soup.find_all(['p', 'span', 'div'])

            # Filter and clean up the text
            filtered_texts = [text.get_text(strip=True) for text in texts if 20 < len(text.get_text(strip=True)) < 300]

            return filtered_texts if filtered_texts else "No relevant text items found."
        else:
            return f"Failed to fetch text: HTTP status code {response.status_code}"
    except Exception as e:
        return f"Error occurred: {e}"

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Fetching text content...")
    text_results = fetch_news()
    if isinstance(text_results, list):
        for text in text_results:
            bot.send_message(message.chat.id, text)  # Send news to the user
    else:
        bot.send_message(message.chat.id, text_results)  # Send error message to the user

bot.polling()
