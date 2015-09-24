from robot import *
import time
import math

pots = []

def pot_callback(data):
    pots[:] = data.position

def main(robotName):
    r = robot(robotName)
    rospy.Subscriber('/dvrk/' + robotName +  '/io/analog_input_pos_si',
                     JointState, pot_callback)

    r.move_joint_list([0.0,0.0,0.1,0.0,0.0,0.0,0.0],[0,1,2,3,4,5,6])
    joint_number = int(raw_input('enter the joint you want to test: '))
    x = []
    y = []

    raw_input('move the joint to the first extreme')
    first_extreme = r.get_current_joint_position()[joint_number]
    raw_input('move the joint to the second extreme')
    second_extreme = r.get_current_joint_position()[joint_number]

    r.move_joint_list([0.0,0.0,0.1,0.0,0.0,0.0,0.0],[0,1,2,3,4,5,6])

    range_of_motion = (math.fabs(first_extreme) + math.fabs(second_extreme))
    
    print range_of_motion

    for i in range(-50,51):
        move_amount =  (range_of_motion / 100) * i 

        r.move_joint_list([move_amount],[joint_number])
        
        time.sleep(.2)
        pot_points = []
        enc_points = []
        print x
        print y
        for c in range(0,10):
            pot_points.append(pots[joint_number])
            enc_points.append(r.get_current_joint_position()[joint_number])
            time.sleep(.01)
        pot_points_average = (math.fsum(pot_points))/10
        enc_points_average = (math.fsum(enc_points))/10
        x.append(pot_points_average)
        y.append(enc_points_average)
        


    x_mean = sum(x)/len(x)
    y_mean = sum(y)/len(y)
    a = x
    b = y
    x_points = x
    y_points = y
    a[:] = [x - x_mean for x in a]
    b[:] = [y - y_mean for y in b]
    sum_a = sum(a)
    sum_b = sum(b)
    ab = []
    for i in range(0,len(a)):
        ab.append(a[i]*b[i])
    a_squared = a
    b_squared = b
    a_squared[:] =[a ** 2 for a in a_squared]
    b_squared[:] =[b ** 2 for b in b_squared]
    sum_ab = sum(ab)
    sum_a_squared = sum(a_squared)
    sum_b_squared = sum(b_squared)
    correlation = sum_ab/(math.sqrt((sum_a_squared)*(sum_b_squared)))
    print 'correlation: ',"%.16f" % correlation
    x_standard_deviation = math.sqrt((sum_a ** 2)/(len(x_points)-1))
    print 'x standard deviation: ',"%.16f" % x_standard_deviation
    y_standard_deviation = math.sqrt((sum_b ** 2)/(len(y_points)-1))
    print 'y standard deviation: ',"%.16f" % y_standard_deviation    
    regression_slope = correlation * ( y_standard_deviation / x_standard_deviation )  
    print 'regression slope: ',"%.16f" % regression_slope
       


if __name__ == '__main__':
    if (len(sys.argv) != 2):
        print sys.argv[0] + ' requires one argument, i.e. name of dVRK arm'
    else:
        main(sys.argv[1])
