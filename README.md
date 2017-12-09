# National Congress of Brazil

## Setup

```console
$ pip3 install -r requirements.txt
```

## Data collection

To download the sources from Chamber of Deputies website, use `src/fetch_*.py` scripts and Scrapy's `crawl` commands:

```console
$ python3 src/fetch_propositions.py
$ cd data_collection
$ scrapy crawl chamber_of_deputies_sessions
$ cd ..
```

The files will be downloaded to `data/sources`. To extract them to `data/sessions`:

```console
$ python3 src/extract_content_files.py
```
