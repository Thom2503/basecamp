def mail_template(is_rejection, name, job, salary=None, start_date=None, feedback=None):
    """
    Functie om de template voor de email te maken. Dit kan een acceptatie brief zijn
    of een weigering zijn.

    @param bool is_rejection - of het een weigering is of niet
    @param string name       - naam van de solicitant
    @param string job        - solicitant baan
    @param string salary     - het salaris als de solicitant mag werken
    @param string start_date - de start datum als de solicitant mag werken
    @param string feedback   - als de solicitant geweigerd is kan er feedback gegeven

    @return string mail - mail wat terug gestuurd word
    """
    mail = ""
    feedback_paragraph = "" # optioneel dus moet altijd leeg zijn

    if is_rejection == True:
        # als er feedback is moet dat ook als paragraaf meegegeven worden
        if feedback != None and feedback != "":
            feedback_paragraph = f"""\nHere we would like to provide you our feedback about the interview.
{feedback}"""

        # de mail die terug gestuurd word als je geweigerd bent
        mail = f"""Dear {name}, 
After careful evaluation of your application for the position of {job}, 
at this moment we have decided to proceed with another candidate. {feedback_paragraph}
We wish you the best in finding your future desired career. Please do not hesitate to contact us with any questions. 
Sincerely, 
HR Department of XYZ"""
    else:
        mail = f"""Dear {name}, 
After careful evaluation of your application for the position of {job}, 
we are glad to offer you the job. Your salary will be {salary} euro annually. 
Your start date will be on {start_date}. Please do not hesitate to contact us with any questions. 
Sincerely, 
HR Department of XYZ"""

    return mail


def check_date(date):
    """
    Simpele functie om de datum te testen, moet in YYYY-MM-DD format zijn.
    Jaar moet tussen 2021 en 2022 zijn, maand tussen 1 en 12 en dag tussen 1 en 31.

    @param string date - datum om te checken

    @return bool - of het een correcte datum is
    """
    if "-" not in date:
        return False

    date_parts = date.split("-") # neem de delen van de datum
    # zorg dat alle datum onderdelen een int zijn
    year  = int(date_parts[0])
    month = int(date_parts[1])
    day   = int(date_parts[2])
    # check of het jaar niet tussen 2021 en 2022
    if not 2021 <= year <= 2022:
        return False
    # check of de maand niet tussen 1 en 12 is
    if not 1 <= month <= 12:
        return False
    # check of de dag niet tussen 1 en 31 is
    if not 1 <= day <= 31:
        return False

    return True


def check_salary(salary):
    """
    Functie om te checken of het salaris dat ingevoerd is correct is.

    @param string salary - salaris

    @return bool - of het klopt
    """
    # check of er niet een . en , in de salaris zitten
    if "." not in salary:
        return False
    if "," not in salary:
        return False
    # check of de salaris niet tussen 20.000,00 en 80.000,00 zit
    if not "20.000,00" <= salary <= "80.000,00":
        return False

    return True


questions = {'more' : 'More Letters?(Yes or No)',
             'rejection' : 'Job Offer or Rejection?',
             'first_name' : 'First Name?',
             'last_name' : 'Last Name?',
             'job' : 'Job title?',
             'salary' : 'Annual Salary?',
             'start_date' : 'Start Date?(YYYY-MM-DD)',
             'feedback_bool' : 'Feedback? (Yes or No)',
             'feedback' : 'Enter your Feedback (One Statement):'}
# dictionary met de antwoorden op de vragen erin
answers = {'more' : None,
           'rejection' : None,
           'first_name' : None,
           'last_name' : None,
           'job' : None,
           'salary' : None,
           'start_date' :  None,
           'feedback_bool' : None,
           'feedback' : None}

is_rejected = False
want_feedback = False

for question in questions:

    if is_rejected == True and (question == 'salary' or question == 'start_date'):
        continue
    elif is_rejected == False and (question == 'feedback_bool' or question == 'feedback'):
        continue
    elif want_feedback == False and question == 'feedback':
        continue

    answers[question] = input(f"{questions[question]} ")

    if answers['more'] != None and answers['more'] == "No":
        break
    if answers['rejection'] != None and answers['rejection'] == "Rejection":
        is_rejected = True
    if answers['feedback_bool'] != None and answers['feedback_bool'] == "Yes":
        want_feedback = True

    # een while loop om te checken of de antwoorden goed zijn, als die goed zijn kan je uit
    # deze while loop breken en dan is het een goed antwoord, anders wordt de vraag
    # herhaald tot dat er een goed antwoord wordt gegeven.
    while True:
        if question == 'more' and answers['more'] in ['Yes', 'No']:
            break
        elif question == 'rejection' and answers['rejection'] in ['Rejection', 'Job Offer']:
            break
        elif question == 'first_name' and (len(answers['first_name']) >= 2 and len(answers['first_name']) <= 10 and answers['first_name'].isalpha()):
            answers['first_name'] = answers['first_name'].capitalize()
            break
        elif question == 'last_name' and (len(answers['last_name']) >= 2 and len(answers['last_name']) <= 10):
            answers['last_name'] = answers['last_name'].capitalize()
            break
        elif question == 'job' and (len(answers['job']) >= 10 and any(c.isdigit() for c in answers['job']) == False):
            break
        elif question == 'salary' and check_salary(answers['salary']) == True:
            break
        elif question == 'start_date' and check_date(answers['start_date']) == True:
            break
        elif question == 'feedback_bool' and answers['feedback_bool'] in ['Yes', 'No']:
            break
        elif question == 'feedback' and (len(answers['feedback']) <= 128):
            break
        else:
            answers[question] = input(f"{questions[question]} ")



full_name = answers['first_name'] + " " + answers['last_name']
rejection = True if answers['rejection'] == 'Rejection' else False
print(mail_template(rejection, full_name, answers['job'], answers['salary'], answers['start_date'], answers['feedback']))
