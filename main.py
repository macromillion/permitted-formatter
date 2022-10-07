import requests
import logging
import threading
import time

def thread_function(name):
    logging.info("Thread %s: starting", name)
    filename = "permittedlist.txt"

    try:
        with open(filename) as f:
            content = f.readlines()
    except FileNotFoundError:
        print('Invalid permittedlist.txt!')
        exit()

    errNum = 0

    print('== START ==\n\nSTEAMID           USERNAME')

    for line in content:
        response = requests.get('http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key=C4F17D21474C11C55E6D5EC08361F18D&steamids=' + str(line))

        json_data = response.json(
    ) if response and response.status_code == 200 else None

        try:
            verifName = json_data['response']['players'][0]['steamid']
        except IndexError:
            print('SKIPPED')
            pass

        i = 0
        while i < len(verifName):
            x = verifName[i]
            checkNum = x.isalpha()
            if checkNum:
                errNum += 1
            i += 1

        try:
            print(json_data['response']['players'][0]['steamid'] + ' ' +
                  json_data['response']['players'][0]['personaname'])
        except IndexError:
            errNum += 1
            pass

    if errNum > 0:
        print('\nList found ' + str(errNum) +
          ' alpha characters in steamids!\n\n== END ==')
    else:
        print('\nSuccessfully verified names with no errors!\n\n== END ==')
        logging.info("Thread %s: finishing", name)

    if __name__ == "__main__":
        format = "%(asctime)s: %(message)s"
        logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")
        logging.info("Main    : before creating thread")
        x = threading.Thread(target=thread_function, args=(1, ))
        logging.info("Main    : before running thread")
        x.start()
        logging.info("Main    : wait for the thread to finish")
        # x.join()
        logging.info("Main    : all done")

x = threading.Thread(target=thread_function, args=(10,))
x.start()