from pydantic import BaseModel, Field
from typing import List

class Transcription(BaseModel):
    text: str = Field(..., description="The transcribed text in the original language")

class Translation(BaseModel):
    text: str = Field(..., description="The translated text in English")

class Illustration(BaseModel):
    description: str = Field(..., description="Description of the illustration on the folio.")

class FolioResponse(BaseModel):
    transcription: Transcription
    translation: Translation
    illustration: Illustration

class OCRResult(BaseModel):
    folios: List[FolioResponse] = Field(..., description="List of processed folios")