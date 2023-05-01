# DEM Analysis application
## About
This application constructs a Digital Elevation Model (DEM) over an input file of 3D points.

The user is able to perform basic DEM analysis by having the option to generate contour lines and color DEM according to slope/aspect of constructed triangles.

## How to Use
### Input files
This application only supports  `CSV` file format.

This application only supports layers in `S-JTSK / Krovak East North (EPSG:5514)` coordinate system. A sample layer is provided in the `input_files/.` folder.

Make sure to have all the `.py` files in the same directory.

Launch the application by running `mainform.py`.

## Credits
- Sample 3D point layer (derived `CSV` file) – [Stahovací služba WFS – Bodová pole](https://geoportal.cuzk.cz/(S(15gnxgccc5nrhruiixeabcmv))/Default.aspx?mode=TextMeta&side=wfs&metadataID=CZ-CUZK-WFS-BODOVAPOLE-P&metadataXSL=metadata.sluzba)

- Icons – courtesy of doc. Ing. Tomáš Bayer, Ph.D.