# Building Simplifier
## About
This application takes an input layer of polygons and simplifies their shape by selecting one of the following algorithms:
- Minimum Area Enclosing Rectangle,
- Wall Average,
- Longest Edge,
- Weighted Bisector.  
  
The user also has the option to construct convex hulls above input polygons by selecting one of the following algorithms:
- Jarvis Scan Algorithm (Gift Wrapping Algorithm),
- Graham Scan Algorithm.

## How to Use
### Input files
This application only supports  `JSON` or `GeoJSON` files.

This application only supports layers in `S-JTSK / Krovak East North (EPSG:5514)` coordinate system. Three sample polygon layers are provided in the `input_files/.` folder.

Make sure to have all the `.py` files in the same directory.

Launch the application by running `mainform.py`.

## Credits
- All sample polygon layers (derived `GeoJSON` files) – [Katastrální mapa ČR](https://geoportal.cuzk.cz/(S(kzic4fwtlfocr0xrbslumcwm))/Default.aspx?mode=TextMeta&side=katastr_map&metadataID=CZ-00025712-CUZK_SERIES-MD_KM-KU-SHP&menu=211)

- All icons except Longest Edge and Weighted Bisector – courtesy of doc. Ing. Tomáš Bayer, Ph.D.