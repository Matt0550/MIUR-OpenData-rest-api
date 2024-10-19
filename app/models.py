from datetime import datetime
from typing import Any
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field


##############
# * SCHOOL * #
##############

# Shared properties
class SchoolBase(BaseModel):
    school_year: int | None = Field(default=None) # AnnoScolastico
    geographic_area: str | None = Field(default=None) # AreaGeografica
    region: str | None = Field(default=None) # Regione
    province: str | None  = Field(default=None) # Provincia
    school_code: str | None  = Field(default=None) # CodiceScuola
    school_name: str | None  = Field(default=None) # DenominazioneScuola
    school_address: str | None  = Field(default=None) # IndirizzoScuola
    school_postal_code: str | None  = Field(default=None) # CAPScuola
    school_city_code: str | None  = Field(default=None) # CodiceComuneScuola
    city_description: str | None  = Field(default=None) # DescrizioneComune
    education_type_description: str | None  = Field(default=None) # DescrizioneTipologiaGradoIstruzioneScuola
    school_email_address: str | None  = Field(default=None) # IndirizzoEmailScuola
    school_certified_email_address: str | None  = Field(default=None) # IndirizzoPecScuola
    school_website: str | None  = Field(default=None) # SitoWebScuola

class SchoolsPaginated(BaseModel):
    schools: list[SchoolBase]
    total: int = 0
    timestamp: str = Field(default_factory=lambda: datetime.now().isoformat())
    cached: bool = False
    cache_expires: str | None = None
####################################

# New response class
class CustomResponse(JSONResponse):
    def __init__(self, content: Any, status_code: int = 200, *args, **kwargs):
        # Customize content and pass my new content...
        content = ResponseStructure(details=content, success=False if status_code != 200 else True, status_code=status_code)
        super().__init__(content=content.dict(), status_code=status_code, *args, **kwargs)

class ResponseStructure(BaseModel):
    details: Any
    success: bool = True
    status_code: int