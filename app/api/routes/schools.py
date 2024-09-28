from fastapi import APIRouter
from app.core.exceptions import MaxLimitReached, NoSchoolsFound
from app.models import (
    CustomResponse,
    SchoolBase,
    SchoolsPaginated
)

from app.scraping import sparql

router = APIRouter(default_response_class=CustomResponse)

@router.get("/", response_model=SchoolsPaginated)
async def get_schools(school_filters: SchoolBase = None, limit: int = 50, exclude_par: bool = False, exclude_aut: bool = False):
    """
    Get schools from SPARQL with optional filters.
    """
    if limit > 1500:
        return MaxLimitReached
    
    schools = sparql.get_schools_from_sparql(school_filters, limit, exclude_par, exclude_aut)
    
    if not schools:
        raise NoSchoolsFound

    return SchoolsPaginated(schools=schools, total=len(schools))