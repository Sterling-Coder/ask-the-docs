import csv
import os
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
HISTORY_FILE = os.path.join(BASE_DIR, "history.csv")

def log_question_answer(question, answer):
    # Check if file exists and is not empty
    write_header = not os.path.isfile(HISTORY_FILE) or os.stat(HISTORY_FILE).st_size == 0

    with open(HISTORY_FILE, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        if write_header:
            writer.writerow(["Timestamp", "Question", "Answer"])

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        writer.writerow([timestamp, question, answer])

def get_history():
    history = []
    if os.path.isfile(HISTORY_FILE):
        with open(HISTORY_FILE, mode="r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            history.extend(reader)
    return history
