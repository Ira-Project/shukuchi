from json import loads
from env import OPENAI_KEY
from time import sleep
from openai import OpenAI

from tests import tests

# To run a different experiment change the import statement
from experiment1.parameters import *

client = OpenAI(
    api_key=OPENAI_KEY,
)


def run_test(test_name):

    # if file is used upload a file to OpenAI
    if is_file:
        file = client.files.create(
            file=open(file_name, "rb"),
            purpose='assistants'
        )

    test = tests[test_name]
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

    f = open(result_file_path, "w")
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
            assistant_id=assistant.id,
            instructions=run_instructions,
        )

        # Polling the run until it is completed
        while (True):
            if run.status == 'completed':
                messages = client.beta.threads.messages.list(
                    thread_id=thread.id
                )
                message = messages.data[0].content[0].text.value
                break
            sleep(10)

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


run_test("probability")
