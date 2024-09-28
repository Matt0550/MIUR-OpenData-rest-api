from fastapi.exceptions import HTTPException

class NoSchoolsFound(HTTPException):
    def __init__(self):
        super().__init__(status_code=404, detail="No schools found")

class MaxLimitReached(HTTPException):
    def __init__(self):
        super().__init__(status_code=400, detail="The limit parameter must be less than or equal to 1500")