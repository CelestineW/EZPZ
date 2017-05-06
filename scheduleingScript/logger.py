import datetime as dt
import MySQLdb as mc
import json
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


if __name__ == "__main__":
  print("hello, world!")
  # Testing can go here
