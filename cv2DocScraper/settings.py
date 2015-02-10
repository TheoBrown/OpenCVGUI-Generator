# Scrapy settings for cv2DocScraper project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#

BOT_NAME = 'cv2DocScraper'
BOT_VERSION = '1.0'
LOG_LEVEL = 'WARNING'
SPIDER_MODULES = ['cv2DocScraper.spiders']
NEWSPIDER_MODULE = 'cv2DocScraper.spiders'
USER_AGENT = '%s/%s' % (BOT_NAME, BOT_VERSION)
ITEM_PIPELINES = [
    'cv2DocScraper.pipelines.JsonWriterPipeline',
]