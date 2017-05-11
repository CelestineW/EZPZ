from logger import Logging
from database import dbAccess
from schedule import generateSchedule
from schedule import findEarliest
import datetime as dt
import json
import sys

def necessary(log, nCourses, pCourses, oCourses, n):
  schedule = {}
  schedule = generateSchedule(log, schedule, nCourses, n)
  schedule = generateSchedule(log, schedule, pCourses, n)
  schedule = generateSchedule(log, schedule, oCourses, n)
  return schedule

def prefered(log, pCourses, oCourses, n):
  schedule = {}
  schedule = generateSchedule(log, schedule, pCourses, n)
  schedule = generateSchedule(log, schedule, oCourses, n)
  return schedule

def ordinary(log, oCourses, n):
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
  return courses

def pref_test(log):
  print("No Preference")
  oCourses = inLineInput(log) 
  print("Preference")
  pCourses = inLineInput(log) 
  print("Necessary")
  nCourses = inLineInput(log) 

  schedule = necessary(log, nCourses, pCourses, oCourses, numCourses)
  log.log(str(schedule))

def retest(log):
  print("No Preference")
  oCourses = inLineInput(log) 
  
  times, course = findEarliest(oCourses)
  oCourses[course].remove(times)

  schedule = ordinary(log, oCourses, len(oCourses))
  log.log(str(schedule))

if __name__ == "__main__":
  print("hello, world!")
  log = Logging()
  
<<<<<<< HEAD
  numCourses = int(raw_input("Please enter number of Courses: "))
  regen = raw_input("Would you like to regenerate the schedule?: ")
  
  if regen.lower() == "n":
    pref_test(log)
  else:
    retest(log)
  
=======
  #data = json.load(sys.stdin)
  courses = {"CSMC 201":[[9,10],[11,12]], "CMSC 202":[[11,12]]}
  schedule = ordinary(log, courses, len(courses))
>>>>>>> 0cd162e48571c0d98cb363c0d9d850e2be7646ba
  print("Goodbye, world!")

  log.close()
