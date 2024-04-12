## README

This repository is primarily used to perform tests on any AI model that we want to use as students. It contains a test document outlining test cases in various topics. It also includes a Python script `run_test.py` to run any test and output the results in a file.

Each experiment at prompt engineering is in a separate folder. The parameters of the prompts are in a parameters folder and the results of the experiment are outlined in the `results.txt` folder. Each experiment also incldues a markdown file `Description.md` that describes the purpose of the experiment and some notes on learnings.

To run the testing script you need an API key from OpenAI. Store the api key as `OPENAI_KEY=sk-...` in an `env.py` file in the top level directory.
