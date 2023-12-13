
## Жизненный цикл

``` mermaid
stateDiagram-v2
    state if_state <<choice>>
    
    state Institute {
        [*] --> [*]: schedule
    }

    Request_Module --> Institute : request

    Institute --> Request_Module : response
    
    Request_Module --> if_state: response

    if_state --> Database: status = 404/500

    state Generator {
        [*] --> Bridge: Data
        Bridge --> [*]: Format Data
    }

    state Bridge {

        state Formatter {
            [*] --> [*]: Format data
        }
        
        [*] --> Formatter: Data
        note right of Formatter : This module is individual for institute
        Formatter --> InstituteGenerator: Pydantic Model
        InstituteGenerator --> [*]: Format data
    }
    
    if_state --> Generator: status = 200

    Database --> Result
    Generator --> Result
```

## Запросы

За запросы отвечает модуль **madi.py**.
В данном модуле реализованы классы, с помощью который можно отправить запросы к определенной сущности института (группа, преподаватель, кафедра) или же создать новый класс, который релизует данные методы.

``` py
class RaspisanieMADI():

    def __init__(self) -> None:
        self.url = 'https://raspisanie.madi.ru/tplan/tasks/{}'

    def _get(self, url, data:dict = None) -> requests.Response:
        return requests.get(self.url.format(url), data)
    
    def _post(self, url, data:dict = None, ) -> requests.Response:
        return requests.post(self.url.format(url), data = data)
    
    def _schedule(self, data:dict) -> requests.Response:
        return self._post(url="tableFiller.php", data=data)

    def _getPageElementOrException(self, response:requests.Response, page_element:str, class_name:str=None, detail:str='Not found') -> List[bs] | bs:
        html = bs(response.text, 'lxml').find_all(name=page_element, attrs={"class":class_name})
        if len(html) < 1:
            raise ValueError(detail)
        return html
```