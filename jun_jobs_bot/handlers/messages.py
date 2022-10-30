from dataclasses import dataclass


@dataclass
class MessageReply:
    INFO = 'Hi. I can upload for you statistics on junior-level jobs in the ' \
       'programming language you are interested in. You can see the dynamics ' \
       'of job growth for the selected period, as well as the number of ' \
       'vacancies at the moment. The jobs are downloaded from hh.ru. ' \
       'To start press /start'
    HELP = 'Available commands:\n' \
           '/start\n' \
           '/info'

    START = 'Choose your language:\n' \
            '/Python\n' \
            '/Java\n' \
            '/Php\n' \
            '/JavaScript\n' \
            '/Ruby'
    COMPARE = 'Choose a comparison format:\n' \
              '/RightNow\n'\
              '/perWeek\n' \
              '/perMonth\n' \
              '/per3Month\n' \
              '/per6Month\n' \
              '/perYear'
