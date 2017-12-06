# National Congress of Brazil

## Setup

```console
$ pip3 install -r requirements.txt
```

## Data collection

To download the sources from Chamber of Deputies website, use Scrapy's `crawl` command:

```console
$ cd data_collection
$ scrapy crawl chamber_of_deputies_sessions
$ cd ..
```

The files will be downloaded to `data/sources`.
