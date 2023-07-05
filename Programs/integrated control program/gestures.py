from main import *
arduino, dashboard, move, feed = robot_connect()
robot_command('up',move, dashboard, feed, arduino)
robot_command('up',move, dashboard, feed, arduino)
robot_command('down',move, dashboard, feed, arduino)
robot_command('down',move, dashboard, feed, arduino)
robot_command('left',move, dashboard, feed, arduino)
robot_command('left',move, dashboard, feed, arduino)
robot_command('right',move, dashboard, feed, arduino)
robot_command('right',move, dashboard, feed, arduino)

robot_command('rand',move, dashboard, feed, arduino)
robot_command('1',move, dashboard, feed, arduino)

robot_command('grab',move, dashboard, feed, arduino)
robot_command('release',move, dashboard, feed, arduino)

robot_command('right',move, dashboard, feed, arduino)
robot_command('reset',move, dashboard, feed, arduino)

robot_command('end',move, dashboard, feed, arduino)
