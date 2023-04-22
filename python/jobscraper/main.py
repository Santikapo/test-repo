import requests
import asyncio
import pyppeteer as p
import re
import time
import string
import time
from csv import DictWriter

hack = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3542.0 Safari/537.36'



baseURL = 'https://ca.indeed.com/jobs?'
searchQueries = ['embedded', 'project']
queryParams = {
    'l=' : 'Coquitlam%2C+BC',
    'radius=' : '35',
    'fromage=' : '1',
}
pages = 2
resultrange = pages*15

newparams = ''
for item in queryParams.items():
    temp = item[0] + item[1]
    newparams += temp + '&'

urls = []

keywords = ['rust', 'goland', 'devops', 'linux', 'python']


for search in searchQueries:
    temp = baseURL + 'q=' + search  + '&' + newparams
    urls.append(temp)
    #print(temp)


jobs = []

joblinks = []

async def main():
    browser = await p.launch()
    page = await browser.newPage()
    await page.setUserAgent(hack)

    # collects all job hrefs
    for url in urls:
        #print('checking ' + url)
        for pointer in range(0, resultrange+1, 15):
            newurl = url + f'start={pointer}'
            await page.goto(newurl)
            time.sleep(0.7)
            print(page.url)
            try:
                for i in range(15):

                    temp = await page.querySelectorAll('.jcs-JobTitle')
                    #print(temp)
                    jobhref = await page.evaluate('(yo) => yo.getAttribute("href")', temp[i])
                    
                    joblinks.append(jobhref)
            except:

                break

    print(f'found {len(joblinks)} jobs')
    print(joblinks)

    for jobhref in joblinks:
        await page.goto('https://ca.indeed.com' + jobhref)
        #job title
        title = await getElement(page, 'h1')

        # company name
        cname = await getElement(page, '.css-1h46us2.eu4oa1w0')
        cname = str(cname).rstrip('reviews')
        cname = re.sub(r'\d+', '', cname)

        # location
        loc = await getElement(page, '.css-6z8o9s.eu4oa1w0')

        # salary/hourly
        try:
            sal = await getElement(page, '.css-2iqe2o.eu4oa1w0')
        except:
            sal = ' '
            
        # job type(s)
        try:
            temp = await page.querySelectorAll('.css-rr5fiy.eu4oa1w0')
            jtype = await page.evaluate('(yo) => yo.textContent', temp[2])
            jtype = str(jtype).lstrip('Job type')
            jtype = str(jtype).split('-time')
        except:
            jtype = ' '

        body = str(await getElement(page, '#jobDescriptionText'))

        body = re.sub(r'[^ -~]', '', body) 
        #body = re.sub(r'/[^a-zA-Z\d\s:.,!?\-;$%&*\u00C0-\u00FF]', '', body)
        #r'/[^a-zA-Z\d\s:.,!?\-;$%&*\u00C0-\u00FF]/g'

        link = page.url
        jobs.append({'TITLE':title, 'COMPANY':cname, 'LOCATION':loc, 'SALARY': sal, 'JOBTYPE':jtype, 'BODY': body, 'LINK': link})


    

    
    curtime = time.strftime("%d%m%Y", time.localtime())
    fieldnames = ['TITLE', 'COMPANY', 'LOCATION', 'SALARY', 'JOBTYPE', 'BODY', 'LINK']
    with open(f'{curtime}.csv', "w", newline='') as f:
        
        writer = DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for job in jobs:
            writer.writerow(job)
    


    await browser.close()


'''
position name
company
location
job type
salary/hourly

mentions of keywords


link to job posting
date posted

'''
async def getElement(page, selector):
    try:
        temp = await page.querySelector(selector)
        temp = await page.evaluate('(yo) => yo.textContent', temp)
    except:
        return ''
    return temp

loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)


asyncio.run(main())
