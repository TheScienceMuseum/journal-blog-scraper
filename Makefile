.PHONY: clean

json: ./output_data/blog.json

csv: ./output_data/blog.csv

./output_data/blog.%: 
	cd smgscraper && scrapy crawl blog -o ../$@

clean:
	rm -f output_data/*
