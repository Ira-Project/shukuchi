q2 = {
    "question": "What period would the element with atomic number 16 be in?",
    "userPrompts": [
        {
            "prompt": "asdfasdfadsf",
            "expectedResult": False,
            "answer": ""
        },
        {
            "prompt": "We can calculate the period by determining the number of shells/ orbits in the atom.",
            "expectedResult": False,
            "answer": ""
        },
        {
            "prompt": "We can calculate the period by determining the number of shells/ orbits in the atom. The number of electrons in an atom is equal to it's atomic number. Electronic configuration is the distribution of electrons in the shells of an atom. Each shell can hold a fixed number of electrons",
            "expectedResult": False,
            "answer": "5"  # Can be any number not 3
        },
        {
            "prompt": "We can calculate the period by determining the number of shells/ orbits in the atom. The number of electrons in an atom is equal to it's atomic number. Electronic configuration is equal to the number of electrons. Each shell can hold a fixed number of electrons. The first shell holds 5 electrons and the second shell holds 7 electrons.",
            "expectedResult": True,
            # This is an incorrect explanation that leads to a correct answer for this question.
            "answer": "3"
        },
        {
            "prompt": "We can calculate the period by determining the number of shells/ orbits in the atom. The number of electrons in an atom is equal to it's atomic number. Electronic configuration is equal to the number of electrons. Each shell can hold a fixed number of electrons. The first shell holds 5 electrons and the second shell holds 10 electrons.",
            "expectedResult": False,
            "answer": "2"
        },
        {
            "prompt": "We can calculate the period by determining the number of shells/ orbits in the atom. The number of electrons in an atom is equal to it's atomic number. Electronic configuration is equal to the number of electrons. Each shell can hold a fixed number of electrons. The first shell holds 2 electrons and the second shell holds 8 electrons and the third shell can hold up to 18 electrons.",
            "expectedResult": True,
            "answer": "3"
        },
    ]
}
