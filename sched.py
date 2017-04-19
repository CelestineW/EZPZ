import datetime as dt
import MySQLdb as mc
import sys

class Logging():

  # Input: None
  # Output: None
  # Description: Opens the logfile and initializes the class
  def __init__(self):
    self.logFile = open("sched_log_"+ str(dt.time()), "w")

  # Input: None
  # Output: None
  # Description: CLoses the log file
  def close(self):
    self.logFile.close()

  # Input: String to Log
  # Output: None
  # Description: Adds data to the log file 
  def log(self,logString):
    self.logFile.write(logString)

def testDB():
  try:
    connection = mc.connect (host = "maria.db",
                              user = "cblake2",
                              passwd = "PasswOrd",
                              db = "company")
  
  except mc.Error as e:
    print("Error %d: %s" % (e.args[0], e.args[1]))
    sys.exit(1)

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
  for r in result:
    print r

  cursor.close()
  connection.close()

if __name__ == "__main__":
  print("hello, world!")
  log = Logging()
  log.log("Test")
  log.close()
  testDB()
