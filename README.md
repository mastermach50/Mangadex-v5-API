# Mangadex-v5-API wrapper for Python
An unofficial Mangadex v5 API wrapper for python. (without async)

## Requirements Python Modules
 - requests
 - json

## Usage
```python
ch_constructor("<manga name>", "<chapter number>")
```
Note : The chapter no should be a string.
A dictionary containing the page no and the url of the page will be returned.
```
{
'page 1': 'url',
'page 2': 'url',
.
.
.
'page n': 'url'
}
```
> work in progress...
