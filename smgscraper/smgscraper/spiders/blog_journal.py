import re
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import SitemapSpider
from w3lib.html import remove_tags

collection_site_link_extractor = LinkExtractor(
    allow_domains=["collection.sciencemuseum.org.uk", "collection.sciencemuseumgroup.org.uk"],
    allow=["https://collection.sciencemuseumgroup.org.uk/documents/.*", "https://collection.sciencemuseumgroup.org.uk/people/.*", "https://collection.sciencemuseumgroup.org.uk/objects/.*"],
)
smg_blog_link_extractor = LinkExtractor(
    allow_domains=["blog.sciencemuseum.org.uk"], 
    deny=["^https://blog.sciencemuseum.org.uk/$", "https://blog.sciencemuseum.org.uk/tag/.*", "https://blog.sciencemuseum.org.uk/category/.*", "https://blog.sciencemuseum.org.uk/author/.*", "https://blog.sciencemuseum.org.uk/trace.*"]
)
wikipedia_link_extractor = LinkExtractor(
    allow_domains=["wikipedia.org"],
    deny=['https://en.wikipedia.org/wiki/Main_Page', 'https://en.wikipedia.org/$']
)

class BlogSpider(SitemapSpider):
    name = 'blog'
    sitemap_urls = ['https://blog.sciencemuseum.org.uk/post-sitemap1.xml', 'https://blog.sciencemuseum.org.uk/post-sitemap2.xml']
    sitemap_rules = [
        ('/', 'parse_blogpost'),
    ]

    def parse_blogpost(self, response):
        # self.logger.info(f"Found {response.url}")

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
            "links": {
                "to_collection": [link.url for link in collection_site_link_extractor.extract_links(response)],
                "to_blog": [link.url for link in smg_blog_link_extractor.extract_links(response) if not link.url.startswith(response.url)],
                "to_wikipedia": [link.url for link in wikipedia_link_extractor.extract_links(response)],
            }
        }

    @staticmethod
    def _get_caption_from_response(response):
        try:
            return response.css('div.o-main__standfirst::text').get().strip()
        except:
            return None

    @staticmethod
    def _get_text_from_paragraph(p):
        return ''.join(
                    line
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
        # self.logger.info(f"Found {response.url}")

        yield {
            "url": response.url,
            "doi": response.xpath("//*[contains(text(), 'Article DOI')]//a/text()").get(),
            "author": response.css('p.article-author a::text').get(),
            "title": remove_tags(response.css('h1').get()),
            "issue": remove_tags(response.css('p.article-journal-info a').getall()[1]),
            "keywords": self._get_keywords_from_article(response),
            "tags": [remove_tags(i).replace(r"\\r\\n", "").strip() for i in response.css('ul.tag-cloud li').getall()],
            # last element contains DOI
            "abstract": self._get_abstract_from_article(response),
            "text_by_paragraph": self._get_text_from_article(response),
            "figure_captions": self._get_figure_captions_from_article(response)
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
    
    @staticmethod
    def _get_abstract_from_article(response):
        """Get abstract if there is one, otherwise return None"""
        abstract_text = response.xpath('//section[@id="abstract"]/p').extract()

        if abstract_text:
            return remove_tags(" ".join([i for i in abstract_text if "Component DOI:" not in i]))
        else:
            return None

    @staticmethod
    def _get_text_from_article(response):
        """Combines introduction and main-body sections, stripping out tags and 'Component DOI' paragraphs"""
        intro_text_by_paragraph = [remove_tags(i) for i in response.xpath('//section[@id="introduction"]/p').extract()]
        main_text_by_paragraph = [remove_tags(i) for i in response.xpath('//section[@id="main-body"]/div/p').extract()]
        main_text_by_paragraph = [i for i in main_text_by_paragraph if "Component DOI:" not in i]

        return intro_text_by_paragraph + main_text_by_paragraph
    
    @staticmethod
    def _get_figure_captions_from_article(response):
        """Get first paragraph from sections with class 'article-figure'."""

        captions = [remove_tags(i) for i in response.xpath('//section[@class="article-figure"]/p').extract()]

        return [i for i in captions if not i.startswith("\r\n")]

