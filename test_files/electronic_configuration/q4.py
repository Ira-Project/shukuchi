q4 = {
    "question": "Consider an element Chlorine (atomic number 17). Which of the three atoms Oxygen (atomic number 16), Nitrogen (atomic number 7), and Fluorine (atomic number 9), is most similar to Chlorine?",
    "userPrompts": [
        {
            "prompt": "asdfasdfadsf",
            "expectedResult": False,
            "answer": ""
        },
        {
            "prompt": "Elements with similar atomic number show show similar properties. ",
            "expectedResult": False,
            "answer": "Oxygen"
        },
        {
            "prompt": "Elements with similar number of electrons in their outermost shell show similar properties. The number of electrons in an atom is equal to it's atomic number. Electronic configuration is the distribution of electrons in the shells of an atom. Each shell can hold a fixed number of electrons.",
            "expectedResult": False,
            "answer": ""
        },
        {
            "prompt": "Elements with similar number of electrons in their outermost shell show similar properties. Atoms have a tendency to have complete shells so the valency is calculated by seeing how many electrons an atom may give up or take in to complete it's shell whichever is easier. The number of electrons in an atom is equal to it's atomic number. Electronic configuration is the distribution of electrons in the shells of an atom. Each shell can hold a fixed number of electrons. The first shell holds 5 electrons and the second shell holds 7 electrons and the third shell can hold 8 electrons.",
            "expectedResult": False,
            "answer": ""
        },
        {
            "prompt": "Elements with similar number of electrons in their outermost shell show similar properties. The number of electrons in an atom is equal to it's atomic number. Electronic configuration is the distribution of electrons in the shells of an atom. Each shell can hold a fixed number of electrons. The first shell holds 2 electrons and the second shell holds 8 electrons and the third shell can hold 8 electrons.",
            "expectedResult": True,
            "answer": "Fluorine"
        },
        {
            "prompt": "Typically elements that sound similar in name are similar in properties.",
            "expectedResult": True,
            "answer": "Fluorine"  # Wrong explanation that leads to correct answer
        },
    ]
}
