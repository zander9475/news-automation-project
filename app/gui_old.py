# pyright: reportUnknownMemberType=false, reportGeneralTypeIssues=false, reportOptionalMemberAccess=false

import FreeSimpleGUI as sg
import pandas as pd
import os
import json
from dotenv import load_dotenv
from datetime import datetime
# Import helper functions from other modules
from app.services.web_scraper import scrape_article_from_url, prompt_for_manual_article
from app.services.google_searcher import search_articles
from app.services.email_formatter import build_email

def create_window(title, layout):
    """Creates a standard window for the application."""
    return sg.Window(title, layout, finalize=True, element_justification='center')

def reorder_articles_ui():
    """GUI to reorder articles by specifying a new position."""
    try:
        df = pd.read_csv("data/full_articles.csv")
        titles = df['title'].tolist()
    except FileNotFoundError:
        sg.popup_error("File 'data/full_articles.csv' not found.\nPlease complete the previous steps first.")
        return

    layout = [
        [sg.Text("Reorder Articles", font=("Helvetica", 16))],
        [sg.Text("Select an article, then enter its new position number (e.g., 1 for the top).")],
        [sg.Listbox(values=titles, size=(80, 20), key="-LIST-", enable_events=True)],
        [
            sg.Text("Move selected to position:", size=(20, 1)),
            sg.Input(key="-POS-", size=(5, 1)),
            sg.Button("Move")
        ],
        [sg.Button("Save and Close", button_color=('white', 'green'))]
    ]
    window = create_window("Reorder Articles", layout)

    while True:
        event, values = window.read()
        if event in (sg.WINDOW_CLOSED, "Save and Close"):
            break
        if event == "Move":
            try:
                selected_title = values["-LIST-"][0]
                current_index = titles.index(selected_title)
                new_pos = int(values["-POS-"]) - 1
                if 0 <= new_pos < len(titles):
                    item = titles.pop(current_index)
                    titles.insert(new_pos, item)
                    window["-LIST-"].update(values=titles, set_to_index=new_pos)
                    window["-POS-"].update("") # type:ignore
                else:
                    sg.popup_error(f"Invalid position. Please enter a number between 1 and {len(titles)}.")
            except (ValueError, IndexError):
                sg.popup_error("Please select an article and enter a valid number.")
    window.close()

    df = df.set_index('title').loc[titles].reset_index()
    df.to_csv("data/full_articles.csv", index=False)

def run_gui():

    # --- Step 2: The Article Collection Screen ---
    collected_articles = []
    layout_step2 = [
        [sg.Text("Step 2: Collect Articles", font=("Helvetica", 16))],
        [sg.Text("Add articles one by one, either by URL or by entering content manually.")],
        [sg.HSeparator()],
        [sg.Text("Add Public Article:", font=("Helvetica", 12), justification='left')],
        [sg.Text("URL:", size=(15,1)), sg.Input(key="-URL-", size=(60,1)), sg.Button("Scrape URL")],
        [sg.HSeparator()],
        [sg.Text("Add Paywalled Article:", font=("Helvetica", 12), justification='left')],
        [sg.Button("Add Manually")],
        [sg.HSeparator()],
        [sg.Text("Collected Articles:", font=("Helvetica", 12), justification='left')],
        [sg.Listbox(values=[], key="-ARTICLE_LIST-", size=(70, 10))],
        [sg.Button("Remove Selected Article", button_color="red"), sg.Button("Save and Continue", button_color=('white','green'))]
    ]
    window_step2 = create_window("Article Collection", layout_step2)

    while True:
        event, values = window_step2.read()
        if event in (sg.WINDOW_CLOSED, "Save and Continue"):
            break
        if event == "Scrape URL":
            url_to_scrape = values["-URL-"]
            if not url_to_scrape:
                sg.popup_error("Please enter a URL.")
                continue
            window_step2["Scrape URL"].update(disabled=True)
            sg.popup_quick_message("Scraping... please wait.", auto_close_duration=3, non_blocking=True)
            try:
                article_data = scrape_article_from_url(url_to_scrape)
                collected_articles.append(article_data)
                window_step2["-URL-"].update("") # type:ignore
            except Exception as e:
                sg.popup_error(f"Scrape Failed: {e}\nPlease add this article manually.")
            window_step2["Scrape URL"].update(disabled=False)
        elif event == "Add Manually":
            article_data = prompt_for_manual_article()
            if article_data:
                collected_articles.append(article_data)

        elif event == "Remove Selected Article":
            selected_titles = values["-ARTICLE_LIST-"]
            if not selected_titles:
                sg.popup_error("Please select an article from the list to remove.")
                continue
            title_to_remove = selected_titles[0]
            collected_articles = [art for art in collected_articles if art['title'] != title_to_remove]

        article_titles = [art['title'] for art in collected_articles]
        window_step2["-ARTICLE_LIST-"].update(values=article_titles)
    window_step2.close()

    if not collected_articles:
        sg.popup_error("No articles were collected. Exiting.")
        return

    pd.DataFrame(collected_articles).to_csv("data/full_articles.csv", index=False)

    # --- Step 3: Reorder Articles ---
    reorder_articles_ui()

    # --- Step 4: Generate Final Email ---
    build_email()
    sg.popup_ok("Success!", "The email has been generated as 'final_email.html' in the 'output' folder." \
                "\nDouble click on this file and then copy and paste into Outlook.")