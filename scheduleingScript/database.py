import logger
import MySQLdb as mc

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

if __name__ == '__main__':
  print("Hello, world!")
  # This will have testing stuff for the db?

