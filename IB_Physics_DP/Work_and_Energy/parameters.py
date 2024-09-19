from sympy import *

F, s, theta, W = symbols("F s theta W")
m, a, v = symbols("m a v")
g, h = symbols("g h")
v_final, v_initial = symbols("v_final v_initial")
h_final, h_initial = symbols("h_final h_initial")
E_p, E_k, E_s = symbols("E_p E_k E_s") 
F_cos_theta = symbols("F_cos_theta")
s_cos_theta = symbols("s_cos_theta")

explanation_sample = "the total mechanical energy is the sum of the kinetic and potential energy. the total mechanical energy is conserved, i.e., it can neither be created nor be destroyed"
formula_sample = "[W = F * s * cos(theta), E_k = 1/2 * m * v**2, E_p = m * g * h]"

known_concepts = [
    "if speed is constant, then acceleration is zero",
    "g is acceleration due to gravity"
    ]

formulas = {}
formulas[W]=F*s*cos(theta)
formulas[F]=m*a
formulas[F_cos_theta]=F*cos(theta)
formulas[s_cos_theta]=s*cos(theta)
formulas[E_p]=m*g*h
formulas[E_k]=(1/2)*m*v**2

unknown_concepts = {}
unknown_concepts["How to find the net force?"] = [
    "force is zero if the acceleration is zero"
    ]
unknown_concepts["How to calculate the work done by a force?"] = [
    "to calculate the work done by a force, we use only the force component along the object's displacement"
    ]
unknown_concepts["What is the work done against gravity?"] = [
    "work done against gravity is equal to change in gravitational potential energy"
    ]
unknown_concepts["What is the work done to change the velocity?"] = [
    "work done to change the velocity is equal to the change in kinetic energy"
    ]
unknown_concepts["What is the conservation of total mechanical enegry?"] = [
    "the total mechanical energy of a system/object is the sum of its kinetic and potential energy",
    "the total mechanical energy is conserved, i.e., it can neither be created nor be destroyed",
    "an isolated system/object is one that doesn't exchange any energy with it's surroundings, i.e, doesn't have any external forces acting on it",
    "work done by external forces on a system or an object transfers energy to or from the system or the object thus, changing it's total mechanical energy",
    "the total mechanical energy of an isolated system is conserved, i.e., it can neither be created nor be destroyed"
    ]