import csv

def save_to_file(jobs):
  file = open("jobs.csv", mode="w", encoding = "utf-8")
  writer = csv.writer(file)
  writer.writerow(["title", "company", "location", "link"])
  for job in jobs:
    writer.writerow(list(job.values())) #dictionary에서 value 추출하고 list에 넣어줌
  return