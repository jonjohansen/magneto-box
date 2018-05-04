from ulinalg import *
from umatrix import *
import math as m

"""
This function takes in two vectors (intended to be the accelerometer data and magnetometer data) with three dimensions.
It then finds the appropriate rotation matrix to rotate one vector (the accelerometer data) to [0,0,1], such that the entirety
of the force is pointed down. Then it applies this same rotation matrix to the magnetometer data, such that the positive 
Z-direction is inverse and parallell to the direction of gravity (which, in layman's terms means "up").
It can rotate any arbitrary vector in three dimensions to any arbitrary vector in three dimensions, unless they are parallell,
which will give a div by zero error.
"""

def rotate(vector):
    # Creating reference matrix
    b = umatrix.matrix([[0,0,1]])
    # Finding cross product of the matrix "vector" and reference matrix
    v = cross(vector,b)
    # Reshapes reference matrix to a column
    b.shape=(3,1)
    # Finds vector dot b (cosine of angle between them)
    c = dot(vector,b)
    # Skew-symmetric cross-product matrix of v
    v_x = umatrix.matrix([[0,v[0,2],-v[0,1]],[-v[0,2],0,v[0,0]],[v[0,1],-v[0,0],0]])
    # Three dimensional identity matrix
    I = umatrix.matrix([[1,0,0],[0,1,0],[0,0,1]])
    # Calculating rotation matrix
    R = I+v_x+dot(v_x,v_x)*(1/(c[0,0]+1))

    return(R)

def matrixise(accelerometertuple, magnetotuple):
    # Fetching accelerometer data
    ax = accelerometertuple[0]
    ay = accelerometertuple[1]
    az = accelerometertuple[2]

    # Creating a matrix-object which contains the force vector
    vector = umatrix.matrix([[ax,ay,az]])
    # Copying force vector
    vector2 = vector.copy()
    # Reshaping copied force vector into a column vector as opposed to a row vector
    vector2.shape = (3,1)
    # Calculating magnitude squared of force vector by dot multiplying it with its copy
    length = dot(vector,vector2)
    # Finding the inverse of the force vector magnitude as a float value
    inverse = 1 / m.sqrt(length[0,0])
    # Normalizing force vector to unit size
    vector = vector*inverse

    # Finding rotation matrix
    rotationmatrix = (rotate(vector))
    # Fetching magnetic data
    mx = magnetotuple[0]
    my = magnetotuple[1]
    mz = magnetotuple[2]
    # Creating a matrix-object which contains the magnetic field vector
    magnetomatrix = umatrix.matrix([[mx,my,mz]])
    # Rotating the magnetic field vector with the rotation matrix found for gravitational force
    rotatedmatrix = dot(magnetomatrix,rotationmatrix)
    # Converting rotated values to a list
    rotatedtuple = [rotatedmatrix[0,0],rotatedmatrix[0,1],rotatedmatrix[0,2]]

    # Treat data with conversion
    return(rotatedtuple)

def test():
    # Test data. This test data is very basic but tests the convertion methods 

    # Simulating the box being upside down.
    print("\nSimulating the box being upside down.")
    accelerodata = (0.001, 0.001, -1) 
    magneticdata = (0, 0, -100)
    returndata = matrixise(accelerodata, magneticdata)
    print("The expected Z value should be 100, we got " + str(returndata[2])+"\n")

    # Simulates that the box is on its side
    print("Simulates that the box is on its side")
    accelerodata = (0, -1, 0) 
    magneticdata = (0, -100, 0)
    returndata = matrixise(accelerodata, magneticdata)
    print("The expected Z value should be 100, we got " + str(returndata[2]))

#test()