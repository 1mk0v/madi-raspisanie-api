from fastapi import status

class BaseAppException(BaseException):

    def __init__(self, *args: object, detail:str = 'Something wrong', status_code) -> None:
        self.detail = detail
        self.status_code = status_code
        super().__init__(*args)


class BaseClientException(BaseAppException):

    def __init__(self, *args: object, detail: str = 'Base client exception. Something wrong with your request.',
                 status_code= status.HTTP_400_BAD_REQUEST) -> None:
        super().__init__(*args, detail=detail, status_code=status_code)


class BaseServerException(BaseAppException):

    def __init__(self, *args: object, detail: str = "Base server exception. Something wrong with app.", 
                 status_code = status.HTTP_500_INTERNAL_SERVER_ERROR) -> None:
        super().__init__(*args, detail=detail, status_code=status_code)


class NotFoundError(BaseClientException):

    def __init__(self, *args: object, detail: str = 
                 "The requested data was not found. They may not be on the website or in the database.",
                 status_code=status.HTTP_404_NOT_FOUND) -> None:
        super().__init__(*args, detail=detail, status_code=status_code)


