"""
.. module:: items
   :platform: Unix
   :synopsis: Items for the OpenCV Documentation Scraper

.. moduleauthor:: Theodore Brown <TheoBrown0@gmail.com>

"""
import scrapy
from scrapy.item import Item, Field

class cv2Scrape(Item):
    """A group to track multiple sections in one scrape
    """
    title = Field()
    sections = Field(serializer=str)
    
class cv2Section(Item):
    """A group of related OpenCV methods
    Parameters:
        title (str): the name of this group
        functionItems (list): a list of :class:`~cv2DocScraper.items.cv2Func` items in this group
        
    """
    title = Field()
    link = Field()
    functionItems = Field(serializer=str)

class cv2Func(Item):
    """A scraper Item that tracks an individual OpenCV Method
    
    Parameters:
        title (str): the function title
        desc (str): a description of the method
        invocation(str): the method name used to call the function
        
        functionParams (dict): a dict of :class:`.cv2Param` items relevant to this method keyed by :py:attr:`~cv2DocScraper.items.cv2Param.title`
        inputParamTypes (dict):  Describes input  data types. A dictonary with key = param name and value = param type. e.g. {'thresh':double, 'type':int,'src':Array}
        outputParamTypes (dict): Describes output data types. A dictonary with key = param name and value = param type. e.g. {'dest':array}
        input (list): a list of input parameters in the order they must be given to the method e.g. [src, maxValue, adaptiveMethod, thresholdType ,...] for cv2.adaptiveThreshold(src, maxValue, adaptiveMethod, thresholdType, blockSize, C[, dst]) 
        output (list): a list of method output in the order it is received e.g. [thresh,ret] for thresh,ret = cv2.threshold(..)
        optionalInput(list): a list of input parameters that are not required
        
        
    """
    title = Field()
    link = Field()
    desc = Field()
    usage = Field()
    examples = Field()
    description = Field()
    invocation = Field()
    inputParamTypes = Field(serializer=str)
    outputParamTypes = Field(serializer=str)

    functionParams = Field(serializer=str)
    input = Field()
    optionalInput = Field()
    output = Field()
#     functionParams = Field(serializer=str)
    
class cv2Param(Item):
    """a detailed description of an input/output parameter for a cv2Func
    
    Parameters:
        title(str): the name of the parameter
        index (int): the position this parametr appears in the method invocation
        required(bool): this is a required parameter for the method
        isOutput (bool): this paramter is an output of the method
        returnIndex (int): if :py:attr:`.isOutput` returnIndex is the position that this param appears in the return statement
        description (str): a description of the nature of the paramter
        type (str): the data type structure of the param
        
        references (list): a list of parameters or built-in values relevant to this param
    """
    title= Field()
    index = Field()
    required = Field()
    isOutput = Field()
    returnIndex = Field()
    description = Field()
    references = Field()
    type = Field(serializer=str)