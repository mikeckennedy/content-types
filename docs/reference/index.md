# API Reference


content-types is intentionally tiny: lookup functions for both directions (filename -\> type, and type -\> extension), the mapping table behind them, and a handful of precomputed shortcut constants for the most common formats.


## Forward lookup


Map a filename, bare extension, Path, or URL to its MIME / content type.


[get_content_type()](get_content_type.md#content_types.get_content_type)  
Return the most specific, commonly accepted MIME type for a filename or extension.


## Reverse lookup


Map a MIME / content type back to its file extension(s) -- the inverse of get_content_type.


[guess_extension()](guess_extension.md#content_types.guess_extension)  
Return the canonical file extension for a MIME / content type.

[guess_all_extensions()](guess_all_extensions.md#content_types.guess_all_extensions)  
Return every known file extension for a MIME / content type, canonical first.


## Mapping data


The underlying extension -\> content-type table (364 entries; keys have no leading dot).


[EXTENSION_TO_CONTENT_TYPE](EXTENSION_TO_CONTENT_TYPE.md#content_types.EXTENSION_TO_CONTENT_TYPE)  
dict() -\> new empty dictionary


## Shortcut constants


Precomputed content types for very common formats, exposed as module-level attributes.


[webp](webp.md#content_types.webp)  
str(object='') -\> str

[png](png.md#content_types.png)  
str(object='') -\> str

[jpg](jpg.md#content_types.jpg)  
str(object='') -\> str

[mp3](mp3.md#content_types.mp3)  
str(object='') -\> str

[json](json.md#content_types.json)  
str(object='') -\> str

[pdf](pdf.md#content_types.pdf)  
str(object='') -\> str

[zip](zip.md#content_types.zip)  
str(object='') -\> str

[xml](xml.md#content_types.xml)  
str(object='') -\> str

[csv](csv.md#content_types.csv)  
str(object='') -\> str

[md](md.md#content_types.md)  
str(object='') -\> str

[parquet](parquet.md#content_types.parquet)  
str(object='') -\> str

[ipynb](ipynb.md#content_types.ipynb)  
str(object='') -\> str

[pkl](pkl.md#content_types.pkl)  
str(object='') -\> str

[yaml](yaml.md#content_types.yaml)  
str(object='') -\> str

[toml](toml.md#content_types.toml)  
str(object='') -\> str

[sqlite](sqlite.md#content_types.sqlite)  
str(object='') -\> str
