from datetime import date
from jun_jobs_bot.logic.user_requests import languages
from jun_jobs_bot.logic.dataclasses import languages_id, region_id
from jun_jobs_bot import models
import requests
import json


def check_db_record():
    with models.session() as s:
        check = s.query(models.Requests).filter(models.Requests.date ==
                                                date.today()).first()
        if check is not None:
            return 'The request has already been made today!'
        upload = Requester()
        message = upload.upload_to_db()
        return message


class Requester:

    def __init__(self):
        self.languages = languages

    def _get_data(self) -> dict[str, int]:
        result = dict()
        for lang in self.languages:
            template = f'https://api.hh.ru/vacancies?text={lang}+junior' \
                       f'&per_page=100&area=113'
            data = json.loads(requests.get(template).text)
            result[lang]: int = data['found']
        return result

    def upload_to_db(self) -> str:
        with models.session() as s:
            data = self._get_data()
            _date = date.today()
            for key, value in data.items():
                record = models.Requests(language_id=languages_id[key],
                                         region_id=region_id['Russia'],
                                         vacancies=value,
                                         date=_date)
                s.add(record)
            s.commit()
            return 'Completed'
