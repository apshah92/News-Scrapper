import scrapy
import datetime
from datetime import date
import sys
import re



class Day:
    months={'January':1, 'February':2, 'March':3 , 'April':4 , 'May':5 , 'June':6 , 'July':7 , 'August':8 , 'September':9 , 'October':10, 'November':11 , 'December':12}

    def __init__(self,month=None,date=None,year=None):
        self.date=date
        self.month=month
        self.year=year

    def __ge__(self,day2):
        day2_date=day2.date
        day2_month=day2.month       
        day2_year=day2.year

        if self.months[self.month] >= self.months[day2_month] and self.date >= day2_date:
            return True
        else:
            return False

    def __str__(self):
        return self.month+' '+str(self.date)+','+str(self.year)
    

class urlSpider(scrapy.Spider):
    name = "urls"
    cutoff_date=Day()
    
    newsroom_url='https://www.newswire.com/newsroom'
    urlfile=None
    filename='select-urls.txt'

    start_urls = [
        newsroom_url,
    ]
    
    def __init__(self):
        while True:
            datestr=str(input('\n\nEnter a date before or equal to today\'s date. If no date is provided, period of one week will be taken as default.\nEnter a date (YYYY-MM-DD):'))  #encoding to utf-8 makes input coveersion to string identical on all platforms
            
            if datestr.strip()=='' or datestr==None:
                datestr=date.today()- datetime.timedelta(days=7)
                break
            else:
                try:
                    x=datetime.datetime.strptime(datestr,'%Y-%m-%d')    #raises value error if not equal to specified format
                    yy,mm,dd=list(map(int,datestr.split('-')))
                    datestr=date(yy,mm,dd)
                    break
                except:
                    print('Incorrect Format. Please Enter again.')
            

        #print('datestr is:',datestr)
        self.cutoff_date=self.toDayObject(datestr)
        #print('datestr printed:',self.cutoff_date)
        
        print('\nFetching news urls for the period of:',datestr,' to',date.today(),' ....')
        
    
    
    def toDayObject(self,datestring):
        datestring=re.split(' |,',datestring.strftime('%B %d,%Y'))                      #split by space or , delimeter
        return Day(datestring[0],int(datestring[1]),int(datestring[2]))   

    
    def parse(self, response):        
        nextpage=True
        self.urlfile=open(self.filename,'a+')
        for news in response.css('div.news-item.col-xs-3'):
            try:
                newsdate=news.css('div.news-item-body time::attr(datetime)').extract_first().split()[0]  #get date out of datetime string
                yr,mm,dd=list(map(int,newsdate.split('-')))
                newsdate=self.toDayObject(datetime.date(yr,mm,dd))
                #print('newsdate is:',newsdate,' newsdate type is:',type(newsdate),' cutoff date type is:',type(self.cutoff_date) )

                if newsdate >= self.cutoff_date:                                                #issue occured: use True and False in __ge__ instead 1 and -1
                    #print('\n\n',newsdate,' is greater or equal to ',self.cutoff_date)
                    newsurl=news.css('div.ni-container a::attr(href)').extract_first()          #get url of the news if it is latest than cutoff-date

                    #print('url of the news:',self.newsroom_url+newsurl)

                    self.urlfile.write('https://www.newswire.com/'+newsurl+'\n')

                else:
                    nextpage=False
                    break
            except Exception as e:
                print(e)
                
        
        if nextpage:
            next_page_num = response.css('div.chunkination.chunkination-centered  ul a::attr(href)').extract()[-1]
            next_page_num = response.urljoin(next_page_num)
            if next_page_num is not None:
                yield response.follow(next_page_num, callback=self.parse)
                
        self.urlfile.close()

        
