# house all utility functions
from passlib.context import CryptContext
from . import database
import base64

def get_db():
    '''
    Yield the database instance
    '''
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

class Hash():
    """
    Hash and verify passwords
    """
    def __init__(self, plain_pwd) -> None:
        # set hash context
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        self.value = self.pwd_context.hash(plain_pwd)

    def verify(self, hashed_pwd):
        return self.pwd_context.verify(self.value, hashed_pwd)

class UploadFormatException(Exception):
    '''
    Just a usual exception. The only special thing is I can pass the name of the file
    '''
    def __init__(self, file_name:str, error_message:str) -> None:
        self.file_name = file_name
        self.error_message = error_message

# I never actually used this class below
class CustomUpload:
    '''
    A product of overthinking. Say I need to upload a file of a certain type,
    persist it in the SQL db as a base64 encoded string and decode it upon retrieval,
    this class handles just that.
    '''

    # def __init__(self, input:UploadFile|None = None) -> None:
    #     if input:
    #         self.input = input
    #         self.is_verified = False
    #         self.is_encoded = False
    #     else: self.input = None

    def verify_input(self, accepted_ext:list = ['image/jpeg', 'image/png']):
        # the default acceptable extensions are jpg and png. Change if you want.
        if self.input:
            if self.input.content_type not in accepted_ext:
                raise UploadFormatException(file_name = self.input.filename,
                                            error_message= f'Accepted file types are {accepted_ext}.')
            else:
                self.is_verified = True

    async def encode(self):
        if self.is_verified:
            content = await self.input.read()

            # encode the input into b64 string
            encoded =  base64.b64encode(content)
            self.is_encoded = True
            return encoded
        else:
            raise UploadFormatException(
                file_name=self.input.filename,
                error_message='An error occurred verifying the file type.'
            )

    def decode(self):
        if self.is_encoded:
            return self.input.decode('base64')
        else:
            raise UploadFormatException(
                file_name=self.input.filename,
                error_message='This file was not previously encoded.'
            )