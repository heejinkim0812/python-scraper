import requests
from bs4 import BeautifulSoup

URL = "https://www.jobkorea.co.kr/Search/?"
headers = {"User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36"}


def get_last_page(url, start=1):
  start_url = f"{url}&Page_No={start}"
  result = requests.get(start_url, headers=headers)
  soup = BeautifulSoup(result.text, 'html.parser')

  pagination = soup.find('div', {'class': 'tplPagination'})
  last_page = int(pagination.find_all('li')[-1].text.strip())
  
  next_btn = soup.find('a', {'class': 'btnPgnNext'})
  if next_btn:
    return max(last_page, get_last_page(url, last_page))
  else:
    return last_page



def extract_job(html):
  title = html.find('div', {'class': 'post-list-info'}).find('a')['title']
  company = html.find('div', {'class': 'post-list-corp'}).find('a')['title']
  location = html.find('p', {'class': 'option'}).find('span', {'class': 'loc long'}).text.strip()
  date =  html.find('p', {'class': 'option'}).find('span', {'class': 'date'}).text.strip()
  job_id = html.find('div', {'class': 'post-list-info'}).find('a')['href']
  return {
    "title": title,
    "company": company,
    "location": location,
    "date": date,
    "apply_url": f"https://www.jobkorea.co.kr{job_id}"
  }



def extract_jobs(url, last_page):
  jobs = []
  for page in range(last_page):
    print(f"Scrapping JobKorea: Page: {page+1}")
    result = requests.get(f"{url}&Page_No={page+1}")
    soup = BeautifulSoup(result.text, "html.parser")

    results = soup.find('div', class_= "list-default").find_all("li", {"class": "list-post"})
    for result in results:
      job = extract_job(result)
      jobs.append(job)
  return jobs



def get_jobs(word):
  url = f"{URL}stext={word}"
  last_page = get_last_page(url)
  jobs = extract_jobs(url, last_page)
  return jobs