from fastapi import status, Request
from fastapi.responses import JSONResponse

class UploadFormatException(Exception):
    def __init__(self, file_name:str, error_message:str) -> None:
        self.file_name = file_name
        self.error_message = error_message
