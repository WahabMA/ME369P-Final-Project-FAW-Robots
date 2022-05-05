# ME369P-Final-Project-FAW-Robots
ME369P Final Project
Made By: Felix Contreras
         Andy Hassun
         Wahab Mohammed Abdul
        
To run our code and have you own working ROS game follow these simple instructions:

  1. Install Ubuntu (Whichever method works for you)
  2. Install ROS (Follow any tutorial)
  3. Install Turtlebot3 (Should be from a git clone)
  4. Now that you're done with the hard stuff, give yourself a break
  5. Create a catkin workspace
  6. Go into your src folder and navigate to src/turtlebot3_simulations/turtlebot3_gazebo:
  
      a. Place the SPYxROS.launch file in the launch folder
      b. Place SPYxROS.world file in the worlds folder
      c. Navigate to your models folder and place the playboard folder inside
      
  7. Navigate back to your catkin workspace/src folder
  8. Place the my_wall_urdf folder inside the src folder
  9. Place game-playing.py in any folder 
  10. Run the following command in a terminal window: export TURTLEBOT3_MODEL=burger
  11. Navigate to the directory where game-playing.py is placed and run the following command:
        python3 game-playing.py
      
