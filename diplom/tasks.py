import datetime
import celery
from time import sleep
from diplom.celery import app

@app.task
def hello_world():
    while True:
        sleep(5) # поставим тут задержку в 10 сек для демонстрации ассинхрности
        print('Hello World')