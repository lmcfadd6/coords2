
class Constants:
    """ An object defining constants
    """ 

    def __init__(self):

        # Gravitational Constant
        self.G = 39.478 #AU^3 yr^-2 M_sun^-1

        # Astronomical Unit in meters
        self.AU = 1.496e+11 # m

        # Seconds in a year
        self.yr = 31557600 #s

        # Solar mass in kg
        self.M_sun = 1.989e30 #kg



class Vector3D:
    """ Basic function defining 3D cartesian vectors in [x, y, z] form

        Example:
            u = Vector3D(0, 1, 2)
            v = Vector3D(1, 1, 1)
            u is a vector [0, 1, 2]
            v is a vector [1, 1, 1]

    """

    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        self.xyz = [x, y, z]

    def __add__(self, other):
        """ Adds two vectors as expected
        Example:
            w = u + v
            w is a vector [1, 2, 2]
        
        """
        result = Vector3D(self.x + other.x, \
                          self.y + other.y, \
                          self.z + other.z)
        return result

    def __sub__(self, other):
        """ Subtracts two vectors as expected
        Example:
            w = u - v
            w is a vector [-1, 0, 1]
        """
        result = Vector3D(self.x - other.x, \
                          self.y - other.y, \
                          self.z - other.z)
        return result


    def __mul__(self, other):
        """ Multipies a vector by a constant
        Example:
            w = u*3
            w is a vector [0, 3, 6]
        """
        result = Vector3D(self.x * other, \
                          self.y * other, \
                          self.z * other)
        return result

    def __str__(self):
        return '[ {:.4f}, {:.4f}, {:.4f}]'.format(self.x, self.y, self.z)

    def mag(self):
        """ Returns the geometric magnitude of the vector
        """
        result = (self.x**2 + self.y**2 + self.z**2)**0.5
        return result

    def dot(self, other):
        """ Returns the dot product of the vectors
        Example:
            w = u.dot(v)
            w = 3
        """ 
        result = self.x*other.x + self.y*other.y + self.z*other.z

        return result

    def cross(self, other):
        """ Returns the cross product of the vectors
        Example:
            w = u.cross(v)
            w is a vector [-1, 2, -1]
        """

        x = self.y*other.z - self.z*other.y
        y = self.z*other.x - self.x*other.z
        z = self.x*other.y - self.y*other.x

        result = Vector3D(x, y, z)
        return result

################
# CODE START
################

### Imports
import numpy as np

### define constants
c = Constants()

def orbitalElements(mu, r, v):
    """ Transforms a rotating body state vectors into Keplarian Orbital parameters
    All units are given in AU, yrs, Solar Masses, and degrees
    Inputs:
        mu [float] - Standard gravatational parameter in AU^3 yr^-2
        r [Vector3D] - [x, y, z] state position vector of the orbiting body in AU
        v [Vector3D] - [v_x, v_y, v_z] state velocity vector of the orbiting body in AU/yr

    Outputs:
        a [float] - Semimajor Axis of orbiting body [AU]
        e [float] - Eccentricity of orbit
        i [float] - Inclination of orbit [deg]
        o [float] - Longitude of Accending node [deg]
        w [float] - Argument of Periapsis [deg]
        f [float] - True Anomaly [deg]
    """

    # Catch bad inputs:

    # no mass -> no orbiting!
    if mu == 0:
        print("[ERROR] Standard Gravitational Mass cannot be 0!")
        return None, None, None, None, None, None

    if r.mag() == 0:
        print("[ERROR] r can not be a zero vector!")
        return None, None, None, None, None, None
    
    if 2/r.mag() <= v.mag()**2/mu:
        print("[ERROR] Orbit is no longer elliptical")
        return None, None, None, None, None, None
        
    # angular momentum per unit mass
    h = r.cross(v)

    # Calculate a, e, i
    #######################
    a = 1/(2/r.mag() - v.mag()**2/mu)
    e = np.sqrt(1 - h.mag()**2/mu/a)
    i = np.arctan2(np.sqrt(h.x**2 + h.y**2), h.z)

    print("[a] = {:.4f} AU".format(a))
    print("[e] = {:.4f}".format(e))
    print("[i] = {:.4f}°".format(np.degrees(i)%360))
    #######################

    # Case 1: Inclination is 0
    if i == 0:
        # o doesn't make any sense, since it doesn't go above the plane
        o = None
        print("[\u03A9] is undefined")
    else:
        o = np.arctan2(h.x, -h.y)
        print("[\u03A9] = {:.2f}°".format(np.degrees(o)%360))

    # Case 2: Eccentricity is 0
    if e == 0:
        # w doesn't make sense if there is no closest point
        print("[WARNING] e is exactly 0!")
        f = None
        w = None
        print("[f] is undefined")
        print("[\u03C9] is undefined")
        
    else:
        f = np.arctan2(r.dot(v)*h.mag(), h.mag()**2 - mu*r.mag())
        print("[f] = {:.4f}°".format(np.degrees(f)%360))

        # Case 3: Inclinaion is 0, but f is calculated first
        if i == 0:
            w = None
            print("[\u03C9] is undefined")
        else:
            w = np.arctan2(r.z*h.mag()/np.sqrt(h.x**2 + h.y**2), r.x*np.cos(o) + r.y*np.sin(o)) - f
            print("[\u03C9] = {:.4f}°".format(np.degrees(w)%360))
        

    # Returns
    return a, e, i, o, f, w

