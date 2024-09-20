import sys
sys.path.append("/Users/likhitnayak/Ira Project/shukuchi")
from IB_Physics_DP.Work_and_Energy.utils import *
from IB_Physics_DP.Work_and_Energy.parameters import *
from sympy import *

# Function to combine value and unit into a string
def combine_value_and_unit(var):
    if var in units_dict:
        return str(values_dict[var]) + " " + units_dict[var]
    else:
        return str(values_dict[var])

## Question Parameters
question_id = 1
required_information = [
    unknown_concepts["How to find the net force?"][0],
    unknown_concepts["How to calculate the work done by a force?"][0],
]

other_force = insert_latex("300 N")
angle = insert_latex("30 \\degree") 
displacement = insert_latex("100 m")

given = {
    theta,
    s
    }
to_find = {
    F
}
objective = {
    W
}

question = "A boy pulls a box across a rough, horizontal surface using a rope. The box is moving at a steady speed. The friction on the box is {other_force} and the rope is at angle of {angle} to the horizontal. Find the work done by the boy to move the box a distance of {displacement} across the horizontal surface.".format(other_force = other_force, angle = angle, displacement = displacement)
question_image = "No"
answer_type = "single_correct"

values_dict = {}
units_dict = {}
values_dict["Friction"] = 300
units_dict["Friction"] = "N"
values_dict["F"] = 300
units_dict["F"] = "N"
values_dict["s"] = 100
units_dict["s"] = "m"
values_dict["theta"] = 30
values_dict["a"] = 0
answer_value = 30
answer_unit = " kJ"
answer_unit_into_1000 = " J"
answer_output = insert_latex('{:.2f}'.format(answer_value) + answer_unit)

question_json = {
    "question_id": question_id,
    "Question": question,
    "Question_image": question_image,
    "Answer": answer_output,
    "Answer_type": answer_type,
    "required_concepts": required_information,
}