from Guis.main import main
import logging

logging.basicConfig(filename='log.txt', level=logging.DEBUG)

if __name__ == '__main__':

    try:

        main()

    except Exception:

        logging.error('A critical error occured', exc_info=True)
