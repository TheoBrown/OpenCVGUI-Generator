"""
.. module:: cv2Doc_spider
   :platform: Unix
   :synopsis: A scrapy spider implementation to parse the OpenCV documentation

.. moduleauthor:: Theodore Brown <TheoBrown0@gmail.com>

"""

import scrapy
from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from scrapy import log, spider

from cv2DocScraper.items import cv2Func, cv2Param, cv2Section, cv2Scrape

import GlobalConfig

from PyUtils.Files import convertString
from scrapy.shell import inspect_response


log.start(loglevel = log.WARNING)

class cv2Spider(BaseSpider):
    """This spider scrapes the documentation of `OpenCV <http://docs.opencv.org>`_ and buils a json dataset describing functionality
    

    """
    name = "opencv"
#     start_urls = ["http://docs.opencv.org/modules/imgproc/doc/miscellaneous_transformations.html"]
    start_urls = ['http://docs.opencv.org/modules/imgproc/doc/filtering.html',
                  'http://docs.opencv.org/modules/imgproc/doc/histograms.html']
    
    inspectResponse = False

    
    def parse(self, response):
        """Parses the XML response of an OpenCV documentation page.
        Scrapes out individual methods, and then parses the input and output necessary to implement the method.
        

        """

        items = cv2Scrape()
        items['sections'] = dict()
        items['title'] = 'test'
        hxs = HtmlXPathSelector(response)
        classList = hxs.select('.//div[@class="section"]')[0].select('.//div[@class="section"]')
        
        headerSections = hxs.select('.//div[@class="section"]')
        for hsec in headerSections:
            if hsec.select('.//h1/text()') != []:
                headerItem = None
                headerItem = cv2Section() #
                headerItem['functionItems'] = dict()
                headerTitle = str(hsec.select('.//h1/text()').extract())
                headerItem['title'] = headerTitle.strip('[').strip(']').strip("u'").strip("'")
                self.log('entering header group %s' %headerItem['title'], level=log.WARNING)

                functionSecs = hsec.select('.//div[@class="section"]')
                for funcSec in functionSecs:
#                     inspect_response(response) #jump into console to check xml layout
                    
                    if funcSec.select('.//dl[@class="pyfunction"]') == []:
                        pass #this seciton is not an API reference, skip it
                    else:
                            
                        funcItem = None
                        funcItem = cv2Func()
                        funcItem['title'] = str(funcSec.select('@id').extract()[0].strip())
                        self.log('entering function %s' %funcItem['title'], level=log.WARNING)
                        if self.inspectResponse:
                            if funcItem['title'] == 'cvtcolor':
                                from scrapy.shell import inspect_response
                                inspect_response(response) #jump into console to check xml layout
                        else:
                            pass
                        
                        funcItem['description'] = funcSec.select('.//p/text()').extract()[0]
                        funcItem['invocation'] = funcSec.select('.//dl[@class="pyfunction"]/dt/@id').extract()
    
                        pList = funcSec.select('.//tr[@class="field-odd field"]/td/ul/li') #gets a list of parameters of this function item
    
                        self.log('with fields %s ' %funcItem.fields, level=log.WARNING)
    
                        pythonParamInvocationList = funcSec.select('.//dl[@class="pyfunction"]/dt/text()').extract() #a list of parameters for the python function
    #                         cParamList = funcSec.select('.//dl[@class="function"]/dt/text()').extract()
                        cPPPArgsTypes = funcSec.select('.//dl[@class="function"]/dt/@id').extract() #a list of parameters for the c++ function implementation
                        
                        funcItem = self.parseCPPArgTypes(funcItem,cPPPArgsTypes) 
    
                        funcItem = self.parsePythonArgsFormat(funcItem, pythonParamInvocationList)
                        
                        funcItem = self.parseParamList(funcItem, pList)
                        
                        self.log('%s functions found %s' %(funcItem['title'],funcItem) , level=log.WARNING)
                                    
                        headerItem['functionItems'][funcItem['title']] = dict(funcItem) #copy this item into the header class
                        self.log('%s functions added to header %s' %(funcItem['title'],headerItem['title']) , level=log.WARNING)
                        
                    items['sections'][headerItem['title']] = dict(headerItem)

#                 items.append(headerItem)
                    
#                     funcItem['params'] = subFunc.select('.//tr').select('.//li')
#                 cv2Section['functions'] = hsec.select('.//div[@class="section"]')
                

#                 item['name'] = subFunc.select('')
#                 self.log('functions found as %s' %, level=log.WARNING)

