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

    # for each of the user prompts create a thread and run the assistant
    for user_prompt in test["userPrompts"]:

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

        f = open("results.txt", "w")
        tests_passed = 0
        f.write("1. " + user_prompt["prompt"] + "\n")
        try:
            message = """{"answer": "0", "working": "I'm unable to calculate probability since you have not explained how to do so.", "is_correct": ""}"""
            json_message = loads(message)
            f.write("Answer: " + json_message["answer"] + "\n")
            f.write("Working: " + json_message["working"] + "\n")
            f.write("Is Correct: " + str(json_message["is_correct"]) + "\n")
            if json_message["is_correct"] == user_prompt["expectedResult"]:
                if user_prompt["answer"].length > 0:
                    if json_message["answer"] == user_prompt["answer"]:
                        tests_passed += 1
                else:
                    tests_passed += 1

        except Exception as e:
            f.write("JSON Format Error", e)

        f.write("-----------------------------------\n")

    f.write("Tests Passed: " + str(tests_passed) + "/" +
            str(len(test["userPrompts"])) + "\n")
    f.close()


run_test("probability")
