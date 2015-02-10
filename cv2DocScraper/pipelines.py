"""
.. module:: pipelines
   :platform: Unix
   :synopsis: Pipelines for the OpenCV Documentation Scraper

.. moduleauthor:: Theodore Brown <TheoBrown0@gmail.com>

"""

from scrapy.exceptions import DropItem
from scrapy.contrib.exporter import CsvItemExporter
from scrapy.contrib.pipeline.images import ImagesPipeline
from scrapy.exceptions import DropItem
from scrapy.http import Request
import json

class JsonWriterPipeline(object):
    """Simple class to dump items to json file
    """

    def __init__(self):
        self.file = open('items.jl', 'wb')
        
    def process_item(self, item, spider):
        line = '['+json.dumps(dict(item)) + "\n" + '],'
        self.file.write(line)
        return item
    
    
class Cv2DocscraperPipeline(object):
    def process_item(self, item, spider):
        return item
