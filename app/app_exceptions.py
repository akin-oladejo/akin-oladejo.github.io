from fastapi import status, Request
from fastapi.responses import JSONResponse

class ImageFormatException(Exception):
    def __init__(self, file_name:str) -> None:
        self.file_name = file_name
    