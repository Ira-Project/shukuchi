from json import loads, dumps
from env import OPENAI_KEY
from time import sleep
from openai import OpenAI

from test_files.tests import tests
from parameters import *

client = OpenAI(
    api_key=OPENAI_KEY,
)

def get_message(steps_evaluated):
    if steps_evaluated == -1:
        message = {
            "answer": None,
            "working": "I could not understand anything from the explanation provided by you. It doesn't seem to contain any meaningful information required to solve the question.",
            "is_correct": False
            }
        message = dumps(message)
    elif steps_evaluated == 0:
        message = {
            "answer": None,
            "working": "I do not know how to begin solving the question based on your explanation. Please provide some more details.",
            "is_correct": False
            }
        message = dumps(message)
    return  message

def run_test(test_name):

    # if file is used upload a file to OpenAI
    if is_file:
        file = client.files.create(
            file=open(file_name, "rb"),
            purpose='assistants'
        )

    test = tests[test_name]
    if len(assistant_id) == 0:
        instructions = assistant_instructions_pre_question + \
            test["question"] + assistant_instructions_post_question
        assistant_instructions_post_question

        # create the assistant based on the parameters
        assistant = client.beta.assistants.create(
            name=assistant_name,
            instructions=instructions,
            tools=assistant_tools,
            model=assistant_model,
            file_ids=[file.id] if is_file else []
        )
    else:
        assistant = client.beta.assistants.retrieve(assistant_id)

    f = open(result_file_path, "w")
    question_string = "Test Question: " + test["question"] + "\n"
    f.write(question_string)
    print(question_string)
    tests_passed = 0

    # for each of the user prompts create a thread and run the assistant
    for i, user_prompt in enumerate(test["userPrompts"]):

        message_content = user_message_pre_explanation + \
            user_prompt["prompt"] + user_message_post_explanation

        thread = client.beta.threads.create(messages=[{
            "role": "user",
            "content": message_content,
        }])

        run = client.beta.threads.runs.create_and_poll(
            thread_id=thread.id,
            assistant_id=assistant.id
        )

        num_steps = 0
        steps = ""
        formulas = ""
        message = None
        run_completed = False
        # Polling the run until it is completed
        while (True):
            run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
            if run.status == 'completed':
                run_completed = True
                break
            elif run.status == 'requires_action':
                function_name = run.required_action.submit_tool_outputs.tool_calls[0].function.name
                if function_name == "evaluate_steps":
                    message_json = loads(run.required_action.submit_tool_outputs.tool_calls[0].function.arguments)
                    # print(run.required_action.submit_tool_outputs.tool_calls)
                    # print(message_json)
                    if message_json['Step stated'] == "Yes":
                        num_steps += 1
                        steps = steps + str(message_json['Step number']) + ") " + message_json['Step'] + "\n"
                        if message_json['Formula stated'] == "No":
                            formulas = formulas + str(message_json['Step number']) + ") " + "\n"
                        else:
                            if message_json['Formula stated correctly'] == "Yes":
                                formulas = formulas + str(message_json['Step number']) + ") " + message_json[
                                    'Formula'] + "\n"
                            else:
                                formulas = formulas + str(message_json['Step number']) + ") " + message_json[
                                    'Incorrect formula'] + "\n"
                        run = client.beta.threads.runs.submit_tool_outputs(
                            thread_id=thread.id,
                            run_id=run.id,
                            tool_outputs=[
                                {
                                    "tool_call_id": run.required_action.submit_tool_outputs.tool_calls[0].id,
                                    "output": """success" : "true""",
                                },
                            ])
                    else:
                        break
                else:
                    break
            sleep(5)

        if run_completed:
            message = get_message(steps_evaluated=num_steps)
        else:
            client.beta.threads.runs.cancel(run_id=run.id, thread_id=thread.id)
        print(steps)
        print(formulas)
        if not message:
            final_message_content = solver_message + "\n" + steps
            client.beta.threads.messages.create(
                thread_id=thread.id,
                role="user",
                content=final_message_content)
            run = client.beta.threads.runs.create_and_poll(
                thread_id=thread.id,
                assistant_id=assistant.id
            )
            while (True):
                if run.status == 'requires_action':
                    message = run.required_action.submit_tool_outputs.tool_calls[0].function.arguments
                    break
                sleep(5)

        title_string = "Test " + str(i) + ": " + user_prompt["prompt"] + "\n"
        print(title_string)
        f.write(title_string)
        try:
            json_message = loads(message)
        except Exception as e:
            error_string = "JSON Format Error: " + str(e) + "\n"
            print(error_string)
            f.write(error_string)

        f.write("Answer: " + str(json_message["answer"]) + "\n")
        print("Answer: " + str(json_message["answer"]))
        f.write("Working: " + str(json_message["working"]) + "\n")
        print("Working: " + str(json_message["working"]))
        f.write("Is Correct: " + str(json_message["is_correct"]) + "\n")
        print("Is Correct: " + str(json_message["is_correct"]))

        print(json_message["is_correct"] == user_prompt["expectedResult"])
        if json_message["is_correct"] == user_prompt["expectedResult"]:
            if len(user_prompt["answer"]) > 0:
                if json_message["answer"] == user_prompt["answer"]:
                    tests_passed += 1
                    f.write("Test Passed\n")
                    print("Test Passed\n")
                else:
                    failure_string = "Test Failed. Expected answer is " + \
                        user_prompt["answer"] + ".\n"
                    f.write(failure_string)
                    print(failure_string)
            else:
                tests_passed += 1
                f.write("Test Passed\n")
                print("Test Passed\n")
        else:
            failure_string = "Test Failed. Expected result is " + \
                str(user_prompt["expectedResult"]) + ".\n"
            f.write(failure_string)
            print(failure_string)

        f.write("-----------------------------------\n")
        print("-----------------------------------")

    f.write("Tests Passed: " + str(tests_passed) + "/" +
            str(len(test["userPrompts"])) + "\n")
    print("Tests Passed: " + str(tests_passed) +
          "/" + str(len(test["userPrompts"])))
    f.close()


run_test(test_name)
