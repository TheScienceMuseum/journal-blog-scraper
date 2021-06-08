# journal-blog-scraper

Simple python scraper using [scrapy](https://scrapy.org/) to get text and metadata from the SMG [blog](https://blog.sciencemuseum.org.uk/) and [journal](http://journal.sciencemuseum.ac.uk/).

## Running 

The only requirement is `scrapy`. All data is stored in *./output_data*. 

**Commands:**

* get all data: `make json` or `make csv` (or [any other format](https://docs.scrapy.org/en/latest/topics/feed-exports.html))
* remove all data (for recreation): `make clean`

## Data Formats

### Blog

| field name      | description | example |
| ----------- | ----------- | ----------- |
| `url`      | - | *https://blog.sciencemuseum.org.uk/re-framing-my-vision-for-2020/* |
| `author`   | Listed in *BY <AUTHOR_NAME> ON <WRITTEN_DATE>* above title.  | *Dr Jo  Gooding MA(RCA/V&A) FHEA* |
| `date` | Listed in *BY <AUTHOR_NAME> ON <WRITTEN_DATE>* above title. Format not necessarily consistent. | 5 July 2020 |
| `title` | - | *Re-framing my vision for 2020* |
| `caption` | Large text below title. | *Dr Jo Gooding, founder and director of Design Research Associates, reflects on how her historical research on National Health Service (NHS) glasses has inspired her current mission to support innovation in disability-related design.*|
| `categories` | Bottom of the page, following '*CATEGORISED*'. | *["Collections and Objects", "Science in the news"]*
| `tags` | Bottom of the page, following '*TAGGED*'. | *["design", "history of medicine", "medicine galleries"]*
| `text_by_paragraph` | Main article text split into paragraphs. | *["As expected, the year 2020 has presented the opportunity for attention-grabbing puns relating to vision. The term \u201920-20 vision\u2019 is used in ophthalmological circles to express visual acuity, a person with perfect vision can read an eye-test chart from a distance of 20 feet.", "However, metaphorically, the phrase has come to mean having focus and clarity but this meaning is often regarded as offensive and \u201cableist\u201d to people with visual impairment.", "It was this, the recently renewed gratitude for the NHS and the anniversary of its creation that led me to reflect on how my historical research on NHS glasses has inspired my current mission to support innovation in disability-related design.", ...]*

### Journal

| field name      | description | example |
| ----------- | ----------- | ----------- |
| `url`      | - | *http://journal.sciencemuseum.ac.uk/browse/issue-13/a-review-of-st-fagans/* |
| `doi` | - | *http://dx.doi.org/10.15180/201304* |
| `author` | - | *Miriam Dafydd* |
| `title` | -  | *A museum by the people for the people? A review of St Fagans National Museum of History\u2019s new galleries* |
| `issue` | - | *Spring 2020, Issue 13*
| `keywords` | Under 'Keywords' heading at top of each article. | *["Exhibition review", "St Fagans", "Wales", "National museum", "Social Engagement", "Museology", "Socially Engaged Practices", "Community Engagement"]*
| `tags` | At the bottom of each article, above references. | *["Exhibitions", "Industrial revolution", "Museology", "Museum collections", "Curating", "Public engagement", "Science museums", "Public history", "Industrial heritage"]*
| `text_by_paragraph` | Main article text split into paragraphs. | *["Situated near Cardiff, St Fagans National Museum of History is not an obvious candidate for an activist museum. First opened in 1948, the Museum set out to represent the lived experience of the Welsh through a selection of historic buildings, plucked from their original locations across the nation and rebuilt in its idyllic grounds. It is now one of Wales\u2019 most popular visitor attractions, and for many who grew up in Wales, like me, it is a place of fond school-trip memories where one entered a strange, but familiar, mini historic Wales.", "In 2018, the Museum completed its six-year \u2018Making History\u2019 redevelopment project...", ...]*

