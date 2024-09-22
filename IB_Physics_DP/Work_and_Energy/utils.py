import sys
sys.path.append("/Users/likhitnayak/Ira Project/shukuchi")
from env import OPENAI_KEY
from openai import OpenAI
from IB_Physics_DP.Work_and_Energy.parameters import *
import json

client = OpenAI(
    api_key=OPENAI_KEY,
)

# Put LaTeX text within delimeters
latex_delimeter = "$!$"
def insert_latex(str):
    return latex_delimeter + str + latex_delimeter

def check_information(information_checklist, explanation, instructions_post=""):
    response = client.chat.completions.create(
        model=information_checklist_model,
        messages=[
            {"role": "system", "content": information_checklist_instructions + information_checklist + instructions_post},
            {"role": "user", "content": information_checklist_prompt_pre + explanation},
        ],
        response_format={"type": "json_object"},
        temperature=0.3
    )
    response_message = json.loads(response.choices[0].message.content)
    return response_message

def formula_reader(formula_question, formula_array):
    response = client.chat.completions.create(
        model=formula_reader_model,
        messages=[
            {"role": "system", "content": formula_reader_instructions},
            {"role": "user", "content": formula_reader_prompt_pre + formula_question + "\n" + formula_reader_prompt_post + formula_array},
        ],
        response_format={"type": "json_object"}
    )
    response_message = json.loads(response.choices[0].message.content)
    return response_message

def print_working_json(question, working):
    response = client.chat.completions.create(
        model=print_working_json_model,
        messages=[
            {"role": "system", "content": print_working_json_instructions},
            {"role": "user", "content": print_working_json_prompt_pre + question + print_working_json_prompt_post + working},
        ],
        response_format={"type": "json_object"}
    )
    response_message = json.loads(response.choices[0].message.content)
    return response_message