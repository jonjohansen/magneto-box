from ulinalg import *
from umatrix import *
import math as m

def rotate(vector):
    b = umatrix.matrix([[0,0,1]]) # B is a vector which points upwards!
    v = cross(vector,b)
    b.shape=(3,1)
    c=dot(vector,b)
    v_x=umatrix.matrix([[0,v[0,2],-v[0,1]],[-v[0,2],0,v[0,0]],[v[0,1],-v[0,0],0]])
    I=umatrix.matrix([[1,0,0],[0,1,0],[0,0,1]])
    R=I+v_x+dot(v_x,v_x)*(1/(c[0,0]+1))
    result=(dot(vector,R))
    if m.fabs(result[0,0])<0.00001:
        result[0,0]=0
    if m.fabs(result[0,1])<0.00001:
        result[0,1]=0
    if m.fabs(result[0,2])<0.00001:
        result[0,2]=0
    resulttest=result.copy()
    resulttest.shape=(3,1)
    return(R)

def matrixise(accelerometertuple, magnetotuple):
    a = accelerometertuple[0]
    b = accelerometertuple[1]
    c = accelerometertuple[2]
    vector = umatrix.matrix([[a,b,c]])
    vector2 = vector.copy()
    vector2.shape=(3,1)
    length = dot(vector,vector2)
    inversefuckyou = 1/m.sqrt(length[0,0])
    vector = vector*inversefuckyou
    rotationmatrix = (rotate(vector))
    x = magnetotuple[0]
    y = magnetotuple[1]
    z = magnetotuple[2]
    magnetomatrix=umatrix.matrix([[x,y,z]])
    rotatedmatrix=dot(magnetomatrix,rotationmatrix)
    rotatedtuple=[rotatedmatrix[0,0],rotatedmatrix[0,1],rotatedmatrix[0,2]]

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