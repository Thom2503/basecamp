import random
# de vragen als dictionary met het goede antwoord als key en de vraag als
# value hier komt een random lijstje van zodat die gesteld kunnen worden
# aan de gebruiker
QUESTIONS = {
    'tokyo': 'What is the capital of Japan?',
    'fyodor dostoevsky': 'Which writer wrote Crime and Punishment?',
    'gustav holst': 'Which componist wrote The Planets?',
    '1917': 'In what year did the Russian Revolution take place?',
    'apple': 'What company is the biggest in terms of money in the world?',
    '1991': 'In what year did the Python programming language come out?',
    'donald trump': 'Who was the 45st president of the United States?',
    '10': 'The British prime minister lives on Downing Street, but at which number?',
    'dromedaris': 'Which animal is depicted on the box of Camel sigarettes?',
    'rubble': 'What is the currency of Russia?',
    'mowgli': 'What is the name of the boy in the Jungle Book?',
    'foxtrot': 'Alpha - Bravo - Charlie - Delta - Echo - ...',
    'mali': 'In which country is Timboektoe located?',
    'gregorian': 'Which calender system do we use?',
    'isaac newton': 'On who\'s head fell an apple?',
    'william shakespeare': 'Who wrote Romeo and Juliet?',
    'github': 'Which website is owned by Microsoft and is used for version software?',
    'richard stallman': 'Who started the gnu foundation?',
    'haruki murakami': 'Who wrote Kafka on the Shore?',
    'philosopher': 'What was Plato? Plato was a ...',
    'asml': 'What Dutch company is the biggest chip manufacturer in Europe?',
    'leo tolstoy': 'Who wrote books like War and Peace and Anna Karenina?',
    '3': 'How many Japanese writers won a Nobel prize in literature?',
    'minecraft': 'The game developed by Mojang is ...',
    'spongebob squarepants': 'Who lives in a pinapple under the sea?',
}


def quiz():
    """
    Functie waar de quiz in word gedaan hier worden 10 random vragen gesteld
    en daar moet je antwoord op geven.
    """
    # kies 10 random vragen uit de QUESTIONS dictionary om te stellen aan de gebruiker
    random_questions = random.sample(QUESTIONS.keys(), 10)
    # om later te laten zien wat goed en fout
    correct_answers = {}  # lijst met de correct gegeven antwoorden en vraag
    incorrect_answers = {}  # lijst met de incorrect gegeven antwoorden en vraag
    # loop door de random vragen heen en stel die
    for answer in random_questions:
        # krijg het antwoord van de gebruiker op de random vraag
        user_answer = input(f"{QUESTIONS[answer]}\n").lower()
        # als je enter drukt moet er niks gebeuren en gaat het gewoon verder
        if len(user_answer) < 1:
            print("No answer given")
            continue
        # check of je de vraag goed hebt met de in keyword want er staan ook namen
        # als antwoord zo kan je ook bijvoorbeeld de achternaam doen. Als het goed
        # of fout is word de goede dictionary geupdatet met "antwoord": "vraag"
        if user_answer in answer:
            print("Correct")
            correct_answers.update({user_answer.capitalize(): QUESTIONS[answer]})
        else:
            print("Incorrect")
            incorrect_answers.update({user_answer.capitalize(): QUESTIONS[answer]})
    # als de correcte antwoorden niet leeg is kan je er doorheen loopen en die dan
    # uitprinten
    if len(correct_answers) > 0:
        print("\nYour correct answers:")
        for correct_answer, correct_question in correct_answers.items():
            print(f"{correct_question} = {correct_answer}")
    # het zelfde bij de correcte antwoorden
    if len(incorrect_answers) > 0:
        print("\nYour incorrect answers:")
        for incorrect_answer, incorrect_question in incorrect_answers.items():
            # zoek het originele antwoord op zodat je kan leren van je fouten
            orig_answer = dict((new_val, new_key) for new_key, new_val in QUESTIONS.items()).get(incorrect_question)
            print(f"You're answer for question '{incorrect_question}' was {incorrect_answer},")
            print(f"it should've been {orig_answer.capitalize()}")


if __name__ == "__main__":
    quiz()
