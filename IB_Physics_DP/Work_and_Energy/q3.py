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
question_id = 3
required_information = [
    unknown_concepts["What is the work done to change the velocity?"][0]
]

mass = insert_latex("200 g")
initial_velocity = insert_latex("20 m/s")
final_velocity = insert_latex("0 m/s")

given = {
    mass,
    initial_velocity,
    final_velocity
    }

objective = {
    W
}

question = "A {mass} football is kicked along the field at an initial speed of {initial_velocity}. What is the work done by friction to bring the football to a stop?".format(mass=mass, initial_velocity=initial_velocity)
question_image = "No"
answer_type = "single_correct"

values_dict = {}
units_dict = {}
values_dict["m"] = 0.2
units_dict["m"] = "kg"
values_dict["v_initial"] = 20
units_dict["v_initial"] = "m/s"
values_dict["v_final"] = 0
units_dict["v_final"] = "m/s"
answer_value = 40
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