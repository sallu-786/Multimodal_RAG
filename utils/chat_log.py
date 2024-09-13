import os
import pandas as pd
from datetime import datetime
from io import BytesIO


chat_log_file = "chat_log/chat_log.xlsx"
def save_chat_log(message, assistant_msg):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    chat_data = pd.DataFrame([[timestamp, message, assistant_msg]], columns=["Timestamp", "Question", "Answer"])
    if os.path.exists(chat_log_file):
        existing_data = pd.read_excel(chat_log_file)
        chat_data = pd.concat([existing_data, chat_data], ignore_index=True)
    chat_data.to_excel(chat_log_file, index=False)

def get_downloadable_excel():
    if os.path.exists(chat_log_file):
        with open(chat_log_file, "rb") as f:
            return BytesIO(f.read())
    return None

