# Point in Polygon Analysis application
## About
This application takes an input layer of polygons and determines whether a given point lies inside, outside, or on the boundary of
a polygon. The user has the option to switch between two available algorithms to determine the location of the point: the *Ray Crossing Algorithm* and the *Winding Number Algorithm*.

## How to Use
### Input files
This application only supports  `JSON` or `GeoJSON` files.

This application only supports layers in `S-JTSK / Krovak East North (EPSG:5514)` coordinate system. Two sample polygon layers are provided in the `input_files/.` folder.

Make sure to have all the `.py` files in the same directory.

Launch the application by running `mainform.py`.

## Credits
- Protected Areas (derived `GeoJSON` file) – [ArcČR 500](https://www.arcdata.cz/produkty/geograficka-data/arccr-4)

- Police Districts (`JSON` file) – [Geoportál Praha](https://www.geoportalpraha.cz/cs/data/otevrena-data/D7283D97-3909-4684-BA99-8FECCACBC2A6)

- Used icons – courtesy of doc. Ing. Tomáš Bayer, Ph.D.


