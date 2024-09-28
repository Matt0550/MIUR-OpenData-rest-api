import json
from typing import List
from SPARQLWrapper import SPARQLWrapper, JSON
import ssl
import urllib.request

from app.models import SchoolBase

def get_schools_from_sparql(
        school_filters: SchoolBase = None,
        limit: int = 50,
        exclude_par: bool = False,
        exclude_aut: bool = False
        
) -> List[SchoolBase]:
    """
    Execute a SPARQL query to retrieve school data with optional filters.
    
    Args:
        school_filters (SchoolFilters): School filters to apply to the query.
    Returns:
        List[SchoolBase]: List of SchoolBase instances.
    """

    # Create an SSL context to allow unsafe legacy renegotiation
    ssl_context = ssl.create_default_context()
    ssl_context.options |= ssl.OP_LEGACY_SERVER_CONNECT

    # Apply the SSL context to urllib
    opener = urllib.request.build_opener(urllib.request.HTTPSHandler(context=ssl_context))
    urllib.request.install_opener(opener)

    # Build the SPARQL query with optional filters
    filters = []

    if school_filters is not None:
        if school_filters.school_year:
            filters.append(f"?S miur:ANNOSCOLASTICO '{school_filters.school_year}' .")

        if school_filters.geographic_area:
            filters.append(f"?S miur:AREAGEOGRAFICA '{school_filters.geographic_area.upper()}' .")

        if school_filters.region:
            filters.append(f"?S miur:REGIONE '{school_filters.region.upper()}' .")

        if school_filters.province:
            filters.append(f"?S miur:PROVINCIA '{school_filters.province.upper()}' .")

        if school_filters.school_code:
            filters.append(f"?S miur:CODICESCUOLA '{school_filters.school_code.upper()}' .")

        if school_filters.school_name:
            filters.append(f"FILTER(CONTAINS(lcase(?DenominazioneScuola), lcase('{school_filters.school_name.lower()}'))) .")

        if school_filters.school_address:
            filters.append(f"FILTER(CONTAINS(lcase(?IndirizzoScuola), lcase('{school_filters.school_address.lower()}'))) .")

        if school_filters.school_postal_code:
            filters.append(f"?S miur:CAPSCUOLA '{school_filters.school_postal_code.upper()}' .")

        if school_filters.school_city_code:
            filters.append(f"?S miur:CODICECOMUNESCUOLA '{school_filters.school_city_code.upper()}' .")

        if school_filters.city_description:
            filters.append(f"?S miur:DESCRIZIONECOMUNE '{school_filters.city_description.upper()}' .")

        if school_filters.education_type_description:
            filters.append(f"FILTER(CONTAINS(lcase(?DescrizioneTipologiaGradoIstruzioneScuola), lcase('{school_filters.education_type_description.lower()}'))) .")

        if school_filters.school_email_address:
            filters.append(f"?S miur:INDIRIZZOEMAILSCUOLA '{school_filters.school_email_address}' .")

        if school_filters.school_certified_email_address:
            filters.append(f"?S miur:INDIRIZZOPECSCUOLA '{school_filters.school_certified_email_address}' .")

        if school_filters.school_website:
            filters.append(f"?S miur:SITOWEBSCUOLA '{school_filters.school_website}' .")



    # Combine the filters into the WHERE clause
    where_clause = "\n".join(filters) if filters else ""

    # Complete query
    query = f"""
        PREFIX miur: <http://www.miur.it/ns/miur#>
        SELECT ?AnnoScolastico ?AreaGeografica ?Regione ?Provincia ?CodiceIstitutoRiferimento ?DenominazioneIstitutoRiferimento ?CodiceScuola ?DenominazioneScuola ?IndirizzoScuola ?CAPScuola ?CodiceComuneScuola ?DescrizioneComune ?DescrizioneCaratteristicaScuola ?DescrizioneTipologiaGradoIstruzioneScuola ?IndicazioneSedeDirettivo ?IndicazioneSedeOmnicomprensivo ?IndirizzoEmailScuola ?IndirizzoPecScuola ?SitoWebScuola ?SedeScolastica
        WHERE {{
            ?S miur:ANNOSCOLASTICO ?AnnoScolastico .
            ?S miur:AREAGEOGRAFICA ?AreaGeografica .
            ?S miur:CAPSCUOLA ?CAPScuola .
            ?S miur:CODICECOMUNESCUOLA ?CodiceComuneScuola .
            ?S miur:CODICEISTITUTORIFERIMENTO ?CodiceIstitutoRiferimento .
            ?S miur:CODICESCUOLA ?CodiceScuola .
            ?S miur:DENOMINAZIONEISTITUTORIFERIMENTO ?DenominazioneIstitutoRiferimento .
            ?S miur:DENOMINAZIONESCUOLA ?DenominazioneScuola .
            ?S miur:DESCRIZIONECARATTERISTICASCUOLA ?DescrizioneCaratteristicaScuola .
            ?S miur:DESCRIZIONECOMUNE ?DescrizioneComune .
            ?S miur:DESCRIZIONETIPOLOGIAGRADOISTRUZIONESCUOLA ?DescrizioneTipologiaGradoIstruzioneScuola .
            ?S miur:INDICAZIONESEDEDIRETTIVO ?IndicazioneSedeDirettivo .
            ?S miur:INDICAZIONESEDEOMNICOMPRENSIVO ?IndicazioneSedeOmnicomprensivo .
            ?S miur:INDIRIZZOEMAILSCUOLA ?IndirizzoEmailScuola .
            ?S miur:INDIRIZZOPECSCUOLA ?IndirizzoPecScuola .
            ?S miur:INDIRIZZOSCUOLA ?IndirizzoScuola .
            ?S miur:PROVINCIA ?Provincia .
            ?S miur:REGIONE ?Regione .
            ?S miur:SITOWEBSCUOLA ?SitoWebScuola .
            OPTIONAL {{ ?S miur:SEDESCOLASTICA ?SedeScolastica }}
            {where_clause}
        }}
        LIMIT {limit}
    """

    
    # Configure the SPARQL connection
    sparql = SPARQLWrapper("https://dati.istruzione.it/opendata/SCUANAGRAFESTAT/query")
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    
    # Execute the query and return the results in JSON format
    response = sparql.query().convert()
    sparql_results = json.loads(response)
    bindings = sparql_results.get("results", {}).get("bindings", [])

    # Query next endpoint SCUANAGRAFEPAR
    if not exclude_par:
        sparql = SPARQLWrapper("https://dati.istruzione.it/opendata/SCUANAGRAFEPAR/query")
        sparql.setQuery(query)
        sparql.setReturnFormat(JSON)
        
        # Execute the query and return the results in JSON format
        response = sparql.query().convert()
        sparql_results = json.loads(response)
        bindings += sparql_results.get("results", {}).get("bindings", [])

    # Query next endpoint SCUANAAUTSTAT
    if not exclude_aut:
        sparql = SPARQLWrapper("https://dati.istruzione.it/opendata/SCUANAAUTSTAT/query")
        sparql.setQuery(query)
        sparql.setReturnFormat(JSON)

        # Execute the query and return the results in JSON format
        response = sparql.query().convert()
        sparql_results = json.loads(response)
        bindings += sparql_results.get("results", {}).get("bindings", [])

    # Query next endpoint SCUANAAUTPAR
    if not exclude_aut and not exclude_par:
        sparql = SPARQLWrapper("https://dati.istruzione.it/opendata/SCUANAAUTPAR/query")
        sparql.setQuery(query)
        sparql.setReturnFormat(JSON)
        
        # Execute the query and return the results in JSON format
        response = sparql.query().convert()
        sparql_results = json.loads(response)
        bindings += sparql_results.get("results", {}).get("bindings", [])
        

    # Map results to SchoolBase instances
    schools = []
    for binding in bindings:
        school = SchoolBase(
            school_year=int(binding.get("AnnoScolastico", {}).get("value", 0)),
            geographic_area=binding.get("AreaGeografica", {}).get("value"),
            region=binding.get("Regione", {}).get("value"),
            province=binding.get("Provincia", {}).get("value"),
            school_code=binding.get("CodiceScuola", {}).get("value"),
            school_name=binding.get("DenominazioneScuola", {}).get("value"),
            school_address=binding.get("IndirizzoScuola", {}).get("value"),
            school_postal_code=binding.get("CAPScuola", {}).get("value"),
            school_city_code=binding.get("CodiceComuneScuola", {}).get("value"),
            city_description=binding.get("DescrizioneComune", {}).get("value"),
            education_type_description=binding.get("DescrizioneTipologiaGradoIstruzioneScuola", {}).get("value"),
            school_email_address=binding.get("IndirizzoEmailScuola", {}).get("value"),
            school_certified_email_address=binding.get("IndirizzoPecScuola", {}).get("value"),
            school_website=binding.get("SitoWebScuola", {}).get("value")
        )
        schools.append(school)

    return schools