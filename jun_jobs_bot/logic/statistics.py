from dataclasses import dataclass
from furl import furl
import requests
from jun_jobs_bot.logic.classes import RequestParams


@dataclass
class URLParts:
    """
    URL parts for build url in Statistics class. Netloc - its body of api url.
    Other params - parts of url, which represent models from database.
    """
    netloc = 'https://jun-jobs-api.online/'
    stat_path = '/stat'


class Statistics:

    def __init__(self, request_data: RequestParams):

        self.request_data = request_data
        self.url = \
            furl(URLParts.netloc) / URLParts.stat_path / \
            self.request_data.language / self.request_data.compare_type
        self.stat = self._get_stat()

    def _get_stat(self) -> dict:
        return requests.get(self.url).json()
