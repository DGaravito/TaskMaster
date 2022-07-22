from Guis.main import main
import logging

# anything will get logged in a log.txt file in the application's directory
logging.basicConfig(filename='log.txt', level=logging.DEBUG)

# main loop
if __name__ == '__main__':

    # run the main python gui
    try:

        main()

    # in case of error, log it in the txt
    except Exception:

        logging.error('A critical error occured', exc_info=True)
