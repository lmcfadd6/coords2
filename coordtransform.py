
class Constants:
    def __init__(self):

        self.G = 39.478 #AU^3 yr^-2 M_sun^-1

c = Constants()

class Vector3D:

    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        self.xyz = np.array([x, y, z])

    def __add__(self, other):
        result = Vector3D(self.x + other.x, \
                          self.y + other.y, \
                          self.z + other.z)
        return result

    def __sub__(self, other):
        result = Vector3D(self.x - other.x, \
                          self.y - other.y, \
                          self.z - other.z)
        return result


    def __mul__(self, other):
        result = Vector3D(self.x * other, \
                          self.y * other, \
                          self.z * other)
        return result

    def __str__(self):
        return '[ {:.4f}, {:.4f}, {:.4f}]'.format(self.x, self.y, self.z)

    def mag(self):
        result = (self.x**2 + self.y**2 + self.z**2)**0.5


def subroutine():
    pass

if __name__ == "__main__":
    m_1 = 1
    m_2 = 1
    mu = c.G*(m_1 + m_2)

    print(mu)