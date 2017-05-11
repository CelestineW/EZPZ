import datetime as dt
import MySQLdb as mc
import sys

class Logging():

  ######################################################
  # Initializes the logging file                       #
  # Input: None                                        #
  # Output: None                                       #
  # Description: Opens the logfile and                 #
  #              initializes the class                 #
  ######################################################
  def __init__(self):
    self.logFile = open("log_sched"+ str(dt.time()), "w")
    self.log("[logging] Logging Created")
  
  ######################################################
  # Close the logging file                             #
  # Input: None                                        #
  # Output: None                                       #
  # Description: CLoses the log file                   #
  ######################################################
  def close(self):
    self.log("[logging] Logging Closed")
    self.logFile.close()

  ######################################################
  # Writes to the logging file                         #
  # Input: String to Log                               #
  # Output: None                                       #
  # Description: Adds data to the log file             #
  ######################################################
  def log(self,logString):
    self.logFile.write(logString + '\n')


class dbAccess():
  def __init__(self, log):
    try:
      self.log = log
      
      """
      Amazon Web Services RDS Free Tier
      
      Hostname: ezpz.c6pi6kjq4ljd.us-east-1.rds.amazonaws.com
      Database Name: ScheduleMe
      Username: client
      Password: *You already know*
      """
      self.connection = mc.connect (host = "ezpz.c6pi6kjq4ljd.us-east-1.rds.amazonaws.com",
                                    user = "client",
                                    passwd = "Passw0rd",
                                    db = "ScheduleMe")
      self.cursor = self.connection.cursor()
      self.log.log("[dbAccess] Connection to database Established")
    except mc.Error as e:
      self.log.log("[dbAccess] Error %d: %s" % (e.args[0], e.args[1]))

  def close(self):
    try:
      self.cursor.close()
      self.connection.close()
      self.log.log("[dbAccess] connection to database closed")
    except mc.Error as e:
      self.log.log("[dbAccess] Error %d: %s" % (e.args[0], e.args[1]))
    
  def request(self, course):
    try:
      sql_command = """
      SELECT section.course_id, course.title, section.sec_id, professor.last_name, professor.first_name, section.room_num, time_slot.days, time_slot.start_hr, time_slot.start_min, time_slot.end_hr, time_slot.end_min
      FROM course
      INNER JOIN section
      ON section.course_id = course.course_id
      INNER JOIN professor
      ON section.prof_id = professor.prof_id
      INNER JOIN time_slot
      ON section.time_slot_id = time_slot.time_slot_id
      WHERE section.course_id = """
      sql_command = sql_command + '"' + course + '";'
      self.cursor.execute(sql_command)
      result = self.cursor.fetchall()
      self.log.log("[dbAccess] command executed")
      
      course = []
      for r in result:
        section = [int(r[7]) + int(r[8]) * .01 , int(r[9]) + int(r[10]) *.01]
        course.append(section)
        self.log.log("[dbAccess] " + str(r))
      return course 
    except mc.Error as e:
      self.log.log("[dbAccess] Error %d: %s" % (e.args[0], e.args[1]))


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
def generateSchedule(log, times):
  # While there are classes left to schedule
  schedule = {}
  time_slot = [0,0]

  log.log("[schedGen] generating schedule...")
  
  # find class with earliest start time
  time_slot,course = findEarliest(times)
  log.log("[schedGen] Earliest time found was " + course + " at " + str(time_slot))
  while time_slot[0] != 25:
    # add to schedule
    schedule[course] = time_slot

    # remove conflicting class times from list 
    updateTimes(times, time_slot[1], course)

    # find class with earliest start time
    time_slot,course = findEarliest(times)
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

def testDB(log):
  try:
    """
    Amazon Web Services RDS Free Tier

    Hostname: ezpz.c6pi6kjq4ljd.us-east-1.rds.amazonaws.com
    Database Name: ScheduleMe
    Username: client
    Password: *You already know*
    """
    connection = mc.connect (host = "ezpz.c6pi6kjq4ljd.us-east-1.rds.amazonaws.com",
                             user = "client",
                             passwd = "Passw0rd",
                             db = "ScheduleMe")
  
    log.log("[testDB] Connection created")
    sql_command = """
    SELECT section.course_id, course.title, section.sec_id, professor.last_name, professor.first_name, section.room_num, time_slot.days, time_slot.start_hr, time_slot.start_min, time_slot.end_hr, time_slot.end_min
    FROM course
    INNER JOIN section
    ON section.course_id = course.course_id
    INNER JOIN professor
    ON section.prof_id = professor.prof_id
    INNER JOIN time_slot
    ON section.time_slot_id = time_slot.time_slot_id
    WHERE section.course_id = "CMSC 202";
    """

    cursor = connection.cursor()
    
    cursor.execute(sql_command)
    result = cursor.fetchall()
    log.log("[testDB] command executed")
    for r in result:
      log.log("[testDB]" + str(r))
      
    cursor.close()
    connection.close()
    log.log("[testDB] connection closed")
  except mc.Error as e:
    log.log("Error %d: %s" % (e.args[0], e.args[1]))

if __name__ == "__main__":
  print("hello, world!")
  log = Logging()
  #testDB(log)
  
  courses = {}

  db = dbAccess(log)
  courses["CMSC 202"] = db.request("CMSC 202")
  courses["CMSC 201"] = db.request("CMSC 201")
  db.close()

  # courses = {"CSMC 201":[[9,10],[11,12]], "CMSC 202":[[11,12]]}

  print(courses)
  schedule = generateSchedule(log, courses)
  print(schedule)

  log.close()
