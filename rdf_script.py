import pandas as pd
from rdflib import Graph, Literal, Namespace, URIRef
from rdflib.namespace import RDF, XSD

# Load both files
file_path = 'Hamburg.csv'
hamburg = pd.read_csv(file_path, delimiter='\t', encoding='utf-8')
file_path2 = 'stops_with_districts.csv'
stops = pd.read_csv(file_path2, delimiter=',', encoding='utf-8')

# For each column with float numbers
# Fix german commas with international/ english comma for those numbers
float_columns = [
    'Durchschnittsalter der Bevölkerung',
    'Arbeitslose in % der 15- bis unter 65-Jährigen',
    'Ausländische Bevölkerung in %',
    'Bevölkerung mit Migrationshintergrund in % der Gesamtbevölkerung',
    'Unter 18-Jährige in % der Bevölkerung',
    'Unter 18-Jährige mit Migrationshintergrund in % der unter 18-Jährigen',
    '65-Jährige und Ältere in % der Bevölkerung',
    'Jugendquotient',
    'Altenquotient',
    'Bevölkerungsdichte in Einwohner:in/km²',
    'Personen je Haushalt',
    'Einpersonenhaushalte in % der Haushalte',
    'Haushalte mit Kindern in % der Haushalte',
    'Alleinerziehende in % der Haushalte mit Kindern',
    'Durchschnittliche Wohnungsgröße in m²',
    'Wohnfläche je Einwohner:in in m²',
    'Anzahl der Sozialwohnungen in % aller Wohnungen',
    'Anzahl der Sozialwohnungen mit Bindungsauslauf in fünf Jahren in % der Sozialwohnungen',
    'Genehmigte Wohnungen in Wohngebäuden (Neubau) je 1000 Einwohner:innen',
    'Fertiggestellte Wohnungen in Wohngebäuden (Neubau) je 1000 Einwohner:innen',
    'PKW-Bestand: Private PKW je 1000 Einwohner:innen',
    'Jüngere Arbeitslose (unter 25 Jahren) in % der 15- bis unter 25-Jährigen',
    'Ältere Arbeitslose (55 bis unter 65 Jahre) in % der 55- bis unter 65-Jährigen'
]
for col in float_columns:
    if col in hamburg.columns:
        hamburg[col] = hamburg[col].astype(str).str.replace(',', '.').str.strip()
        hamburg[col] = pd.to_numeric(hamburg[col], errors='coerce') 

# Set the namespaces
SCHEMA = Namespace("https://schema.org/")
SED = Namespace("http://heydt-schemas.com/socio-economic-data#")
LOC = Namespace("http://heydt-schemas.com/location#")
STOP = Namespace("http://heydt-schemas.com/stops#")
GEO = Namespace("https://www.w3.org/2003/01/geo/wgs84_pos#")

# Create the graph and bind the namespaces to it
g = Graph()
g.bind("loc", LOC)
g.bind("schema", SCHEMA)
g.bind("sed", SED)
g.bind("geo", GEO)
g.bind("stop", STOP)

