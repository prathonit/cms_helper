# CMS Un-enroller
Helps to unenrol from all or selective courses from CMS (Moodle). 

## Installation and Instructions
1) Clone this repo. 
2) Login to CMS as you normally do with google sign in. After opening the dashboard press ```ctrl+shift+i``` or go to dropdown menu > more tools > developers tools.
3) On the dev tools window choose console from the top ribbon.
4) Paste the following command in the console: 
  ```
    document.cookie.split(";").filter(item=>item.trim().startsWith("MoodleSession"))[0].split("=")[1];
  ```
5) Copy the string printed on the console without the quotes.
6) Open up a terminal and navigate to project folder and type ```pip install -r requirements.txt``` to install all dependencies.

## Enroll to all registered courses
1) On the terminal execute enroll.py file using ```python enroll.py```
2) You will be asked to enter your erp username, password and Moodle Session cookie which we copied on our clipboard in previous steps.
3) Follow the instructions, the status of enrollment will be shown on the terminal.

## Un-enroll from courses
1) On the terminal execute unenroll.py file using ```python unenroll.py```
2) You will be asked to paste your moodle session cookie. 
3) Follow the instructions, you can choose to un-enroll from all or only selected courses. 

