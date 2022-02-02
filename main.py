from flask import Flask, render_template, request, redirect, send_file
from scraper import get_jobs
from exporter import save_to_file

app = Flask("JobScrapper")
db = {}

@app.route("/")
def home():
  return render_template("home.html")

@app.route("/report")
def report():
  word = request.args.get("word")
  if word:
    word = word.lower()
    fromDb = db.get(word)
    if fromDb:
      jobs = fromDb
    else:
      jobs = get_jobs(word)
      db[word] = jobs
  else:
    return redirect("/")
  return render_template("report.html", searchingBy=word, resultsNumber=len(jobs), jobs=jobs)

@app.route("/export")
def export():
  try:
    word= request.args.get("word")
    if not word:
      raise Exception()
    word = word.lower()
    jobs = db.get(word)
    if not jobs:
      raise Exception()
    save_to_file(jobs)
    return send_file("jobs.csv", attachment_filename=f'jobs[{word}].csv', as_attachment=True)
  except:
    return redirect("/")
    
app.run(host = "0.0.0.0")