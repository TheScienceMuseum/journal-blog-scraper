# journal-blog-scraper

Simple python scraper using [scrapy](https://scrapy.org/) to get text and metadata from the SMG [blog](https://blog.sciencemuseum.org.uk/) and [journal](http://journal.sciencemuseum.ac.uk/).

## Running 

The only requirement is `scrapy`. All data is stored in *./output_data*. 

**Commands:**

* get all data: `make json` or `make csv` (or [any other format](https://docs.scrapy.org/en/latest/topics/feed-exports.html))
* remove all data (for recreation): `make clean`