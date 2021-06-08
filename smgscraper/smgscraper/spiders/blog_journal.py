import re
import scrapy
from w3lib.html import remove_tags

class BlogSpider(scrapy.spiders.SitemapSpider):
    name = 'blog'
    sitemap_urls = ['https://blog.sciencemuseum.org.uk/post-sitemap1.xml', 'https://blog.sciencemuseum.org.uk/post-sitemap2.xml']
    sitemap_rules = [
        ('/', 'parse_blogpost'),
    ]

    def parse_blogpost(self, response):
        self.logger.info(f"Found {response.url}")
        yield {
            "url": response.url,
            "author": response.css('h2.c-hero__subtitle a::text').get() or self._get_author_from_author_string(remove_tags(response.css('h2.c-hero__subtitle').get())),
            "date": self._get_date_from_author_string(remove_tags(response.css('h2.c-hero__subtitle').get())),
            "title": response.css('h1::text').get(),
            "caption": self._get_caption_from_response(response),
            "categories": response.css('dl.o-dl dd a[rel="category tag"]::text').getall(),
            "tags": response.css('dl.o-dl dd a[rel="tag"]::text').getall(),
            "text_by_paragraph": [
                self._get_text_from_paragraph(p) for p in response.css('div.o-textstyles p')
             ],
        }

    @staticmethod
    def _get_caption_from_response(response):
        try:
            return response.css('div.o-main__standfirst::text').get().strip()
        except:
            return None

    @staticmethod
    def _get_text_from_paragraph(p):
        return '\n'.join(
                     line.strip()
                     for line in p.xpath('.//text()').extract()
                     if line.strip()
                 )

    @staticmethod
    def _get_author_from_author_string(text):
        """Get author name from 'By Author Name on xx/xx/xx'"""

        return re.search(r"By (.*) on", text).group(1).strip()
    
    @staticmethod
    def _get_date_from_author_string(text):
        """Get date from 'By Author Name on xx/xx/xx'"""

        return re.search(r"By (?:.*) on (.*)", text).group(1).strip()

class JournalSpider(scrapy.Spider):
    name = 'journal'
    url_prefix = "http://journal.sciencemuseum.ac.uk"
    start_urls = ['http://journal.sciencemuseum.ac.uk/browse/']

    def parse(self, response):
        article_page_links = [self.url_prefix + slug for slug in response.css('a[rel="bookmark"]::attr(href)').getall()]
        yield from response.follow_all(article_page_links, self.parse_article)

        pagination_links = response.css('a.icon-arrow-right::attr(href)').getall()
        yield from response.follow_all(pagination_links, self.parse)

    def parse_article(self, response):
        self.logger.info(f"Found {response.url}")

        yield {
            "url": response.url,
            "doi": response.xpath("//*[contains(text(), 'Article DOI')]//a/text()").get(),
            "author": response.css('p.article-author a::text').get(),
            "title": remove_tags(response.css('h1').get()),
            "issue": remove_tags(response.css('p.article-journal-info a').getall()[1]),
            "keywords": self._get_keywords_from_article(response),
            "tags": [remove_tags(i).replace(r"\\r\\n", "").strip() for i in response.css('ul.tag-cloud li').getall()],
            # last element contains DOI
            "text": remove_tags("\n".join(response.xpath('//div[@id="text-1"]/p').extract()[:-1])).encode('utf-8').decode("utf-8")
        }
    
    @staticmethod
    def _get_keywords_from_article(response):
        """Uses the regex to find a comma-separated list in the section with ID 'keywords', as some keywords are nested in <p> tags
        and others are not"""

        try: 
            keywords_section = remove_tags(response.css('section#keywords').get())
            return [item.strip() for item in re.findall(r"(.+?)(?:,|$)", keywords_section) if "\\" not in item and item.strip()]

        except:
            return []        
