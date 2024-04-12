q3 = {
    "question": "What is the valency of an element with atomic number 17?",
    "userPrompts": [
        {
            "prompt": "asdfasdfadsf",
            "expectedResult": False,
            "answer": ""
        },
        {
            "prompt": "We can calculate valency by determining how many electrons are in the outermost shell of an atom. The number of electrons in an atom is equal to it's atomic number.",
            "expectedResult": False,
            "answer": ""
        },
        {
            "prompt": "We can calculate valency by determining how many electrons are in the outermost shell of an atom. The number of electrons in an atom is equal to it's atomic number. Electronic configuration is the distribution of electrons in the shells of an atom. Each shell can hold a fixed number of electrons",
            "expectedResult": False,
            "answer": ""
        },
        {
            "prompt": "We can calculate valency by determining how many electrons are in the outermost shell of an atom. Atoms have a tendency to have complete shells so the valency is calculated by seeing how many electrons an atom may give up or take in to complete it's shell whichever is easier. The number of electrons in an atom is equal to it's atomic number. Electronic configuration is the distribution of electrons in the shells of an atom. Each shell can hold a fixed number of electrons. The first shell holds 5 electrons and the second shell holds 7 electrons and the third shell can hold 8 electrons.",
            "expectedResult": False,
            "answer": "2"
        },
        {
            "prompt": "We can calculate valency by determining how many electrons are in the outermost shell of an atom. Atoms have a tendency to have complete shells so the valency is calculated by seeing how many electrons an atom may give up or take in to complete it's shell whichever is easier. The number of electrons in an atom is equal to it's atomic number. Electronic configuration is the distribution of electrons in the shells of an atom. Each shell can hold a fixed number of electrons. The first shell holds 2 electrons and the second shell holds 8 electrons and the third shell can hold 8 electrons.",
            "expectedResult": True,
            "answer": "1"
        },
        {
            "prompt": "We can calculate valency by determining how many electrons are in the outermost shell of an atom. Atoms have a tendency to have complete orbitals and stable configurations. Valency is calculated by seeing how many electrons an atom may give up or take in to reach a stable state. The number of electrons in an atom is equal to it's atomic number. Electronic configuration is the distribution of electrons in the shells of an atom. Each shell can hold a fixed number of electrons. The first shell holds 2 electrons and the second shell holds 8 electrons and the third shell can hold 8 electrons.",
            "expectedResult": True,
            # The 18 electrons in third shell is technically not incorrect and refers to a more complex understanding.
            "answer": "1"
        },
    ]
}
