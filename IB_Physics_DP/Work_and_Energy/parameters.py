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
    "if speed is constant, then acceleration is zero or if speed is constant",
    "g is acceleration due to gravity"
    ]

formulas = {}
formulas[W]=F*s*cos(theta)
formulas[F]=m*a
formulas[F_cos_theta]=F*cos(theta)
formulas[s_cos_theta]=s*cos(theta)
formulas[E_p]=m*g*h
formulas[E_k]=(1/2)*m*v**2

# Question: What is the net force when acceleration is zero?
# Information: the net force is zero if the acceleration is zero
# Question: To calculate work, is the direction of force considered?
# Information: to calculate the work done, only the component of force that is in the direction of the object's displacement is considered
# Question: What is the work done when moving an object under gravitational force?
# Information: the work done is equal to the change in gravitational potential energy
# Question: What is the work done in moving an object?
# Information: the work done is equal to the change in kinetic energy
# Question: What is the total mechanical energy?
# Information: the total mechanical energy of a system/object is the sum of its kinetic and potential energy
# Question: Is the total mechanical energy conserved?
# Information: the total mechanical energy is conserved, i.e., it can neither be created nor be destroyed
# Question: When is total mechanical energy conserved?
# Information: the total mechanical energy is conserved only when the object or the system is isolated
# Question: What does it mean for an object or a system to be isolated?
# Information: a system/object is isolated when it doesn't exchange any energy with it's surroundings, i.e, it doesn't have any external forces acting on it
# Question: What is the net work done?
# Information: the net work or total work done on the system/object is equal to a change in it's energy


unknown_concepts = {}
unknown_concepts["How to find the net force?"] = [
    "the net force is zero if the acceleration is zero"
    ]
unknown_concepts["How to calculate the work done by a force?"] = [
    "to calculate the work done, only the component of force that is in the direction of the object's displacement is considered"
    ]
unknown_concepts["What is the work done against gravity?"] = [
    "the work done is equal to the change in gravitational potential energy"
    ]
unknown_concepts["What is the work done to change the velocity?"] = [
    "the work done is equal to the change in kinetic energy"
    ]
unknown_concepts["What is the conservation of total mechanical energy?"] = [
    "the total mechanical energy of a system/object is the sum of its kinetic and potential energy",
    "the total mechanical energy is conserved, i.e., it can neither be created nor be destroyed",
    "a system/object is isolated when it doesn't exchange any energy with it's surroundings, i.e, it doesn't have any external forces acting on it",
    "the net work or total work done on the system/object is equal to a change in it's total energy",
    "the total mechanical energy is conserved only when the object or the system is isolated"
    ]

information_questions = {}
information_questions["the net force is zero if the acceleration is zero"] = "What is the net force when acceleration is zero?"
information_questions["to calculate the work done, only the component of force that is in the direction of the object's displacement is considered"] = "To calculate work, is the direction of force considered?"
information_questions["the work done is equal to the change in gravitational potential energy"] = "What is the work done when moving an object under gravitational force?"
information_questions["the work done is equal to the change in kinetic energy"] = "What is the work done in moving or stopping an object?"
information_questions["the total mechanical energy of a system/object is the sum of its kinetic and potential energy"] = "What is the total mechanical energy?"
information_questions["the total mechanical energy is conserved, i.e., it can neither be created nor be destroyed"] = "Is the total mechanical energy conserved?"
information_questions["the total mechanical energy is conserved only when the object or the system is isolated"] = "When is total mechanical energy conserved?"
information_questions["a system/object is isolated when it doesn't exchange any energy with it's surroundings, i.e, it doesn't have any external forces acting on it"] = "What does it mean for an object or a system to be isolated?"
information_questions["the net work or total work done on the system/object is equal to a change in it's total energy"] = "What is the net work done?"


information_checklist_model = "gpt-4o"
information_checklist_instructions = "You are an automated checklist. I need you to carefully read my message to check if it contains some information. Your response should be a valid jsonlist called 'information_checklist' where each json object has 'information' and 'check' attributes. The 'check' attribute can only be 'Yes', 'No', or 'Wrong'. Each piece of 'information' lists the correct answer to some question. The list of 'information' is given as follows along with the questions it answers:\n"
information_checklist_prompt_post = "\nYou should check for the information in the context of the question. If my message answers the question, then the 'check' should be 'Yes'. If my message doesn't answer the question, then the check should be 'No'. And in the case where my message answers the question incorrectly, then the 'check' should be 'Wrong'."
information_checklist_prompt_pre = "Read the message to check if it contains the information to answer all the questions. Your 'check' should be based ONLY on the message given below and can only be 'Yes', 'No', or 'Wrong'.\nMessage:\n"

formula_reader_model = "gpt-4o"
formula_reader_instructions = "You are a latex formula reader. I need you to read over an array in latex and give me a formula. Your response should be a json object called 'formula'. In your response, use the following symbols:\1) force should be denoted by 'F'\n2) distance/displacement should be denoted by 's'\n3) angle should be denoted by 'theta'\n4) mass should be denoted by 'm'\n5) acceleration should be denoted by 'a'\n6) velocity should be denoted by 'v'\7) height should be denoted by 'h'\n8) acceleration due to gravity should be denoted by 'g'\n9) gravitational potential energy should be denoted by 'E_p'\n10) kinetic energy should be denoted by 'E_k'\n11) spring potential energy should be denoted by 'E_s'\n12) cosine, sine, tangent, cotangent, cosecant, and secant should be denoted by cos, sin, tan, cot, cosec, and sec respectively\nDO NOT use any other symbols in your response. Follow python syntax while writing the formula.\nIn the case that the formula I asked for is not in the array, then respond with 'Unknown'."
formula_reader_prompt_pre = "Read this array and give me a formula for:\n"
formula_reader_prompt_post = "The formula should be based ONLY on the array given below, even if it contradicts common knowledge.\nArray:\n"

print_working_json_model = "gpt-4o"
print_working_json_instructions = "You are a paraphraser. I need you to read a question and it's working and paraphrase it. Your response should be a json object which has the 'working' attribute. The 'working' will be a paraphrased version of the given working."
print_working_json_prompt_pre = "Help me paraphrase the working to the given question. If no working is given, return an empty string for working. \nQuestion: "
print_working_json_prompt_post = "\nWorking: "