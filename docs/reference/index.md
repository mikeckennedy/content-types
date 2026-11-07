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
The extension -\> content type table that every lookup reads from.


## Shortcut constants


Precomputed content types for very common formats, exposed as module-level attributes.


[webp](webp.md#content_types.webp)  
The content type for `.webp` files: `image/webp`.

[png](png.md#content_types.png)  
The content type for `.png` files: `image/png`.

[jpg](jpg.md#content_types.jpg)  
The content type for `.jpg` files: `image/jpeg`.

[mp3](mp3.md#content_types.mp3)  
The content type for `.mp3` files: `audio/mpeg`.

[json](json.md#content_types.json)  
The content type for `.json` files: `application/json`.

[pdf](pdf.md#content_types.pdf)  
The content type for `.pdf` files: `application/pdf`.

[zip](zip.md#content_types.zip)  
The content type for `.zip` files: `application/zip`.

[xml](xml.md#content_types.xml)  
The content type for `.xml` files: `application/xml`.

[csv](csv.md#content_types.csv)  
The content type for `.csv` files: `text/csv`.

[md](md.md#content_types.md)  
The content type for `.md` files: `text/markdown`.

[parquet](parquet.md#content_types.parquet)  
The content type for `.parquet` files: `application/vnd.apache.parquet`.

[ipynb](ipynb.md#content_types.ipynb)  
The content type for `.ipynb` files: `application/x-ipynb+json`.

[pkl](pkl.md#content_types.pkl)  
The content type for `.pkl` files: `application/octet-stream`.

[yaml](yaml.md#content_types.yaml)  
The content type for `.yaml` files: `application/yaml`.

[toml](toml.md#content_types.toml)  
The content type for `.toml` files: `application/toml`.

[sqlite](sqlite.md#content_types.sqlite)  
The content type for `.sqlite` files: `application/vnd.sqlite3`.
