import multiprocessing.process
import os
import time
import asyncio
import multiprocessing
from dotenv import load_dotenv

# python files
from src.utils import get_eng_path, get_titles_from_tuple
from src.filemanager import FileManager
from src.parser import extract_posts
from src.checker import DecisionEngine, SmartFilter
from src.messager import PushoverClient
from src.tts.google_TTS import run_text_to_speech_processor


# ------------------------------------------------------------
load_dotenv(get_eng_path())
WATCH_DIR = os.getenv("WATCH_DIR")
TIME_SLEEP = int(os.getenv("TIME_SLEEP"))
OPEANAI_API_KEY = os.getenv("OPEANAI_API_KEY")
BOOLEAN_CONDITIONS = os.getenv("BOOLEAN_CONDITIONS")
PUSHOVER_USER_KEY = os.getenv("PUSHOVER_USER_KEY")
PUSHOVER_APP_TOKEN = os.getenv("PUSHOVER_APP_TOKEN")
LINGUISTIC_CONDITTIONS = os.getenv("LINGUISTIC_CONDITTIONS")
# ------------------------------------------------------------


async def main():
    manager = FileManager(WATCH_DIR)
    processed_boolean = DecisionEngine(BOOLEAN_CONDITIONS)
    processed_linguistic = SmartFilter(OPEANAI_API_KEY, LINGUISTIC_CONDITTIONS)
    messager = PushoverClient(PUSHOVER_APP_TOKEN, PUSHOVER_USER_KEY, send_notification)
    # Множество для отслеживания обработанных заголовков
    processed_posts = set()

    while True:
        global is_first_iteration
        html_files = manager.process_new_files()
        print(f"{len(html_files)} new html files found")

        # Используем генераторы для извлечения заголовков, чтобы не хранить списки в памяти
        posts = []
        for html_file in html_files:
            posts.extend(extract_posts(html_file))

        # Объединяем заголовки из двух источников в генератор
        all_posts = set(post for post in posts)

        if is_first_iteration:
            # При первой итерации просто добавляем заголовки в множество
            processed_posts.update(all_posts)
            is_first_iteration = False
            print(f"Initial processed titles: {len(processed_posts)}")
        else:
            # На последующих итерациях проверяем новые заголовки
            new_titles = all_posts - processed_posts
            processed_posts.update(new_titles)

            if new_titles:
                print(f"New titles: {len(new_titles)}")
                validated_data = processed_boolean.process(list(new_titles))
                validated_data = await processed_linguistic.process(get_titles_from_tuple(validated_data))
                print("yes")
                manager.delete_audio_files()
                multiprocessing.Process(target=run_text_to_speech_processor, args=(validated_data,)).start() # audioplay title
                messager.send_multiple_messages(validated_data)
                
                # Wait for the process to finish

            else:
                print("No new titles found.")

        print(f"Waiting {TIME_SLEEP} seconds...\n")
        time.sleep(TIME_SLEEP)


if __name__ == "__main__":
    is_first_iteration = True
    send_notification = input("send notifications (1. yes, 2. no): ") == "1"
    if send_notification:
        is_first_iteration = input("send notification for first iteration (1. yes, 2. no): ") == "2"
    asyncio.run(main())
