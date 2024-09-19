import sys
sys.path.append("/Users/likhitnayak/Ira Project/shukuchi")
from IB_Physics_DP.utils import *
from IB_Physics_DP.Work_and_Energy.parameters import *
from sympy import *
import math

# Function to combine value and unit into a string
def combine_value_and_unit(var):
    if var in units_dict:
        return str(values_dict[var]) + " " + units_dict[var]
    else:
        return str(values_dict[var])
    
# Question Parameters
question_id = 5
required_information = [
    unknown_concepts["What is the conservation of total mechanical enegry?"][0],
    unknown_concepts["What is the conservation of total mechanical enegry?"][1],
    unknown_concepts["What is the conservation of total mechanical enegry?"][2],
    unknown_concepts["What is the conservation of total mechanical enegry?"][4],
]

mass = insert_latex("2 kg")
initial_speed = insert_latex("10 m/s")
height = insert_latex("3 m")

given = {
    m,
    v_initial,
    h
}

objective = {
    v_final
}

question = "A {mass} block is thrown from a height of {height} above the ground at a speed of {initial_speed}. What is the final speed of the block just before it hits the ground? Will the final speed be the same if we consider air resistance?".format(mass=mass, height=height, initial_speed=initial_speed)
question_image = "No"
answer_type = "multi_correct"

values_dict = {}
units_dict = {}
values_dict["m"] = 2
units_dict["m"] = "kg"
values_dict["v_initial"] = 10
units_dict["v_initial"] = "m/s"
values_dict["h"] = 3
units_dict["h"] = "m"
values_dict["g"] = 9.8
units_dict["g"] = "m/s^2"
answer_value = math.sqrt(2 * values_dict["g"] * values_dict["h"] + values_dict["v_initial"]**2)
answer_unit = " m/s"
answer_output = insert_latex('{:.2f}'.format(answer_value) + answer_unit) + ", the final speed won't be the same"

question_json = {
    "question_id": question_id,
    "Question": question,
    "Question_image": question_image,
    "Answer": answer_output,
    "Answer_type": answer_type,
    "required_concepts": required_information,
}