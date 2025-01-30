Project for Graph Data and Knowledge

Hamburg.csv is cleaned data of socio-economic data of Hamburg.

hamburg_stops.csv is a first list of hamburg stops not completely cleaned.

With cleanup_stops.py it gets cleaned and districts get added and saved in stops_with_districts.csv.

For that we also use districts.gfs and .gml to know which busstop is in which district.

With the cleaned datas we can run the rdf_script.py which creates hamburg.ttl.

There was manuall cleaning and linking afterwards which is in hamburg_cleaned_m.ttl

shapes.ttl is there for validation purposes and visualize_sommething.py create diagrams for my report (which can also be found here).
