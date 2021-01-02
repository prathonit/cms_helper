import os
import requests
import json
from htmldom import htmldom

# Login to cms and open developer console by pressing ctrl+shift+i
# Select console from top ribbon
# Paste this in the console:
# document.cookie.split(";").filter(item=>item.trim().startsWith("MoodleSession"))[0].split("=")[1];
# Copy the string that is printed on the console without the quotes ""

BASE_URL = "https://cms.bits-hyderabad.ac.in/"
MOODLE_SESSION = input("Paste your cms/moodle session cookie here: ")

cookies = {'MoodleSession': MOODLE_SESSION}


def get_courses_and_session_key():
    global cookies
    COURSE_CODES = []
    session_key = None
    url = BASE_URL + 'my/'
    r = requests.get(url, cookies=cookies)
    dom = htmldom.HtmlDom()
    dom = dom.createDom(str(r.content))
    courses = dom.find("a")
    for course in courses:
        link = course.attr("href")
        if "https://cms.bits-hyderabad.ac.in/course/view.php?id=" in link:
            course_title = course.attr("title")
            if course_title == "Undefined Attribute":
                continue
            course_id = link.split("=")[1]
            COURSE_CODES.insert(len(COURSE_CODES), (course_id, course_title))
        if "https://cms.bits-hyderabad.ac.in/login/logout.php?sesskey=" in link:
            session_key = link.split("=")[1]
    return (COURSE_CODES, session_key)

def get_enrol_id(course_id):
    global cookies
    enrol_id = None
    url = BASE_URL + 'course/view.php?id=' + str(course_id.strip())
    r = requests.get(url, cookies=cookies)
    dom = htmldom.HtmlDom()
    dom = dom.createDom(str(r.content))
    links = dom.find("a")
    for link in links:
        link = link.attr("href")
        if "https://cms.bits-hyderabad.ac.in/enrol/self/unenrolself.php?enrolid=" in link:
            enrol_id = link.split("=")[1]
            return enrol_id
    return 0

def unenrol(enrol_id, session_key):
    global cookies
    url = BASE_URL + 'enrol/self/unenrolself.php'
    data = {
        "enrolid": enrol_id,
        "confirm": 1,
        "sesskey": session_key
    }
    r = requests.post(url, cookies=cookies, data=data)
    if r.status_code == 200:
        return True
    return False

def main():
    try:
        course_and_session_key = get_courses_and_session_key()
        courses = course_and_session_key[0]
        session_key = course_and_session_key[1]
        user_input = input("Un-enrol me from all courses, press (Y/y) for yes, any other key for un-enrolling from selective courses: ")
        consent = 0
        if user_input.strip().lower() == 'y':
            consent = 1
        for course in courses:
            course_id = course[0]
            course_title = course[1]
            if consent != 1:
                user_input = input("Unenrol me from " + course_title + ", press (Y/y) for yes, and other key for no: ")
                if user_input.strip().lower() != 'y':
                    continue
            enrol_id = get_enrol_id(course_id)
            print(course_title)
            r = unenrol(enrol_id, session_key)
            if r:
                print("Successfully un-enrolled...")
            else:
                print("Failed to un-enrol")
            print("***")
    except Exception as e:
        print("Error, make sure the moodle session cookie is valid")


if __name__ == "__main__":
    main()