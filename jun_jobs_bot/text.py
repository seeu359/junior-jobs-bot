from dataclasses import dataclass
from string import Template


@dataclass
class MessageReply:
    INFO = (
        "Hi. I can upload for you statistics on junior-level jobs in the "
        "programming language you are interested in. You can see the dynamics"
        " of job growth for the selected period, as well as the number of "
        "vacancies at the moment. The jobs are downloaded from hh.ru. "
        "To start press /start"
    )
    HELP = "Available commands:\n" "/start\n" "/info"

    SELECT_LANG = "Select a programming language"
    COMPARE = "Select the type of comparison"
    ADMIN_START = "Make a general request?"
    REQUEST_MADE = "The request has already been made today!"
    HAVE_NO_DATE = "Today's data has not yet been uploaded"
    DATA_DOWNLOADED_SUCCESS = "The data was successfully uploaded to the " "database"
    TODAY_STAT = Template(
        "$language vacancies are currently: $all_vacancies.\n"
        "Of these jobs, there are no experience requirements: "
        "$no_exp_vacancies"
    )

    VACS_NO_CHANGE = "The number of vacancies has not changed"

    VACS_DECREASED = Template("The number of $language jobs decreased by " "$result%")

    VACS_INCREASED = Template(
        "The number of $language vacancies has increased by $result%"
    )

    NOT_CORRECT_LANG = "I can't process this kind of language"

    NOT_CORRECT_COMPARE_TYPE = "I can't compare it to this type of"


@dataclass
class ExceptionMessage:
    CONNECTION_ERROR = Template(
        "URL $url is temporarily unavailable or incorrectly entered. "
        "Status code is $status"
    )
