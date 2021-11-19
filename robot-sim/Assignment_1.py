from __future__ import print_function

import time
from sr.robot import *

asilver_th = 1.86
""" float: Threshold for the control of the linear orientation of silver"""
silver_th= 78.0
"""float: Threshold for the control of linear orientation of silver perc """
dsilver_th = 0.5
""" float: threshold for distance of silver token"""
dgolden_th=0.7
""" float: threshold for distance of golden token"""
ang_th= 87.0
""" float: Threshold for the angular alignmnet of golden"""
silver = True
""" Check to tell robot what to look for golden or silver """
R = Robot()

def drive(speed, seconds):
    """
    Function for setting a linear velocity
    
    Args: speed (int): the speed of the wheels
	  seconds (int): the time interval
    """
    R.motors[0].m0.power = speed
    R.motors[0].m1.power = speed
    time.sleep(seconds)
    R.motors[0].m0.power = 25
    R.motors[0].m1.power = -25

def turn(speed, seconds):
    """
    Function for setting an angular velocity
    
    Args: speed (int): the speed of the wheels
	  seconds (int): the time interval
    """
    R.motors[0].m0.power = speed
    R.motors[0].m1.power = -speed
    time.sleep(seconds)
    R.motors[0].m0.power = 25   # to turning the robot on the spot 
    R.motors[0].m1.power = -25

def find_silver_token():
    """
    Function to find the closest silver token
    Returns:
	dist (float): distance of the closest silver token (-1 if no silver token is detected)
	rot_y (float): angle between the robot and the silver token (-1 if no silver token is detected)
    """
    dist=100
    for token in R.see():
        if token.dist < dist and token.info.marker_type is MARKER_TOKEN_SILVER:
            dist=token.dist
	    rot_y=token.rot_y
    if dist==100:
	return -1, -1
    else:
   	return dist, rot_y

def find_golden_token(): # Same as exercise solution 
    """
    Function to find the closest golden token
    Args:
	dist (float): distance of the closest golden token (-1 if no golden token is detected)
	rot_y (float): angle between the robot and the golden token (-1 if no golden token is detected)
    """
    dist= 100
    for token in R.see():
        if token.dist < dist and token.info.marker_type is MARKER_TOKEN_GOLD:
            dist=token.dist
	    rot_y=token.rot_y
    if dist==100: 
    	return -1, -1
    else:
   	return dist, rot_y

def gold_manage(dist, rot_y):
    
    if dist<dgolden_th:
        print("Close to golden")
    	
    	if -ang_th<= rot_y <= ang_th:
            View()
    	else:
            print(" safe")
            drive(50, 0.25)    
    else:
        drive(50,0.25)

def path_adjustment(rot_y): 
    "Function to adjust the path per my observation robot motor as some offset which i cant resolve"
    while rot_y < -asilver_th: 
        print("Left a bit...")
        turn(-10, 0.5)
        dist, rot_y = find_silver_token()
        
    while rot_y > asilver_th:
        print("Right a bit...")
        turn(+10, 0.5)
        dist, rot_y = find_silver_token()
    print("Ah, that'll do.")
    drive(50, 0.25)

def changeBool(dist, silver):
    """
    Function to change the Boolean value of the silver token
    
    Args:
        dist (float): distance of the closest golden token (-1 if no golden token is detected)
        silver (boolean): boolean value of the silver token (True when the robot has to search it, False if not)
    """
    if silver== False :
        if dist > dsilver_th:
            silver= True
    else:
        print("unable to detect anything")       
    return silver 
    
def View():
    """
    Function to check on the side  of the robot and choose the side without near golden token
    """
    dist_right= 100
    dist_left= 100
    
    for token in R.see():    
        if token.info.marker_type is MARKER_TOKEN_GOLD:   
            if 80<=token.rot_y<=110:
                if token.dist<=dist_right:
                    dist_right= token.dist 
                
            if -110<=token.rot_y<=-80: 
                if token.dist<=dist_left:
                    dist_left= token.dist
    
    if dist_right < dist_left:   #compare the side distances and go toward the further one
        turn(-10,0.5)
    elif dist_right > dist_left:
        turn(+10,0.5)
    
while 1:
    distg, rotg_y = find_golden_token()
    gold_manage(distg, rotg_y)
    if silver == True: # if silver is True, than we look for a silver token, otherwise for a golden one
	dist, rot_y = find_silver_token()
	if dist <= dsilver_th and -silver_th<=rot_y<=silver_th: #if we are close to the token and with the right orientation, we try grab it.
            print("Found it!")
            if R.grab(): # if we grab the token, we move the robot forward and on the right, we release the token, and we go back to the initial position
                print("Gotcha!")
	        turn(30, 2)
	        R.release()
	        turn(-30,2)
	        silver = not silver # we modify the value of the variable silver, so that in the next step we will look for the other type of token
	    else:
	        path_adjustment(rot_y)
        else:
            print("Aww, I'm not close enough.")
            
    else:
	print ("on to next box")
	dist, rot_y = find_silver_token()
	changeBool(dist, silver)    
	silver = changeBool(dist, silver)

