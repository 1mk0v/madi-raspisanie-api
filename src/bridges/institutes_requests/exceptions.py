from exceptions import NotFoundError

class EmptyResultError(NotFoundError):
    def __init__(self, *args: object, detail: str = 'Returned empty result', status_code=400) -> None:
        super().__init__(*args, detail=detail, status_code=status_code)