# For each entry in the socio-economic data enter all possible triples
# Build the district ui and use it always as subject
# Use the custom namespaces as predicate
# Build literals with the entries in the socia-economic data
for _, entry in hamburg.iterrows():
    district_uri = LOC[entry["Region"]]
    g.add((district_uri, RDF.type, SCHEMA.AdministrativeArea))
    g.add((district_uri, SCHEMA.name, Literal(entry["Region"], datatype=XSD.string)))
    g.add((district_uri, SCHEMA.population, Literal(entry["Bevölkerung insgesamt"], datatype=XSD.integer)))
    g.add((district_uri, SED.districtCode, Literal(entry["Code"], datatype=XSD.integer)))
    g.add((district_uri, SED.averageAge, Literal(entry["Durchschnittsalter der Bevölkerung"], datatype=XSD.float)))
    g.add((district_uri, SED.femalePopulation, Literal(entry["Weibliche Bevölkerung"], datatype=XSD.integer)))
    g.add((district_uri, SED.foreignPopulation, Literal(entry["Ausländische Bevölkerung"], datatype=XSD.integer)))
    g.add((district_uri, SED.foreignPopulationPercentage, Literal(entry["Ausländische Bevölkerung in %"], datatype=XSD.float)))
    g.add((district_uri, SED.populationWithMigrationBackground, Literal(entry["Bevölkerung mit Migrationshintergrund"], datatype=XSD.integer)))
    g.add((district_uri, SED.populationWithMigrationBackgroundPercentage, Literal(entry["Bevölkerung mit Migrationshintergrund in % der Gesamtbevölkerung"], datatype=XSD.float)))
    g.add((district_uri, SED.under18Population, Literal(entry["Unter 18-Jährige"], datatype=XSD.integer)))
    g.add((district_uri, SED.under18PopulationPercentage, Literal(entry["Unter 18-Jährige in % der Bevölkerung"], datatype=XSD.float)))
    g.add((district_uri, SED.under18WithMigrationBackground, Literal(entry["Unter 18-Jährige mit Migrationshintergrund"], datatype=XSD.integer)))
    g.add((district_uri, SED.under18WithMigrationBackgroundPercentage, Literal(entry["Unter 18-Jährige mit Migrationshintergrund in % der unter 18-Jährigen"], datatype=XSD.float)))
    g.add((district_uri, SED.over65Population, Literal(entry["65-Jährige und Ältere"], datatype=XSD.integer)))
    g.add((district_uri, SED.over65PopulationPercentage, Literal(entry["65-Jährige und Ältere in % der Bevölkerung"], datatype=XSD.float)))
    g.add((district_uri, SED.averageAge, Literal(entry["Durchschnittsalter der Bevölkerung"], datatype=XSD.float)))
    g.add((district_uri, SED.youthQuotient, Literal(entry["Jugendquotient"], datatype=XSD.float)))
    g.add((district_uri, SED.elderlyQuotient, Literal(entry["Altenquotient"], datatype=XSD.float)))
    g.add((district_uri, SED.populationDensity, Literal(entry["Bevölkerungsdichte in Einwohner:in/km²"], datatype=XSD.float)))
    g.add((district_uri, SED.numberOfHouseholds, Literal(entry["Anzahl der Haushalte"], datatype=XSD.integer)))
    g.add((district_uri, SED.personsPerHousehold, Literal(entry["Personen je Haushalt"], datatype=XSD.float)))
    g.add((district_uri, SED.singlePersonHouseholds, Literal(entry["Einpersonenhaushalte"], datatype=XSD.integer)))
    g.add((district_uri, SED.singlePersonHouseholdsPercentage, Literal(entry["Einpersonenhaushalte in % der Haushalte"], datatype=XSD.float)))
    g.add((district_uri, SED.householdsWithChildren, Literal(entry["Haushalte mit Kindern"], datatype=XSD.integer)))
    g.add((district_uri, SED.householdsWithChildrenPercentage, Literal(entry["Haushalte mit Kindern in % der Haushalte"], datatype=XSD.float)))
    g.add((district_uri, SED.singleParentHouseholds, Literal(entry["Alleinerziehende"], datatype=XSD.integer)))
    g.add((district_uri, SED.singleParentHouseholdsPercentage, Literal(entry["Alleinerziehende in % der Haushalte mit Kindern"], datatype=XSD.float)))
    g.add((district_uri, SED.numberOfResidentialBuildings, Literal(entry["Anzahl der Wohngebäude"], datatype=XSD.integer)))
    g.add((district_uri, SED.numberOfApartments, Literal(entry["Anzahl der Wohnungen in Wohn- und Nichtwohngebäuden"], datatype=XSD.integer)))
    g.add((district_uri, SED.averageApartmentSize, Literal(entry["Durchschnittliche Wohnungsgröße in m²"], datatype=XSD.float)))
    g.add((district_uri, SED.livingSpacePerCapita, Literal(entry["Wohnfläche je Einwohner:in in m²"], datatype=XSD.float)))
    g.add((district_uri, SED.numberOfSocialHousingUnits, Literal(entry["Anzahl der Sozialwohnungen"], datatype=XSD.integer)))
    g.add((district_uri, SED.socialHousingPercentage, Literal(entry["Anzahl der Sozialwohnungen in % aller Wohnungen"], datatype=XSD.float)))
    g.add((district_uri, SED.socialHousingEndingIn5Years, Literal(entry["Anzahl der Sozialwohnungen mit Bindungsauslauf in fünf Jahren"], datatype=XSD.integer)))
    g.add((district_uri, SED.socialHousingEndingIn5YearsPercentage, Literal(entry["Anzahl der Sozialwohnungen mit Bindungsauslauf in fünf Jahren in % der Sozialwohnungen"], datatype=XSD.float)))
    g.add((district_uri, SED.approvedHousingUnits, Literal(entry["Anzahl der genehmigten Wohnungen insgesamt (Neubau und Baumaßnahmen)"], datatype=XSD.integer)))
    g.add((district_uri, SED.buildingPermitsResidential, Literal(entry["Anzahl der Baugenehmigungen für Wohngebäude (Neubau)"], datatype=XSD.integer)))
    g.add((district_uri, SED.approvedResidentialUnits, Literal(entry["Genehmigte Wohnungen in Wohngebäuden (Neubau)"], datatype=XSD.integer)))
    g.add((district_uri, SED.approvedUnitsPerThousandPeople, Literal(entry["Genehmigte Wohnungen in Wohngebäuden (Neubau) je 1000 Einwohner:innen"], datatype=XSD.float)))
    g.add((district_uri, SED.completedHousingUnits, Literal(entry["Anzahl der fertiggestellten Wohnungen insgesamt (Neubau und Baumaßnahmen)"], datatype=XSD.integer)))
    g.add((district_uri, SED.completedResidentialBuildings, Literal(entry["Anzahl der Fertigstellungen neuer Wohngebäude (Neubau)"], datatype=XSD.integer)))
    g.add((district_uri, SED.completedResidentialUnits, Literal(entry["Fertiggestellte Wohnungen in Wohngebäuden (Neubau)"], datatype=XSD.integer)))
    g.add((district_uri, SED.completedUnitsPerThousandPeople, Literal(entry["Fertiggestellte Wohnungen in Wohngebäuden (Neubau) je 1000 Einwohner:innen"], datatype=XSD.float)))
    g.add((district_uri, SED.totalUnemployed, Literal(entry["Arbeitslose insgesamt"], datatype=XSD.integer)))
    g.add((district_uri, SED.unemploymentRate, Literal(entry["Arbeitslose in % der 15- bis unter 65-Jährigen"], datatype=XSD.float)))
    g.add((district_uri, SED.unemployedUnder25, Literal(entry["Jüngere Arbeitslose (unter 25 Jahren)"], datatype=XSD.integer)))
    g.add((district_uri, SED.unemployedUnder25Percentage, Literal(entry["Jüngere Arbeitslose (unter 25 Jahren) in % der 15- bis unter 25-Jährigen"], datatype=XSD.float)))
    g.add((district_uri, SED.unemployed55To65, Literal(entry["Ältere Arbeitslose (55 bis unter 65 Jahre)"], datatype=XSD.integer)))
    g.add((district_uri, SED.unemployed55To65Percentage, Literal(entry["Ältere Arbeitslose (55 bis unter 65 Jahre) in % der 55- bis unter 65-Jährigen"], datatype=XSD.float)))
    g.add((district_uri, SED.totalTrafficAccidents, Literal(entry["Straßenverkehrsunfälle insgesamt"], datatype=XSD.integer)))
    g.add((district_uri, SED.accidentsWithInjuries, Literal(entry["Unfälle mit Personenschaden"], datatype=XSD.integer)))
    g.add((district_uri, SED.trafficFatalities, Literal(entry["Getötete Personen"], datatype=XSD.integer)))
    g.add((district_uri, SED.trafficInjuries, Literal(entry["Verletzte Personen"], datatype=XSD.integer)))
    g.add((district_uri, SED.numberOfPrivateCars, Literal(entry["PKW-Bestand: Private PKW"], datatype=XSD.integer)))
    g.add((district_uri, SED.privateCarsPerThousandPeople, Literal(entry["PKW-Bestand: Private PKW je 1000 Einwohner:innen"], datatype=XSD.float)))

# Check, if every Busstop has a District number.
# If there is then add that busstop to that district
for _, stop in stops.iterrows():
    if pd.isna(stop["Bezirk_Name"]):
        print(f"Skipping stop due to missing Bezirk_Name: {stop['stop_name']}")
        continue
    
    # Busstop names have symbols in them, that you cant use within the shortened versions
    # So we stay with the longer version
    stop_uri = URIRef(f"http://heydt-schema.com/stop/{stop['stop_name'].replace(' ', '_')}")
    #stop_uri = STOP[stop["stop_name"].replace(' ', '_')]
    district_uri = LOC[stop["Bezirk_Name"]]
    g.add((stop_uri, RDF.type, SCHEMA.BusStation))
    g.add((stop_uri, SCHEMA.name, Literal(stop["stop_name"], datatype=XSD.string)))
    g.add((stop_uri, GEO.lat, Literal(stop["stop_lat"], datatype=XSD.float)))
    g.add((stop_uri, GEO.long, Literal(stop["stop_lon"], datatype=XSD.float)))
    g.add((stop_uri, SCHEMA.containedIn, district_uri))


# Write the graph to the file
output_file = 'hamburg.ttl'
g.serialize(destination=output_file, format='turtle')
print(f"RDF data written")