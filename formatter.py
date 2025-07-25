import pandas as pd
from jinja2 import Environment, FileSystemLoader
from datetime import datetime
from congress_scraper import get_congressional_activity

def build_email():
    # Load email template and article data
    df = pd.read_csv("data/full_articles.csv")

    # Replace 'nan' in empty author column with empty string
    df['author'] =df['author'].fillna('')

    # Get the congressional activity
    congress_activity = get_congressional_activity()

    env = Environment(loader=FileSystemLoader("templates"))
    template = env.get_template("email_template.html")

    # Get today's date and format it as Month dd, yyyy (ex: July 21, 2025)
    current_date = datetime.now().strftime('%B %d, %Y')

    # Insert data into the template
    html = template.render(
        articles = df.to_dict(orient="records"),
        today_date = current_date,
        congress_activity = congress_activity
        )

    # Save html string to a file
    with open("output/final_email.html", "w", encoding="utf-8") as f:
        f.write(html)