q1 = {
    "question": "What is the electronic configuration of Chlorine with the atomic number 17?",
    "userPrompts": [
        {
            "prompt": "asdfasdfadsf",
            "expectedResult": False,
            "answer": ""
        },
        {
            "prompt": "Electronic configuration refers to the number of electrons in each shell of an atom. The number of electrons in an atom is equal to it's atomic number.",
            "expectedResult": False,
            "answer": "17"
        },
        {
            "prompt": "The number of electrons in an atom is equal to it's atomic number. Electronic configuration is the distribution of electrons in the shells of an atom. Each shell can hold a fixed number of electrons",
            "expectedResult": False,
            "answer": "10, 7"  # This maybe any combination that adds to 17
        },
        {
            "prompt": "The number of electrons in an atom is equal to it's atomic number. Electronic configuration is equal to the number of electrons. Each shell can hold a fixed number of electrons. The first shell holds 5 electrons and the second shell holds 7 electrons.",
            "expectedResult": False,
            "answer": "5, 7, 5"
        },
        {
            "prompt": "The number of electrons in an atom is equal to it's atomic number. Electronic configuration is equal to the number of electrons. Each shell can hold a fixed number of electrons. The first shell holds 2 electrons and the second shell holds 8 electrons and the third shell can hold up to 18 electrons.",
            "expectedResult": True,
            "answer": "2, 8, 7"
        },
    ]
}