if __name__ == "__main__":

    # units = AU, yr, Solar mass

    print("==========================================================")
    print("Test 1")
    print("Earth's orbit given r and v at furthest point from the sun")
    print("i = 0")
    print("==========================================================")

    #Calculate standard gravitational parameter
    m_1 = 1
    m_2 = 3.00273e-6
    mu = c.G*(m_1 + m_2)

    # Earth's orbit
    a_0 = 149.596e9/c.AU
    e_0 = 0.0167
    b_0 = a_0*np.sqrt(1 - e_0**2)

    r = Vector3D(np.sqrt(a_0**2 - b_0**2) + a_0, 0, 0)
    v = Vector3D(0, np.sqrt(mu*(2/r.mag() - 1/a_0)), 0)

    a, e, i, o, f, w = orbitalElements(mu, r, v)


    print("==========================================================")
    print("Test 2")
    print("Earth's orbit given r and v at closest point from the sun")
    print("i is slightly above 0")
    print("==========================================================")
    m_1 = 1
    m_2 = 3.00273e-6
    mu = c.G*(m_1 + m_2)

    # Earth's orbit
    a_0 = 149.596e9/c.AU
    e_0 = 0.0167
    b_0 = a_0*np.sqrt(1 - e_0**2)

    r = Vector3D(np.sqrt(a_0**2 - b_0**2) - a_0, 0, 1/c.AU)
    v = Vector3D(0, -np.sqrt(mu*(2/r.mag() - 1/a_0)), 0)

    a, e, i, o, f, w = orbitalElements(mu, r, v)
    

    print("==========================================================")
    print("Test 3")
    print("Test with similar matlab program test code")
    print("Similar program used MKS, values should be as expected")
    #https://www.mathworks.com/matlabcentral/fileexchange/35455-convert-keplerian-orbital-elements-to-a-state-vector
    print("==========================================================")
    

    mu = 3.986e+14
    r = Vector3D(6524.834, 6862.875, 6448.296)
    v = Vector3D(4.901327, 5.533756,-1.976341)

    a, e, i, o, f, w = orbitalElements(mu, r, v)
    print("Expected:")
    print("[a] = {:.4f} AU".format(5.728285815095142e+03))
    print("[e] = {:.4f}".format(0.999999999033934))
    print("[i] = {:.4f}°".format(np.degrees(1.533605562639449)))
    print("[\u03A9] = {:.2f}°".format(np.degrees(3.977575002801695)))
    print("[f] = {:.4f}°".format(np.degrees(3.141592653589793)))
    print("[\u03C9] = {:.4f}°".format(np.degrees(5.684887965507214)))
    