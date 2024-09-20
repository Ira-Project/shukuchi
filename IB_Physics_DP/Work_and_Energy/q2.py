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
question_id = 2
required_information = [
    unknown_concepts["What is the work done against gravity?"][0]
]

mass = insert_latex("10 kg")
initial_height = insert_latex("1 m") 
final_height = insert_latex("3 m")

given = {
    mass,
    initial_height,
    final_height
    }
objective = {
    W
}

question = "A {mass} dumbell is initially kept on a rack of height {initial_height}. It is then lifted to a height of {final_height}. Calculate the work done in lifting the dumbell.".format(mass=mass, initial_height=initial_height, final_height=final_height)
question_image = "No"
answer_type = "single_correct"

values_dict = {}
units_dict = {}
values_dict["m"] = 10
units_dict["m"] = "kg"
values_dict["h1"] = 1
units_dict["h1"] = "m"
values_dict["g"] = 9.8
units_dict["g"] = "m/s^2"
values_dict["h2"] = 3
units_dict["h2"] = "m"
answer_value = 196
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