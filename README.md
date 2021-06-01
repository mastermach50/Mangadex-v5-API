# Mangadex-v5-API wrapper for Python
An unofficial Mangadex v5 API wrapper for python. (without async)

## Requirements Python Modules
 - requests
 - json

## Usage
```python
ch_constructor("<manga name>", <chapter number>)
```
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
## The Work done by the API
1. search for manga using given input
1. selects the first result as the required manga
1. gets the id of the selected manga
1. gets the chapter id using the manga id and chapter number
1. gets the server address of the server hosting the chapter using chapter id
1. constructs the ulr for each page of the chapter from the obtained info
1. returns all page urls as a dict

> work in progress...
> may not work properly
