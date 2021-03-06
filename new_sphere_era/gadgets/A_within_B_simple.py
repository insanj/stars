import qutip
import vpython
import math
import scipy
import numpy as np

print("usage:")
print("a/d s/w z/x for sigma X Z Y on A")
print("j/l k/i m/, for sigma X Z Y on B")

vpython.scene.width = 1000
vpython.scene.height = 600

va = vpython.sphere(pos=vpython.vector(-1.5,0,0), radius=1.0, color=vpython.color.blue, opacity=0.5)
va_star = vpython.sphere(pos=vpython.vector(0,0,0), radius=0.1, color=vpython.color.white, opacity=0.7)
vb_in_a = vpython.sphere(pos=vpython.vector(0,0,0), radius=0.2, color=vpython.color.red, opacity=0.5)

vb = vpython.sphere(pos=vpython.vector(1.5,0,0), radius=1.0, color=vpython.color.red, opacity=0.5)
vb_star = vpython.sphere(pos=vpython.vector(0,0,0), radius=0.1, color=vpython.color.white, opacity=0.7)
va_in_b = vpython.sphere(pos=vpython.vector(0,0,0), radius=0.2, color=vpython.color.blue, opacity=0.5)

dt = 0.01

a = qutip.rand_ket(2)
b = qutip.rand_ket(2)

def keyboard(event):
    global dt
    global a
    global b
    key = event.key
    operator = None
    if key == "a":   #-x for A
        operator = qutip.Qobj(scipy.linalg.expm(-2*math.pi*complex(0,1)*qutip.sigmax().full()*dt))
        a = operator.dag()*a
    elif key == "d": #+x for A
        operator = qutip.Qobj(scipy.linalg.expm(-2*math.pi*complex(0,1)*qutip.sigmax().full()*dt))
        a = operator*a
    elif key == "s": #-z for A
        operator = qutip.Qobj(scipy.linalg.expm(-2*math.pi*complex(0,1)*qutip.sigmaz().full()*dt))
        a = operator.dag()*a
    elif key == "w": #+z for A
        operator = qutip.Qobj(scipy.linalg.expm(-2*math.pi*complex(0,1)*qutip.sigmaz().full()*dt))
        a = operator*a
    elif key == "z": #-y for A
        operator = qutip.Qobj(scipy.linalg.expm(-2*math.pi*complex(0,1)*qutip.sigmay().full()*dt))
        a = operator.dag()*a
    elif key == "x": #+y for A
        operator = qutip.Qobj(scipy.linalg.expm(-2*math.pi*complex(0,1)*qutip.sigmay().full()*dt))
        a = operator*a
    elif key == "j": #-x for B
        operator = qutip.Qobj(scipy.linalg.expm(-2*math.pi*complex(0,1)*qutip.sigmax().full()*dt))
        b = operator.dag()*b
    elif key == "l": #+x for B
        operator = qutip.Qobj(scipy.linalg.expm(-2*math.pi*complex(0,1)*qutip.sigmax().full()*dt))
        b = operator*b
    elif key == "k": #-z for B
        operator = qutip.Qobj(scipy.linalg.expm(-2*math.pi*complex(0,1)*qutip.sigmaz().full()*dt))
        b = operator.dag()*b
    elif key == "i": #+z for B
        operator = qutip.Qobj(scipy.linalg.expm(-2*math.pi*complex(0,1)*qutip.sigmaz().full()*dt))
        b = operator*b
    elif key == "m": #-y for B
        operator = qutip.Qobj(scipy.linalg.expm(-2*math.pi*complex(0,1)*qutip.sigmay().full()*dt))
        b = operator.dag()*b
    elif key == ",": #+y for B
        operator = qutip.Qobj(scipy.linalg.expm(-2*math.pi*complex(0,1)*qutip.sigmay().full()*dt))
        b = operator*b

vpython.scene.bind('keydown', keyboard)

def poo(state):
    T = qutip.identity(2)
    X, Y, Z = qutip.jmat(1./2.)
    t = qutip.expect(T, state)
    x = qutip.expect(X, state)
    y = qutip.expect(Y, state)
    z = qutip.expect(Z, state)
    spin = np.array([t, x, y, z])
    magnitude = np.linalg.norm(spin)
    if magnitude != 0:
        spin = spin / magnitude
    return spin.tolist()

while True:
    vpython.rate(50)
    a_x = qutip.expect(qutip.sigmax(), a)
    a_y = qutip.expect(qutip.sigmay(), a)
    a_z = qutip.expect(qutip.sigmaz(), a)
    va_star.pos = vpython.vector(a_x-1.5, a_y, a_z)
    
    b_x = qutip.expect(qutip.sigmax(), b)
    b_y = qutip.expect(qutip.sigmay(), b)
    b_z = qutip.expect(qutip.sigmaz(), b)
    vb_star.pos = vpython.vector(b_x+1.5, b_y, b_z)
    
    a_according_to_b = b.ptrace(0)*a
    ab_x = qutip.expect(qutip.sigmax(), a_according_to_b.ptrace(0))
    ab_y = qutip.expect(qutip.sigmay(), a_according_to_b.ptrace(0))
    ab_z = qutip.expect(qutip.sigmaz(), a_according_to_b.ptrace(0))
    #ab_t, ab_x, ab_y, ab_z = poo(a_according_to_b)
    va_in_b.pos = vpython.vector(ab_x+1.5, ab_y, ab_z)
    
    b_according_to_a = a.ptrace(0)*b
    ba_x = qutip.expect(qutip.sigmax(), b_according_to_a.ptrace(0))
    ba_y = qutip.expect(qutip.sigmay(), b_according_to_a.ptrace(0))
    ba_z = qutip.expect(qutip.sigmaz(), b_according_to_a.ptrace(0))
    #ba_t, ba_x, ba_y, ba_z = poo(b_according_to_a)
    vb_in_a.pos = vpython.vector(ba_x-1.5, ba_y, ba_z)
