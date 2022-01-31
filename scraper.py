import requests
from bs4 import BeautifulSoup

headers = {"User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36"}


def get_last_page(url):
  result = requests.get(url, headers=headers)
  soup = BeautifulSoup(result.text, "html.parser") 
  
  pagination = soup.find("div", {"class": "s-pagination"})
  last_page = pagination.find_all("a")[-2].text.strip()

  return int(last_page)



def extract_job(html):
  title = html.find("div", {"class": "flex--item fl1"}).find("a", title=True)["title"]

  company, location = html.find("h3", {"class": "fc-black-700"}).find_all("span", recursive=False) #첫 span만 가져오기
  company = company.get_text(strip=True)
  location = location.get_text(strip=True) #예쁘게 정리

  job_id = html["data-jobid"]
  apply_link = f"https://stackoverflow.com/jobs/{job_id}"

  return {"title": title, "company": company, "location": location, "apply_link": apply_link}



def extract_jobs(url,last_page):
  jobs = []
  for page in range(last_page):
    print(f"Scrapping SO: Page: {page+1}")    
    result = requests.get(f"{url}&pg={page+1}")
    soup = BeautifulSoup(result.text, "html.parser")
    
    results = soup.find_all("div", {"class": "-job"})
    for result in results:
      job = extract_job(result)
      jobs.append(job)
    
  return jobs



def get_jobs(word):
  url = f"https://stackoverflow.com/jobs?q={word}&sort=i" 
  last_page = get_last_page(url)
  jobs = extract_jobs(url, last_page)
  return jobs