#         self.log('Response found from url %s' % response.url, level=log.WARNING)


        return items
    
    def parseCPPArgTypes(self,funcItem,argsList):
        """Parses the input and output parameter types for the C++ method
        
        Parameters:
            funcItem (:class:`~cv2DocScraper.items.cv2Func`): the method whose arguments will be parsed
            argList (list): a list of textual data extracted from  an :py:class:HtmlXPathSelector object pertaining to the C++ method implementation
        
        Returns:
            funcItem (:class:`~cv2DocScraper.items.cv2Func`): the updated method with inserted parameter information
        
        Yields:
            inputParamTypes - fills in this dictionary in the given (:class:`~cv2DocScraper.items.cv2Func`)
            outputParamTypes -fills in this dictionary in the given (:class:`~cv2DocScraper.items.cv2Func`)
        
        """
        funcItem['inputParamTypes'] = dict()
        funcItem['outputParamTypes'] = dict()

        for invocationType in argsList:#invocationType is the c++ invocation string
            sepSides = invocationType.strip(')').split('(')
            output = sepSides.pop(0) #the first half of sepSides is the output of the C++ method
            outputList = [istr.strip() for istr in output.split(', ') if istr !='']
            if len(sepSides) != 1:
                self.log('%s parse did not work, extra argument in list %s' %(funcItem['title'],sepSides) ,level=log.WARNING) 
            else:
                for outputPair in outputList:
                    outputParamName = outputPair.split(' ')[1]
                    outputParamType = outputPair.split(' ')[0]
                    outputParamName = str(outputParamName)
                    outputParamType = str(outputParamType)
                    if outputParamName == u'void':
                        pass #this method has void output, no need to document
                    else:
                        if outputParamName in funcItem['outputParamTypes'].keys():
#                         if funcItem['outputParamTypes'][outputParamName] != None:
                            if outputParamType in funcItem['outputParamTypes'][outputParamName]:
                                #all is good , no need for double
                                pass
                            else:
                                funcItem['outputParamTypes'][outputParamName].append(outputParamType)
                        else:
                            funcItem['outputParamTypes'][outputParamName] = []
                            funcItem['outputParamTypes'][outputParamName].append(outputParamType)
                            
                inputStr = sepSides[-1] #the last part of sepSides is the input of the C++ method
                inputList = [istr.strip() for istr in inputStr.split(', ') if istr !='']  #crates a list of input arguments
                
                for inputPair in inputList:
                    inputParamName = inputPair.split(' ')[1]
                    inputParamName= str(inputParamName)
                    inputParamType = inputPair.split(' ')[0]
                    inputParamType = str(inputParamType)
                    if inputParamName in funcItem['inputParamTypes'].keys():
#                     if funcItem['inputParamTypes'][inputParamName] != None:
                        if inputParamType in funcItem['inputParamTypes'][inputParamName]:
                            #this parameter is already described, it can be skipped
                            pass
                        else: #add the type info for this parameter to the function
                            funcItem['inputParamTypes'][inputParamName].append(inputParamType)
                    else:
                        funcItem['inputParamTypes'][inputParamName] = []
                        funcItem['inputParamTypes'][inputParamName].append(inputParamType)
                        
        self.log('inputTypes %s' %funcItem['inputParamTypes'] ,level=log.WARNING) 
        self.log('outputParamTypes %s' %funcItem['outputParamTypes'] ,level=log.WARNING) 

        return funcItem

    def parsePythonArgsFormat(self,funcItem,argsList):
        """Parses the input and output parameter types from the **python** method

        Parameters:
            funcItem (:class:`~cv2DocScraper.items.cv2Func`): the method whose arguments will be parsed
            argList (list):  a list of textual data extracted from  an :py:class:`~scrapy.selector.HtmlXPathSelector` object pertaining to the python method implementation
            
        
        Returns:
            funcItem (:class:`~cv2DocScraper.items.cv2Func`): the updated method with inserted parameter information
        
        Yields:
            input - sets method input for (:class:`~cv2DocScraper.items.cv2Func`)
            output - sets method output for (:class:`~cv2DocScraper.items.cv2Func`)
            optionalInput - sets method optionalInput for (:class:`~cv2DocScraper.items.cv2Func`)
            
        """
        if argsList[0] == u'\n':
            argsList.pop(0)
        self.log('%s arglist' %argsList ,level=log.WARNING) 
        requiredParamsList = argsList.pop(0).split(', ')
#         self.log('requiredParamsList %s' %requiredParamsList ,level=log.WARNING) 

        requiredParams = [convertString(cleanArg.strip()) for cleanArg in requiredParamsList if cleanArg != '']
        funcItem['input'] = requiredParams

        remainingArgs = ''.join([arg for arg in argsList])
        remainingArgsList = remainingArgs.split(u'\u2192')
