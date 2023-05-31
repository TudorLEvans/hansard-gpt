import os
import shutil
import sqlite3
import time
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import List, Optional

import openai
import requests
from random_user_agent.params import OperatingSystem, SoftwareName
from random_user_agent.user_agent import UserAgent
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

DOWNLOAD_PATH = os.getenv("DOWNLOAD_PATH", "D:\\hansard\\tmp")

STORAGE_PATH = os.getenv("STORAGE_PATH", "D:\\hansard")
START_DATE = datetime(2023, 3, 15)
END_DATE = datetime(2023, 3, 31)

# Rotate user agents to trick the rate limiting system into thinking I'm many people
software_names = [SoftwareName.CHROME.value]
operating_systems = [OperatingSystem.WINDOWS.value, OperatingSystem.LINUX.value]
user_agent_rotator = UserAgent(
    software_names=software_names, operating_systems=operating_systems, limit=100
)
user_agent = user_agent_rotator.get_random_user_agent()


def create_driver():
    options = webdriver.ChromeOptions()

    isExist = os.path.exists(DOWNLOAD_PATH)
    if isExist:
        shutil.rmtree(DOWNLOAD_PATH)

    os.makedirs(DOWNLOAD_PATH)
    prefs = {}
    prefs["profile.default_content_settings.popups"] = 0
    prefs["download.default_directory"] = DOWNLOAD_PATH
    prefs["directory_upgrade"] = True
    options.add_experimental_option("prefs", prefs)
    options.add_argument(f"user-agent={user_agent}")

    SERVICE = ChromeService(executable_path=ChromeDriverManager().install())
    driver = webdriver.Chrome(service=SERVICE, options=options)
    return driver


@dataclass
class Sitting:
    meeting_id: str
    title: str
    date: str
    link: str
    text: Optional[str]


def get_meetings(start_date: datetime, end_date: datetime) -> List[str]:
    meetings: List[Sitting] = []
    day_count = (end_date - start_date).days + 1
    for debate_date in (start_date + timedelta(n) for n in range(day_count)):
        string_date = debate_date.strftime("%Y-%m-%d")
        try:
            driver = create_driver()
            driver.get(f"https://hansard.parliament.uk/commons/{string_date}")
            time.sleep(4)
            WebDriverWait(driver, 5) # .until(EC.to(By.XPATH, '//a[@class="card card-section"]'))
            links = driver.find_elements(By.XPATH, '//a[@class="card card-section"]')
            for link in links:
                href = link.get_attribute("href")
                meeting_id = href.split("/")[6]
                title = href.split("/")[7]
                sitting = Sitting(meeting_id, title, string_date, href, None)
                meetings.append(sitting)
        except Exception as e:
            print("Failed to get meeting ids for date ", string_date, e)

    return meetings


def download_text(meeting_id: str) -> str:
    try:
        driver = create_driver()
        time.sleep(4)
        driver.get(
            f"https://hansard.parliament.uk/debates/GetDebateAsText/{meeting_id}"
        )
        WebDriverWait(driver, 5)
        filenames = next(os.walk(DOWNLOAD_PATH), (None, None, []))[2]
        output = ""
        for file in filenames:
            with open(os.path.join(DOWNLOAD_PATH, file), "r", encoding="utf-8") as f:
                output = f.read()
                print(output)
            os.remove(os.path.join(DOWNLOAD_PATH, file))
        return output
    except Exception as e:
        print("Failed to download file ", meeting_id, e)


if __name__ == "__main__":
    if not os.path.exists(STORAGE_PATH):
        os.makedirs(STORAGE_PATH)

    con = sqlite3.connect(os.path.join(STORAGE_PATH, "database.db"))
    try:
        cur = con.cursor()

        cur.execute("PRAGMA encoding=UTF8")

        with open("./server/sqlite/chunks.sql") as file:
            schema = file.read()
            cur.execute(schema)
            con.commit()

        with open("./server/sqlite/dumps.sql") as file:
            schema = file.read()
            cur.execute(schema)
            con.commit()

        meetings = get_meetings(START_DATE, END_DATE)

        # Loop through meetings and save them to a csv
        # ideally I want to scrape once and be able to try different embedding approaches on this data afterwards
        for meeting in meetings:
            if (
                cur.execute(
                    "SELECT meeting_id FROM text_dumps WHERE meeting_id = ?",
                    (meeting.meeting_id,),
                ).fetchone()
                is None
            ):
                meeting.text = download_text(meeting.meeting_id)
                cur.execute(
                    "INSERT INTO text_dumps (meeting_id, title, meeting_date, link, content) VALUES(?, ?, ?, ?, ?)",
                    (
                        meeting.meeting_id,
                        meeting.title,
                        meeting.date,
                        meeting.link,
                        meeting.text,
                    ),
                )
                con.commit()
        cur.close()
    except sqlite3.Error as error:
        print("Failed to read data from table", error)
    finally:
        if con:
            con.close()
            print("The Sqlite connection is closed")
