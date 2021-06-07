import re
from scrapy.spiders import SitemapSpider

class BlogSpider(SitemapSpider):
    name = 'blog'
    sitemap_urls = ['https://blog.sciencemuseum.org.uk/post-sitemap1.xml', 'https://blog.sciencemuseum.org.uk/post-sitemap2.xml']
    sitemap_rules = [
        ('/', 'parse_blogpost'),
    ]

    def parse_blogpost(self, response):
        self.logger.info(f"Found {response.url}") # ... scrape product ...
        yield {
            "url": response.url,
            "author": response.css('h2.c-hero__subtitle a::text').get() or self._get_author_from_author_string(response.css('h2.c-hero__subtitle::text').get()),
            "title": response.css('h1::text').get(),
            "caption": response.css('div.o-main__standfirst::text').get(),
            "categories": response.css('dl.o-dl dd a[rel="category tag"]::text').getall(),
            "tags": response.css('dl.o-dl dd a[rel="tag"]::text').getall(),
            "text_by_paragraph": [
                self._get_text_from_paragraph(p) for p in response.css('div.o-textstyles p')
             ],
        }

    @staticmethod
    def _get_text_from_paragraph(p):
        return ' '.join(
                     line.strip()
                     for line in p.xpath('.//text()').extract()
                     if line.strip()
                 )

    @staticmethod
    def _get_author_from_author_string(text):
        """Get author name from 'By Author Name on xx/xx/xx'"""

        return re.search(r"By (.*) on", text).group(1)

