import pandas as pd
from jinja2 import Environment, FileSystemLoader
from datetime import datetime
from app.services.congress_scraper import get_congressional_activity
import ast

def build_email():
    # Load email template and article data
    df = pd.read_csv("data/full_articles.csv")

    # Convert the string representation of author list back to a Python list
    df['author'] = df['author'].apply(lambda x: ast.literal_eval(x) if isinstance(x, str) else x)
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