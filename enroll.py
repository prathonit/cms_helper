from erp_login import main as erp_helper
import os
import requests
import json
import re
from htmldom import htmldom

MOODLE_SESSION = input("Paste your cms/moodle session cookie here: ")

cookies = {'MoodleSession': MOODLE_SESSION}

def get_searchable_course_list(courses, enroll_in_main_section=1):
    final_list = []
    for course in courses:
        course = course.strip()
        course = course.replace('-', ' ')
        final_list.append(course)
        if enroll_in_main_section == 1:
            if course[-2] != 'L':
                continue
            course = course[0: -1]
            final_list.append(course)
    return final_list

def search_for_course(course):
    course = course.split(' ')
    course = "+" + course[0] + " +" + course[1] + " +" + course[2]
    url = "https://cms.bits-hyderabad.ac.in/course/search.php"
    payload = {
        "q": course,
        "areaids": "core_course-course"
    }
    r = requests.get(url, params=payload, cookies=cookies)
    dom = htmldom.HtmlDom()
    dom = dom.createDom(str(r.content))
    course_id = dom.find("div.courses").find("div")[0].attr("data-courseid")
    return course_id

def enroll_in_course(course_id):
    url = "https://cms.bits-hyderabad.ac.in/enrol/index.php"
    r = requests.get(url, params={"id": course_id}, cookies=cookies)
    dom = htmldom.HtmlDom()
    dom = dom.createDom(str(r.content))
    form = dom.find("form").find("input")
    data = {}
    for input in form:
        data[input.attr("name")] = input.attr("value")
    url = "https://cms.bits-hyderabad.ac.in/enrol/index.php"
    r = requests.post(url, data=data, cookies=cookies)
    if r.status_code == 200:
        return 1
    return 0

def main():
    username = input("Enter erp username: ")
    password = input("Enter erp password: ")
    courses = erp_helper(username, password)
    print("Generating sections list...")
    enroll_in_main_section = input("Do you want to enroll in L sections of lectures (Y/y) for yes, anything else for n: ")
    if enroll_in_main_section.strip().lower() == 'y':
        courses = get_searchable_course_list(courses, 1)
    else:
        courses = get_searchable_course_list(courses, 0)
    LENGTH = len(courses)
    COURSE_IDS = []
    print("Fetching course ids...")
    counter = 1
    for course in courses:
        print("Fetched {} out of {}".format(counter, LENGTH))
        try:
            course_course_id = search_for_course(course)
            COURSE_IDS.append(course_course_id)
        except Exception as e:
            COURSE_IDS.append(0)
        counter = counter + 1
    print("Attempting to enroll...")
    counter = 0
    for course_id in COURSE_IDS:
        print("Attempting to enroll for {}".format(courses[counter]))
        r = enroll_in_course(course_id)
        if r == 1:
            print("Successfully enrolled")
        else:
            print("Failed to enroll")
        print("***")
        counter = counter + 1


if __name__ == "__main__":
    main()