#!/usr/bin/env python3
import json
import hashlib
import logging
import os
import time
from Crypto.Random import random
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
from tkinter import Tk
from tkinter.messagebox import askyesno
from tkinter.simpledialog import askstring
import cryptionhub as ch

#Configuration
logging.basicConfig(level=logging.DEBUG, filename="encryption_monitor.log",format="%(filename)s:%(asctime)s:%(message)s")
HMAC_ITERATIONS = 500000
with open("config.json", "r") as config_file:
    config = json.load(config_file)
    DES_PATH = config["DES_PATH"]
    SRC_PATH = config["SRC_PATH"]

logging.info("Destination Path (DES_PATH) set to %s" % DES_PATH)
logging.info("Moitoring Path set to %s" % SRC_PATH)
logging.info("HMAC Iterations set to %s" % HMAC_ITERATIONS)

class CustomFileHandler(PatternMatchingEventHandler):
    def on_created(self, event):
        logging.info("%s has been created." % event.src_path)
        root = Tk()
        root.lift()
        root.withdraw() #prevents two prompts from showing when called
        root.attributes("-topmost", True)
        #Checking if a file is being written to.
        f_size = os.stat(event.src_path).st_size
        time.sleep(1)
        n_size = os.stat(event.src_path).st_size
        while f_size != n_size:
            time.sleep(1)
            f_size = n_size
            n_size = os.stat(event.src_path).st_size
            logging.debug("Video Sizes - f_size = %s, n_size = %s" % (f_size, n_size))
        logging.debug("File %s has completed writing with a size of %s" % (event.src_path, f_size))
        if askyesno("Diary Locker", "Do you want to encrypt this video?"):
            iv = ch.geniv()
            passphrase = askstring("Diary Locker", "Please enter a passphrase (The longer the better)", show="*")
            passphrase = hashlib.pbkdf2_hmac("sha256", passphrase.encode(), iv, HMAC_ITERATIONS)
            destination = DES_PATH+event.src_path.split("\\")[-1] + "."  + iv.decode() + "." + "aes"
            ch.encrypt(event.src_path, destination, passphrase, iv)
        else:
            logging.info("File encryption request denied.")

def main():
    event_handler = CustomFileHandler(patterns=["*.mp4"])
    observer = Observer()
    observer.schedule(event_handler, SRC_PATH, recursive=False)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    main()
    