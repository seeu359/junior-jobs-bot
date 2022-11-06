from dataclasses import dataclass


@dataclass
class MessageReply:
    INFO = 'Hi. I can upload for you statistics on junior-level jobs in the ' \
       'programming language you are interested in. You can see the dynamics' \
       ' of job growth for the selected period, as well as the number of ' \
       'vacancies at the moment. The jobs are downloaded from hh.ru. ' \
       'To start press /start'
    HELP = 'Available commands:\n' \
           '/start\n' \
           '/info'

    SELECT_LANG = 'Select a programming language'
    COMPARE = 'Select the type of comparison'
    ADMIN_START = 'Make a general request?'
    REQUEST_MADE = 'The request has already been made today!'
    HAVE_NO_DATE = 'Today\'s data has not yet been uploaded'
    DATA_DOWNLOADED_SUCCESS = 'The data was successfully uploaded to the ' \
                              'database'