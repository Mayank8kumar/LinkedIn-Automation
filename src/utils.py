import time, random

def random_delay(min_sec=2, max_sec=6):
    delay = random.uniform(min_sec, max_sec)
    time.sleep(delay)

def human_typing(element, text):
    for char in text:
        element.send_keys(char)
        time.sleep(random.uniform(0.05, 0.15))
