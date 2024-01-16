import os
import time
import schedule


def delete_json_file(filename):
    if os.path.isfile(filename):
        os.remove(filename)


# need to put here the right name
schedule.every(2).day.do(delete_json_file("aaa"))

while True:
    schedule.run_pending()
    time.sleep(1)
