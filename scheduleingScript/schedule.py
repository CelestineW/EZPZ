from logger import Logging

#########################################################
# Generate Schedule                                     #
# Input: logging instance                               #
#        a dictionary containing:                       #
#                     key : class name                  #
#                value(s) : [[start time, end time]]    #
# Output: a dictionary containing:                      #
#                     key : class name                  #
#                value(s) : [start time, end time]      #
#########################################################
def generateSchedule(log, schedule, courses, n):
  # While there are classes left to schedule
  time_slot = [0,0]

  log.log("[schedGen] generating schedule...")
  
  # find class with earliest start time
  time_slot,course = findEarliest(courses)
  log.log("[schedGen] Earliest time found was " + course + " at " + str(time_slot))
  while time_slot[0] != 25 and len(schedule) < n:
    # add to schedule
    schedule[course] = time_slot

    # remove conflicting class times from list 
    updateTimes(courses, time_slot[1], course)

    # find class with earliest start time
    time_slot,course = findEarliest(courses)
    log.log("[schedGen] Earliest time found was " + course + " at " + str(time_slot))
    
  log.log("[schedGen] Finished generating schedule")
  return schedule 
    
#########################################################
# Finds earliest time slot available                    #
# Input: a dictionary containing:                       #
#                     key : class name                  #
#                value(s) : [[start time, end time]]    #
# Output: earliest time slot available                  #
#         course title                                  #
#########################################################
def findEarliest(times):
  time_slot = [25,0]
  course = ""

  for key in times:
    for slot in times[key]:
      # If time slot is earliest so far, update variables
      if slot[0] < time_slot[0]:
        time_slot = [slot[0],slot[1]]
        course = key

  return time_slot, course

#########################################################
# Updates the times list                                #
# Input: a dictionary containing:                       #
#                     key : class name                  #
#                value(s) : [[start time, end time]]    #
#        end time                                       #
#        course title                                   #
# Output: None                                          #
#########################################################
def updateTimes(times, end_time, course):
  # Removes scheduled class from listing
  times.pop(course, None)

  # 'Removes' all uncompatiable time slots (sets them to 25) 
  for key in times:
    for i in range(len(times[key])):
      if times[key][i][0] < end_time:
        times[key][i][0] = 25
        times[key][i][1] = 25

if __name__ == "__main__":
  print("hello, world!")

