from sympy import *

F, s, theta, W = symbols("F s theta W")
m, a, v, g, h = symbols("m a v g h")
v_final, v_initial = symbols("v_final v_initial")
h_final, h_initial = symbols("h_final h_initial")
F_cos_theta = symbols("F_cos_theta")
s_cos_theta = symbols("s_cos_theta")

explanation_sample = "when the acceleration is zero the force is also zero. when calculating work done, the force should be in the direction of displacement."
formula_sample = "[W = F * s * cos(theta)]"