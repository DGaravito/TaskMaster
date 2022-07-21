from Guis.main import main
import logging

logging.basicConfig(filename='log.txt', level=logging.DEBUG)

if __name__ == '__main__':

    try:

        main()
        raise OSError('Emulated exception to be traced back to log file')

    except Exception:

        logging.error('A critical error occured', exc_info=True)
