import glob
import logging
import os
import time
from bs4 import BeautifulSoup
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, LoggingEventHandler

CURRENT_DIR = os.getcwd()
logging.basicConfig(level=logging.DEBUG)
class CustomEventHandler(FileSystemEventHandler):
    def on_moved(self, event):
        logging.debug("File moved from %s to %s" % (event.src_path, event.dest_path))
        html_docs = glob.iglob(CURRENT_DIR+"**\\*.html")
        for doc in html_docs:
            rewrite_doc = False
            with open(doc, "r") as html:
                mkuri = lambda x:os.path.relpath(x).replace("\\","/")
                body = html.read()
                new_body = body.replace(mkuri(event.src_path), mkuri(event.dest_path))
                if body != new_body:
                    rewrite_doc = True
            if rewrite_doc:
                with open(doc, "w") as html:
                    html.write(new_body)

def main():
    event_handler = CustomEventHandler()
    observer = Observer()
    observer.schedule(event_handler, CURRENT_DIR, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        exit(0)

if __name__ == "__main__":
    main()
