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
    b = umatrix.matrix([[0,0,1]])           #creating reference matrix
    v = cross(vector,b)                     #finding cross product of the matrix "vector" and reference matrix
    b.shape = (3,1)                         #reshapes reference matrix to a column
    c = dot(vector,b)                       #finds vector dot b (cosine of angle between them)
    v_x = umatrix.matrix([[0,v[0,2],-v[0,1]],[-v[0,2],0,v[0,0]],[v[0,1],-v[0,0],0]])    #skew-symmetric cross-product matrix of v
    I = umatrix.matrix([[1,0,0],[0,1,0],[0,0,1]])   #three dimensional identity matrix
    R = I+v_x+dot(v_x,v_x)*(1/(c[0,0]+1))           #calculating rotation matrix
#    result = (dot(vector,R))                        #testing that vector dot rotation matrix is in fact identical to reference matrix
#    if m.fabs(result[0,0])<0.00001:                 #removing irrelevant numerical errors
#        result[0,0]=0                               
#    if m.fabs(result[0,1])<0.00001:                 #removing irrelevant numerical errors
#        result[0,1]=0
#    if m.fabs(result[0,2])<0.00001:                 #removing irrelevant numerical errors
#        result[0,2]=0
#    resulttest=result.copy()                        #copying result vector
#    resulttest.shape=(3,1)                          #reshaping result vector
#    return(R)

def matrixise(accelerometertuple, magnetotuple):
    a = accelerometertuple[0]           #fetching x-component of the accelerometer data
    b = accelerometertuple[1]           #fetching y-component
    c = accelerometertuple[2]           #and z-component

    vector=umatrix.matrix([[a,b,c]])    #creating a matrix-object which contains the force vector
    vector2=vector.copy()               #copying force vector
    vector2.shape=(3,1)                 #reshaping copied force vector into a column vector as opposed to a row vector
    length=dot(vector,vector2)          #calculating magnitude squared of force vector by dot multiplying it with its copy
    inversefuckyou=1/m.sqrt(length[0,0])#finding the inverse of the force vector magnitude as a float value
    vector=vector*inversefuckyou        #normalizing force vector to unit size

    rotationmatrix=(rotate(vector))     #finding rotation matrix

    x=magnetotuple[0]                   #fetching x-component of the magnetometer data
    y=magnetotuple[1]                   #fetching y-component
    z=magnetotuple[2]                   #and z-component
    magnetomatrix=umatrix.matrix([[x,y,z]]) #creating a matrix-object which contains the magnetic field vector
    
    rotatedmatrix=dot(magnetomatrix,rotationmatrix) #rotating the magnetic field vector with the rotation matrix found for gravitational force
    rotatedtuple=[rotatedmatrix[0,0],rotatedmatrix[0,1],rotatedmatrix[0,2]] #converting rotated values to a list
    
    return(rotatedtuple)                #returning rotated list

    treated = treat_yo_data(rotatedtuple)
    return(treated)

def treat_yo_data(rotated):

    rotated[0] *= 100/3
    rotated[1] *= 100/3
    rotated[2] *= 100/3

    return rotated

#a=1
#b=2
#c=3

#magnetotuple=[1,2,3]
#accelerometertuple=[a,b,c]
#testvec=(matrixise(accelerometertuple,magnetotuple))
#print(m.sqrt(1**2+2**2+3**2),m.sqrt(testvec[0]**2+testvec[1]**2+testvec[2]**2))