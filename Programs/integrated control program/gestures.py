from main import *
arduino, dashboard, move, feed = robot_connect()

#added three optional parameters speed, acceleration, and move_rate
#by default the move speed and acceleration is set to 50% of max output, and angular_move_rate is set to 1 degree
robot_command('up',move, dashboard, feed, arduino, speed = 50, acceleration= 50, angular_move_rate=15.0)
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
