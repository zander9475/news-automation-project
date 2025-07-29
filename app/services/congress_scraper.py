# pyright: reportAttributeAccessIssue=false
# congress_scraper.py

import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime
import pytz
from dateutil import parser

def get_house_schedule():
    """Scrapes the House Majority Leader's site for the daily schedule."""
    try:
        # Get today's date to verify against the House schedule
        today_str = datetime.now().strftime('%A, %B %d').upper().replace(' 0', ' ')
        print(today_str)

        # Get the main House Majority Leader page and scrape it using BeautifulSoup
        url = "https://www.majorityleader.gov/schedule/default.aspx"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find the HTML element that contains the schedule
        schedule_container = soup.find('span', id='ctl00_ctl23_ctl00_Text')

        if schedule_container:
            # Get the entire text content of the container
            full_text = schedule_container.get_text(separator=' ', strip=True)

            # Check if today's date is anywhere in that text
            if today_str in full_text.upper():
                # Use the current day of the week to create a dynamic delimiter
                day_of_week = datetime.now().strftime('%A')
                delimiter = f"On {day_of_week}, the House"

                if delimiter in full_text:
                    schedule_details = full_text.split(delimiter)[1].strip()
                
                    # Remove all unnecessary details about the House schedule
                    cutoff = "Legislation"
                    if cutoff in schedule_details:
                        schedule_details = schedule_details.split(cutoff)[0].strip()
                    
                    return f'The House {schedule_details}'
                else:
                    # Fallback in case the "On [Day]," text isn't present
                    return f'The House {full_text}'
            else:
                return f"The House is out."  

        return "House schedule not found."
    except Exception as e:
        print(f"Could not fetch House schedule: {e}")
        return "House schedule currently unavailable."


def get_senate_schedule():
    """Scrapes the Senate's site for the daily schedule."""
    try:
        # Get today's date to verify against the Senate schedule
        today_date = datetime.now().strftime("%A, %b %d, %Y").replace(' 0', ' ')

        # Get the main Senate page and scrape it using BeautifulSoup
        url = "https://www.senate.gov/"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find the HTML element that contains the schedule
        schedule_container = soup.find('article', id='proceedings_schedule')

        if schedule_container:
            # Extract the date to ensure it matches today
            date_text = schedule_container.find('h3').text.strip() #type:ignore

            # Extract the schedule text (e.g., "Convene at 10:00 a.m.") if date matches
            if today_date in date_text:
                schedule_text = schedule_container.find('span', class_="floor-schedule").text.strip().lower() #type:ignore
                return f'The Senate will {schedule_text}'
            else:
                return "The Senate is out"

        return "Senate schedule not found."
    except Exception as e:
        print(f"Could not fetch Senate schedule: {e}")
        return "Senate schedule currently unavailable."


def process_schedule_text(text, chamber):
    """Parses time from schedule text and adjusts verb tense based on current time."""

    # Find a time pattern like "3:00 p.m." or "noon"
    time_match = re.search(r'(\d{1,2}:\d{2}\s*[ap]\.?m\.?|noon|midnight)', text, re.IGNORECASE)

    if not time_match:
        return text  # No time found, return original text (e.g., "The Senate is out.")   

    time_str = time_match.group(1)
   
    # Handle special cases
    if time_str.lower() == 'noon':
        time_str = '12:00 PM'
    elif time_str.lower() == 'midnight':
        time_str = '12:00 AM'

    try:
        # Parse the time string into a datetime object
        parsed_time = parser.parse(time_str).time()

        # Combine with today's date in EST
        est = pytz.timezone('US/Eastern')
        today_date = datetime.now(est).date()
        schedule_time_est = est.localize(datetime.combine(today_date, parsed_time))

        # Get current time in EST
        now_est = datetime.now(est)

        # Compare times and change verb tense
        if now_est > schedule_time_est:
            if chamber == 'senate':
                return text.replace('will convene', 'convened')
            elif chamber == 'house':
                return text.replace('will meet', 'met')

    except (ValueError, parser.ParserError) as e:
        print(f"Could not parse time '{time_str}': {e}")

    return text


def get_congressional_activity():
    """Gets and processes schedules for both chambers."""
    raw_senate_text = get_senate_schedule()
    raw_house_text = get_house_schedule()
 
    return {
        "senate": process_schedule_text(raw_senate_text, 'senate'),
        "house": process_schedule_text(raw_house_text, 'house')
    }