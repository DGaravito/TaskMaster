from Guis.main import main
import logging

# anything will get logged in a log.txt file in the application's directory
logging.basicConfig(filename='TaskMaster.log', level=logging.DEBUG, filemode='w', format='%(asctime)s %(message)s')
logger = logging.getLogger(__name__)

# main loop
if __name__ == '__main__':

    # run the main python gui
    try:

        logging.info('Starting TaskMaster...')
        main()
        logging.info('Closing TaskMaster...')

    # in case of error, log it in the txt
    except Exception as err:

        logging.exception(err, exc_info=True)