#         self.log('remainingArgsList %s' %remainingArgsList ,level=log.WARNING) 

        resultArgs = remainingArgsList.pop(-1).strip()
        resultArgsList = resultArgs.split(', ')
        resultParamList = [convertString(cleanArg.strip()) for cleanArg in resultArgsList if cleanArg != '']
        funcItem['output'] = resultParamList

        optionalParams = ''.join([arg for arg in remainingArgsList])
        optionalArgsList = optionalParams.split(', ')
        optionalParamsList = [convertString(cleanArg.strip()) for cleanArg in optionalArgsList if cleanArg != '']
#         self.log('optionalParamsList %s' %optionalParamsList ,level=log.WARNING) =
        funcItem['optionalInput'] = optionalParamsList
        return funcItem

    def parseParamList(self,funcItem,argsList):
        """Sets the `functionParam` parameter of the given (:class:`~cv2DocScraper.items.cv2Func`). 
        Creates :class:`~cv2DocScraper.items.cv2Param` for each paramter pertaining to this method
        
        Parameters:
            funcItem (:class:`~cv2DocScraper.items.cv2Func`): the method whose arguments will be parsed
            argList (list):a list of textual data extracted from  an :py:class:`HtmlXPathSelector` object pertaining to the python method implementation
        
        Returns:
            funcItem (:class:`~cv2DocScraper.items.cv2Func`): the updated method with inserted parameter information
            
        """
        funcItem['functionParams'] = dict()
        self.log('parseParamList %s ' %argsList, level=log.WARNING)

        for i, argumentElement in enumerate(argsList):
            newParam = None
            newParam = cv2Param()
#             self.log('with fields %s ' %funcItem.fields, level=log.WARNING)

            textList = argumentElement.select('.//text()').extract()
            newParam['title'] = str(textList.pop(0))
            newParam = self.setupParamData(funcItem, newParam)            
#             self.log('new param  %s %s ' %(newParam['index'],newParam['title']), level=log.WARNING)

            descriptionString = ''.join([convertString(cleanArg) for cleanArg in textList if cleanArg != ''])
            newParam['description'] = descriptionString
            referencedArgs = argumentElement.select('.//tt[@class="docutils literal"]//text()').extract()
            if len(referencedArgs) != 0:
                newParam['references'] = [convertString(cleanArg.strip()) for cleanArg in referencedArgs if cleanArg != '']
#             paramList.append(newParam)
#             self.log('parseParamList with keys %s ' %funcItem.keys(), level=log.WARNING)
#             self.log('parseParamList with values %s ' %funcItem.items(), level=log.WARNING)

            funcItem['functionParams'][newParam['title']] = dict(newParam)
            i+=1
        return funcItem
    
    def setupParamData(self,functionItem,paramItem):
        """Parses information for the :class:`~cv2DocScraper.items.cv2Param` paramItem. Updates it based on data already set in the :class:`~cv2DocScraper.items.cv2Func`
        
        Parameters:
            funcItem (:class:`~cv2DocScraper.items.cv2Func`): the method whose arguments will be parsed
            paramItem (:class:`~cv2DocScraper.items.cv2Param`): a parameter whos values will be updated in the :class:`~cv2DocScraper.items.cv2Func` item
        
        Returns:
            paramItem (:class:`~cv2DocScraper.items.cv2Param`): the updated parameter
        
        Yields:
            sets the values: `index`, `required`, `type`, and `isOutput` in the paramItem

        """
        self.log('looking for %s' %paramItem['title'] ,level=log.WARNING) 
        searchName = paramItem['title']
        if searchName in functionItem['input']:
            paramItem['index'] = functionItem['input'].index(searchName)
            paramItem['required'] = True
            paramItem['isOutput'] = False
            if searchName in functionItem['inputParamTypes'].keys():
                paramItem['type'] = functionItem['inputParamTypes'][searchName]

        elif searchName in functionItem['optionalInput']:
            paramItem['index'] = len(functionItem['input'])+functionItem['optionalInput'].index(searchName)#optional inputs are always listed after (right) of inputs
            paramItem['required'] = False
            paramItem['isOutput'] = False
            if searchName in functionItem['inputParamTypes'].keys():
                paramItem['type'] = functionItem['inputParamTypes'][searchName]

        if searchName in functionItem['output']:
            paramItem['returnIndex'] = functionItem['output'].index(searchName)
            paramItem['isOutput'] = True
            if searchName in functionItem['outputParamTypes'].keys():
                paramItem['type'] = functionItem['outputParamTypes'][searchName]
        return paramItem
    

