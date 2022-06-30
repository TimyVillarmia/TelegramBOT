from telegram.ext import Updater, CommandHandler
import requests
from bs4 import BeautifulSoup

# Paste here the cookies and headers of the Target website
# visit https://curlconverter.com/ on how to get the cookies and headers

cookies = {
   
   }

headers = {

}



Target_URL = requests.get('https://sams.act.edu.ph/OnlineExam/Index', cookies=cookies, headers=headers)
soup = BeautifulSoup(Target_URL.content, 'html.parser')
Activity_card = soup.find_all('a', class_='exam-link')

LMS_LINK = 'https://sams.act.edu.ph'



print("Bot started...")


def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Type /help to get started")
    
def help(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text='''Available Command/s: 
                             
"/backlog" - to get the old/new active items in your backlog
''')


def backlog(update, context):
    counter = 0
    for activity in Activity_card: #Loop through anchor tag
         # Find the <td>Attemtp Limit</td> then return the next sibling 
        if "0 / 2" in activity.find("td", text="Attempt Limit").find_next_sibling("td").text:
            act_link = (f"{LMS_LINK + activity['href']}\n")
            title = activity.find('h3', class_='exam-title c-finished-exam')
            table = activity.find('table', class_='exam-detail-table')
            act_table = (f"{table.text}").replace("\n\n", "\n")
            act_title = (f"{title.text}")
            message_block = (f"Title: {act_title}\n{act_link}{act_table}\n")
            context.bot.send_message(chat_id=update.effective_chat.id, text=message_block)
            counter += 1  
        else:
            pass    
        
    context.bot.send_message(chat_id=update.effective_chat.id, text=f"You {counter} new active activities ")

       


def main():
    TOKEN = "Change this to your TelegramBot API KEY"
    updater = Updater(token=TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    start_handler = CommandHandler("start", start)
    help_handler = CommandHandler("help", help)
    backklog_handler = CommandHandler("backlog", backlog)
    
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(help_handler)
    dispatcher.add_handler(backklog_handler)

    updater.start_polling()
    
    

if __name__ == '__main__':
    main()


