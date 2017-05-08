from logger import Logging
from database import dbAccess
from schedule import generateSchedule
import datetime as dt
import MySQLdb as mc
import json
import sys

def necessary(log, nCourse, pCourse, oCourse, n):
  schedule = {}
  schedule = generateSchedule(log, schedule, nCourses, n)
  schedule = generateSchedule(log, schedule, pCourses, n)
  schedule = generateSchedule(log, schedule, oCourses, n)
  return schedule

def prefered(log, pCourse, oCourse, n):
  schedule = {}
  schedule = generateSchedule(log, schedule, pCourses, n)
  schedule = generateSchedule(log, schedule, oCourses, n)
  return schedule

def ordinary(log, oCourse, n):
  schedule = {}
  schedule = generateSchedule(log, schedule, oCourses, n)
  return schedule

def inLineInput(log):
  courses = {}

  userCourses = []
  
  user_choice = raw_input("Please enter a course (q to quit): ")
  while user_choice != 'q':
    userCourses.append(user_choice)
    user_choice = raw_input("Please enter a course (q to quit): ")

  db = dbAccess(log)

  for c in userCourses:
    courses[c] = db.request(c)
  
  db.close()

  print(courses)
  schedule = {}
  schedule = generateSchedule(log, schedule, courses, len(courses))
  print(schedule)

if __name__ == "__main__":
  print("hello, world!")
  log = Logging()
  
  #data = json.load(sys.stdin)
  courses = {"CSMC 201":[[9,10],[11,12]], "CMSC 202":[[11,12]]}
  schedule = ordinary(log, courses, len(courses))
  print("Goodbye, world!")

  log.close()
