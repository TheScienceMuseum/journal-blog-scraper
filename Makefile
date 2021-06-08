.PHONY: clean

json: ./output_data/blog.json ./output_data/journal.json

csv: ./output_data/blog.csv ./output_data/journal.csv

./output_data/blog.%: 
	cd smgscraper && scrapy crawl blog -o ../$@

./output_data/journal.%: 
	cd smgscraper && scrapy crawl journal -o ../$@

clean:
	rm -f output_data/*
