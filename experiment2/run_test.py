from json import loads, dumps
from env import OPENAI_KEY
from time import sleep
from openai import OpenAI

from test_files.tests import tests
from parameters import *

client = OpenAI(
    api_key=OPENAI_KEY,
)


def get_message(working, answer=None):
    is_correct = False
    if answer == "None":
        answer = None
    else:
        if answer == 1/15:
            is_correct = True
    message = {
        "answer": answer,
        "working": working,
        "is_correct": is_correct
    }
    message = dumps(message)
    return message


def run_test(test_name):

    test = tests[test_name]

    assistant = client.beta.assistants.retrieve(assistant_id)
    calculator_assistant = client.beta.assistants.retrieve(
        calculator_assistant_id)

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

        message = None
        # Polling the run until it is completed
        while (True):
            if run.status == 'completed':
                messages = client.beta.threads.messages.list(
                    thread_id=thread.id)
                message = get_message(messages.data[0].content[0].text.value)
                break
            elif run.status == 'requires_action':
                function_name = run.required_action.submit_tool_outputs.tool_calls[0].function.name
                if function_name == "compute_response":
                    response = loads(run.required_action.submit_tool_outputs.tool_calls[0].function.arguments)
                    working = response["response"]
                    # Uses another assistant to perform calculations
                    calculator_message_content = calculator_pre_message + working
                    calculator_thread = client.beta.threads.create(messages=[{
                        "role": "user",
                        "content": calculator_message_content,
                    }])
                    calculator_run = client.beta.threads.runs.create_and_poll(
                        thread_id=calculator_thread.id,
                        assistant_id=calculator_assistant.id
                    )
                    while (True):
                        if calculator_run.status == 'requires_action':
                            calculator_function_name = calculator_run.required_action.submit_tool_outputs.tool_calls[
                                0].function.name
                            if calculator_function_name == "get_answer":
                                calculator_response = loads(
                                    calculator_run.required_action.submit_tool_outputs.tool_calls[0].function.arguments)
                                answer = calculator_response["answer"]
                                break
                            else:
                                break
                        sleep(2)
                    break
                else:
                    break
            sleep(2)

        # if not run_completed:
        #     client.beta.threads.runs.cancel(run_id=run.id, thread_id=thread.id)
        if not message:
            message = get_message(working, answer)

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
