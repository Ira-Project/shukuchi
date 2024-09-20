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
question_id = 4
required_information = [
    unknown_concepts["What is the work done to change the velocity?"][0],
    unknown_concepts["What is the conservation of total mechanical enegry?"][0],
    unknown_concepts["What is the conservation of total mechanical enegry?"][1],
    unknown_concepts["What is the conservation of total mechanical enegry?"][2],
    unknown_concepts["What is the conservation of total mechanical enegry?"][3],
    unknown_concepts["What is the conservation of total mechanical enegry?"][4],
]

work_done = insert_latex("100 J")
distance = insert_latex("d")
new_distance = insert_latex("2d")

given = {
    W,
    s
}

objective = {
    W
}

question = "The work done in dragging a box for distance {distance} across a rough horizontal surface is {work_done}. Assuming that the speed of the box is constant, what is the work done in dragged the box for a distance of {new_distance}?".format(distance=distance, work_done=work_done, new_distance=new_distance)
question_image = "No"
answer_type = "single_correct"

values_dict = {}
units_dict = {}
values_dict["W"] = 100
units_dict["W"] = "J"
values_dict["s_old"] = symbols("d")
values_dict["s_new"] = 2 * values_dict["s_old"]
values_dict["v1"] = symbols("v1")
values_dict["v2"] = values_dict["v1"]
answer_value = 200
answer_unit = " J"
answer_output = insert_latex('{:.2f}'.format(answer_value) + answer_unit)

question_json = {
    "question_id": question_id,
    "Question": question,
    "Question_image": question_image,
    "Answer": answer_output,
    "Answer_type": answer_type,
    "required_concepts": required_information,
}