from bs4 import BeautifulSoup
import requests
import time
import sqlite3

def loop():
# fetching resentely (few days ago) posted jobs from timesjobs website
    html_text = requests.get('https://www.timesjobs.com/candidate/job-search.html?searchType=personalizedSearch&from=submit&txtKeywords=python&txtLocation=').text
    soup = BeautifulSoup(html_text, 'lxml')
    jobs = soup.find_all('li', class_='clearfix job-bx wht-shd-bx')
    for job in jobs:
        published_date = job.find('span',class_='sim-posted').span.text
        if 'few' in published_date:
            company_name = job.find('h3', class_='joblist-comp-name').text
            skills_required = job.find('span', class_='srp-skills').text.replace(' ','')
            more_info = job.header.h2.a['href']
            print(f"\t Company Name: {company_name.strip()}")
            print(f"\t Required skill: {skills_required.strip()}")
            print(f"\t More_info: {more_info}")
            print('\n')
# saving the fetched data to the database using sqlite3
            con = sqlite3.connect('database.db')
            c = con.cursor()
            try:
                c.execute("CREATE TABLE Job_Info(Company_Name text, Skills_Required text, More_info text)")  
            except:
                pass
            c.execute("INSERT INTO Job_Info VALUES(?,?,?)",(company_name,skills_required,more_info,))
            c.execute("SELECT rowid, * FROM Job_Info ")
        con.commit()
    con.close()

def deletedatabase():
    try:
        con = sqlite3.connect("database.db")
        c = con.cursor()
        c.execute("DELETE FROM Job_Info")
    except:
        pass

while True:
    loop()
    wt = 10
    print(f"waiting {wt} minutes.....")
    time.sleep(wt * 60)
