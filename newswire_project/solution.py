import os


if os.name=='nt':
    os.system('runscripts.bat')


elif os.name=='posix':   
    os.system('sudo apt-get install python3-pip')

   

    '''------get scrapy dependencies------'''

    os.system('sudo apt-get install python-dev python-pip libxml2-dev libxslt1-dev zlib1g-dev libffi-dev libssl-dev')
    os.system('sudo apt-get install python3 python3-dev')


    '''----install modules-----'''
    os.system('sudo python3 -m pip install scrapy')

    os.system('sudo python3 -m pip install pandas')

    '''--------run spiders---------'''

    os.system('scrapy crawl urls')
    os.system('scrapy crawl trends')

    os.system('rm select-urls.txt')

    

else:
    exit()
