import requests
from bs4 import BeautifulSoup

LIMIT = 50
URL = f"https://kr.indeed.com/jobs?q=python&limit={LIMIT}"


def get_last_page(start=0):
    url = f"{URL}&start={start * LIMIT}"
    result = requests.get(url)
    soup = BeautifulSoup(result.text, "html.parser")

    pagination = soup.find("div", {"class": "pagination"})
    links = pagination.find_all("a")  #find_all: list로 추출
    pages = []

    for link in links:
        page_numb = link.find("span").string # 그냥 link.string 해줘도 됨
        if page_numb:  
            pages.append(int(page_numb))

    max_page = pages[-1]

    next_button = pagination.find("a", {"aria-label": "다음"})
    if next_button:  # 다음 버튼이 있으면 재귀함수
        return max(max_page, get_last_page(max_page))
    else:
        return max_page



def extract_job(html):
    # 공고제목
    title = html.find("h2", {"class": "jobTitle"}).find("span", title=True).string

    # 회사이름
    company = html.find("span", {"class": "companyName"})
    if company is not None:
      company_anchor = company.find("a")  #링크주소
      if company_anchor is not None:      #있으면
          company = str(company_anchor.string)
      else:
          company = str(company.string)
      company = company.strip()
    else:
      company = None
      
    # 회사위치
    location = html.find("div", {"class": "companyLocation"}).string

    # 개별 url link
    job_id = html["data-jk"]

    return {
        "title": title,
        "company": company,
        "location": location,
        "link": f"https://kr.indeed.com/%EC%B1%84%EC%9A%A9%EB%B3%B4%EA%B8%B0?jk={job_id}&from=web&vjs=3"
    }



def extract_jobs(last_page):
  jobs = []
  for page in range(last_page):
    print(f"Scrapping Indeed: Page: {page+1}")
    result = requests.get(f"{URL}&start={page * LIMIT}")
    soup = BeautifulSoup(result.text, "html.parser")

    results = soup.find_all("a", {"class": "fs-unmask"})
    for result in results:
        job = extract_job(result)
        jobs.append(job)

  return jobs



def get_jobs():
  last_page = get_last_page()
  jobs = extract_jobs(last_page)
  return jobs