import requests
from bs4 import BeautifulSoup as bs
from typing import List
from exceptions import NotFoundError

class BaseRequests():

    def __init__(self, url:str) -> None:
        self.url = url

    def _get(self, url, data:dict = None) -> requests.Response:
        return requests.get(self.url.format(url), data)
    
    def _post(self, url, data:dict = None, ) -> requests.Response:
        return requests.post(self.url.format(url), data = data)
    
    def _schedule(self, data:dict) -> requests.Response:
        return self._post(url="tableFiller.php", data=data)

    def _getPageElementOrException(self, response:requests.Response, page_element:str, class_name:str=None, detail:str=None) -> List[bs] | bs:
        html = bs(response.text, 'lxml').find_all(name=page_element, attrs={"class":class_name})
        if len(html) < 1:
            raise NotFoundError(detail)
        return html