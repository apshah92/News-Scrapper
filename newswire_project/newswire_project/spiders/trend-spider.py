import scrapy
import pandas as pd


class trendSpider(scrapy.Spider):
    name = "trends"

    filename='select-urls.txt'

    urls=[]
    trends_locations={}
    trends_categories={}
    trends_tags={}

    def __init__(self):
        with open(self.filename,'r') as urlfile:
            for line in urlfile:
                self.urls.append(line.strip())

        print('\nAnalyzing News Trends...')
        
    def start_requests(self):
        for url in self.urls:
            yield scrapy.Request(url=url, callback=self.parse)

        self.getTopTrends()

    def parse(self, response):
        
        location=response.css('div.html-content strong.date-line.color-pr::text').extract_first().replace('(Newswire.com) -','').strip() #css attributes for location-date line
        location=location.split(',')
       
        '''
            location could be in form of city,state,date,year or state,date,year
            so delete last two indices from list. remaining items compose location.
        '''
        
        del location[-1]                 
        del location[-1]

        location=','.join(location)
        #print('\n\nlocation:',location)
        
        items=response.css('p.mb-0')

        try:                                                #urls may not have either of location, category or tags

            '''---------get location-------------'''
            if location in self.trends_locations:
                self.trends_locations[location]+=1
            else:
                self.trends_locations[location]=1



            '''---------get categories-------------'''
            categories=items[0].css('a::text').extract()           

            for ctgr in categories:                         
                if ctgr in self.trends_categories:
                    self.trends_categories[ctgr]+=1
                else:
                    self.trends_categories[ctgr]=1

            
            '''----------get tags------------------'''
            tags=items[1].css('a::text').extract()          
            
            for tag in tags:
                tag=tag.replace('#','')
                if tag in self.trends_tags:
                    self.trends_tags[tag]+=1
                else:
                    self.trends_tags[tag]=1
        except:
            pass
        


    def getTopTrends(self):        
            top_locatons=sorted(self.trends_locations.items(),key=lambda kv:kv[1],reverse=True)
            top_categories=sorted(self.trends_categories.items(),key=lambda kv:kv[1],reverse=True)
            top_tags=sorted(self.trends_tags.items(),key=lambda kv:kv[1],reverse=True)

            #print('\n\n',top_locatons,'\n\n',top_categories,'\n\n',top_tags)
            
            trends_df=pd.DataFrame({'Top Locations':[i[0] for i in top_locatons[:10]],'Top Categories':[i[0] for i in top_categories[:10]],'Top Tags':[i[0] for i in top_tags[:10]]})

            print('\nTop trends by Location, Categories and Tags: ')
            print('\n\n')
            print(trends_df.iloc[:,0])
            print('\n\n')
            print(trends_df.iloc[:,1])
            print('\n\n')
            print(trends_df.iloc[:,2])
        

          
        
        
