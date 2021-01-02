import os
import requests
import json
import re

session = requests.Session()

def login(username, password):
    username = username.strip()
    password = password.strip()
    url = "https://sis.erp.bits-pilani.ac.in/psp/sisprd/?cmd=login&languageCd=ENG&"
    payload = {
        "userid": username,
        "pwd": password
    }
    r = session.post(url, data=payload)
    if r.url[-1] == 'T':
        return 1
    return 0    
    
def get_courses():
    url = "https://sis.erp.bits-pilani.ac.in/psc/sisprd/EMPLOYEE/HRMS/c/SA_LEARNER_SERVICES.SSS_STUDENT_CENTER.GBL?FolderPath=PORTAL_ROOT_OBJECT.CO_EMPLOYEE_SELF_SERVICE.HC_SSS_STUDENT_CENTER&IsFolder=false&IgnoreParamTempl=FolderPath%2cIsFolder&PortalActualURL=https%3a%2f%2fsis.erp.bits-pilani.ac.in%2fpsc%2fsisprd%2fEMPLOYEE%2fHRMS%2fc%2fSA_LEARNER_SERVICES.SSS_STUDENT_CENTER.GBL&PortalContentURL=https%3a%2f%2fsis.erp.bits-pilani.ac.in%2fpsc%2fsisprd%2fEMPLOYEE%2fHRMS%2fc%2fSA_LEARNER_SERVICES.SSS_STUDENT_CENTER.GBL&PortalContentProvider=HRMS&PortalCRefLabel=Student%20Center&PortalRegistryName=EMPLOYEE&PortalServletURI=https%3a%2f%2fsis.erp.bits-pilani.ac.in%2fpsp%2fsisprd%2f&PortalURI=https%3a%2f%2fsis.erp.bits-pilani.ac.in%2fpsc%2fsisprd%2f&PortalHostNode=HRMS&NoCrumbs=yes&PortalKeyStruct=yes"
    r = session.get(url)
    p = re.compile('[A-Z]+ [A-Z][0-9]+[-][A-Z][0-9]')
    result = p.findall(str(r.content))
    return result

def main(username, password):
    login_status = login(username, password)
    if login_status == 1:
        print("Logged in successfully")
    else:
        print("Unauthorized, check username and password")
        return -1
    print("Fetching registered courses...")
    courses = get_courses()
    return courses
