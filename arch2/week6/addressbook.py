'''
Create an application that manages contacts in an addressbook.
The following requirements should be implemented:
- Add a contact with first name and last name (only alphabet), multiple (unique)
  e-mails (containing at least one '@'), multiple (unique) phone numbers (only digits).
  Also, an ID should be generated which should be 1 higher than the highest current ID.
- Remove a contact by ID.
- List all contacts with the option to sort by first_name or last_name (default first_name)
  with a sort_by parameter and in ascending (ASC) or decending (DESC) direction (default ASC)
  witb a direction parameter.
- Merge duplicate contacts (automatically). Contacts with the exact same full name
  (first and last name combined) should be merged. The e-mails and phone numbers of
  the duplicate contacts should be added to the the first duplicate contact
  (contact with the highest ID). The other duplicate contcts should be deleted from the addressbook
- Contacts are read from the provided JSON file and should be updated with new or removed contacts.
'''

import os
import sys
import json

addressbook = []


def find_contact(first_name="", last_name="", find_last=True):
    """
    Om een contact te vinden op basis van de voor en achternaam
    of je kan alleen de laatste zoeken.

    @param string first_name - optioneel voornaam
    @param string last_name  - optioneel achternaam
    @param bool   find_last  - of je alleen de laatste wilt zoeken

    @return tuple (id, must_merge) - het id (bij laatste) en of je moet mergen
    """
    id = 0
    # variable om te weten of de contact gemerged moet worden
    must_merge = False
    # als het allemaal leeg is hoeft het niet gemerged worden
    if first_name == "" and last_name == "":
        must_merge = False
    # loop door de contacten heen en als de first en last name
    # van de parameters overeenkomen met die van de contact
    # dan moet je mergen
    for contact in addressbook:
        if first_name == contact['first_name'] and last_name == contact['last_name']:
            # verander de id naar degene die je moet hebben
            id = contact['id']
            # nu weet je zeker dat het gemerged moet worden
            must_merge = True
            # en je moet niet de laatste hebben
            find_last = False
            # breek uit de loop want we hoeven niet meer te
            # zoeken
            break
        else:
            find_last = True
    # als je de laatste id moet zoeken dit is bedoeld
    # om te gebruiken om de id met 1 te incrementen
    if find_last is True:
        id = max([contact['id'] for contact in addressbook])
    # return de tuple met de twee belangrijke data
    return (int(id), must_merge)


'''
print all contacts in the following format:
======================================
Position: <position>
First name: <firstname>
Last name: <lastname>
Emails: <email_1>, <email_2>
Phone numbers: <number_1>, <number_2>
'''


def display(list=[]):
    # loop door de lijst en print die met een f string
    # mooi en duidelijk
    for contact in list:
        # maak een lijstje met comma's voor de emails
        # en nummers anders zie je een python list
        emails = ", ".join(contact['emails'])
        numbers = ", ".join(contact['phone_numbers'])

        print_format = f"""Position: {contact['id']}
First name: {contact['first_name']}
Last name: {contact['last_name']}
Emails: {emails}
Phone numbers: {numbers}"""
        print(print_format)


'''
return list of contacts sorted by first_name or last_name [if blank then unsorted],
direction [ASC (default)/DESC])
'''


def list_contacts(first_or_last="first", direction="asc"):
    global addressbook
    # boolean voor in de sorted function om de directie aan te
    # kunnen geven
    reversed = True if direction.lower() == "desc" else False
    # als het leeg is dan moet je de adressbook returnen
    if first_or_last.lower() == "":
        return addressbook
    # er zijn twee dingen waar op gesorteerd kan worden en dat
    # is first of last name en die wilt de sorted functie als key
    what_key = "first_name" if first_or_last.lower() == "first" else "last_name"
    # sorteer de lijst
    addressbook = sorted(addressbook, key=lambda k: k[what_key], reverse=reversed)

    return addressbook


'''
add new contact:
- first_name
- last_name
- emails = {}
- phone_numbers = {}
'''


def add_contact(first_name, last_name, emails, numbers):
    # om bij te houden of het een goed contact is
    valid_contact = True
    # om een lijstje met incorrecte data aan de gebruiker
    # te tonen
    invalid_data = []
    # check alle verschillende data of het niet klopt als
    # het niet klopt wordt is het geen goede contact
    # en krijg je errors te zien.
    if first_name == "" or first_name.isalpha() is not True:
        valid_contact = False
        invalid_data.append("First name is empty or has numbers")
    if last_name == "" or last_name.isalpha() is not True:
        valid_contact = False
        invalid_data.append("Last name is empty or has numbers")
    if emails == 0:
        valid_contact = False
        invalid_data.append("Email is empty")
    else:
        # er kunnen meerdere emails ingevuld worden
        # dus loop door die om te checken of ze
        # kloppen
        for email in emails:
            if email == "" or "@" not in email:
                valid_contact = False
                invalid_data.append("Email is empty or no '@' found")
    if numbers == 0:
        valid_contact = False
        invalid_data.append("No numbers")
    else:
        for number in numbers:
            if number == "" or number.isnumeric() is not True:
                valid_contact = False
                invalid_data.append("No number or is not numeric")
    # als het een goed contact is mag je door gaan
    if valid_contact is True:
        # zoek naar de laatste id van alle contacten
        # dit is zodat elk id met 1 wordt geincrement
        found_contact = find_contact(find_last=False)
        found_id = found_contact[0]
        # maak de data van de contact in een dictionary
        data = {}
        data['id'] = found_id + 1
        data['first_name'] = first_name
        data['last_name'] = last_name
        data['emails'] = emails
        data['phone_numbers'] = numbers
        # voeg deze nieuwe data dictionary aan de addressbook
        # toe
        addressbook.append(data)
    else:
        # maak de errors in een lijstje en print die dan
        errors = "\n".join(invalid_data)
        print(errors)


'''
remove contact by ID (integer)
'''


def remove_contact(id):
    # loop door de addressbook heen met de index
    # want die heb je nodig om de item uit de lijst
    # te kunnen verwijderen
    for idx, contact in enumerate(addressbook):
        if contact['id'] == id:
            addressbook.pop(idx)


'''
merge duplicates (automated > same fullname [firstname & lastname])
'''


def merge_contacts():
    # lists met alle data dat nodig is
    # voor het mergen van de contacten
    found_ids = []
    duplicate_emails = {}
    duplicate_numbers = {}
    for contact in addressbook:
        contact_id = contact['id']
        # zoek de contact met de voor en achternaam
        # dit id komt dan in een dictionary met de emails/nummers als value
        # hier wordt dan doorheen geloopt en aan de goede contact toegevoegd
        found_contact = find_contact(contact['first_name'], contact['last_name'])
        found_id = found_contact[0]
        must_merge = found_contact[1]
        if must_merge is True:
            # stop alle data in de nodige lists om te gebruiken
            # bij de merge
            found_ids.append({contact_id: found_id})
            duplicate_emails.update({contact_id: contact['emails']})
            duplicate_numbers.update({contact_id: contact['phone_numbers']})
    # ids die gemerged moeten gaan worden
    ids_to_merge = {}
    # om alle niet duplicates uit de lijst
    # te halen en in de ids_to_merge dict
    # doen want dat zijn degene die gemerged moeten worden
    for idx, id in enumerate(found_ids):
        key = list(id.keys())[0]
        val = list(id.values())[0]
        # als de key en de val niet gelijk zijn
        # is het een id die gemerged moet worden
        if key != val:
            ids_to_merge.update({key: val})
    # loop door de ids heen die gemerged moeten worden
    # die lopen dan weer door de emails en nummers toe
    # die dan worden toegevoegd aan de goede contact
    if len(ids_to_merge) > 0:
        for c_id, merge_id in ids_to_merge.items():
            for email in duplicate_emails[c_id]:
                addressbook[merge_id - 1]['emails'].append(email)
            for number in duplicate_numbers[c_id]:
                addressbook[merge_id - 1]['phone_numbers'].append(number)
            # verwijder de contact uit de lijst want die is nu gemerged
            remove_contact(c_id)


'''
read_from_json
Do NOT change this function
'''


def read_from_json(filename):
    # read file
    with open(os.path.join(sys.path[0], filename)) as outfile:
        data = json.load(outfile)
        # iterate over each line in data and call the add function
        for contact in data:
            addressbook.append(contact)


'''
write_to_json
Do NOT change this function
'''


def write_to_json(filename):
    json_object = json.dumps(addressbook, indent=4)

    with open(os.path.join(sys.path[0], filename), "w") as outfile:
        outfile.write(json_object)


'''
main function:
# build menu structure as following
# the input can be case-insensitive (so E and e are valid inputs)
# [L] List contacts
# [A] Add contact
# [R] Remove contact
# [M] Merge contacts
# [Q] Quit program
Don't forget to put the contacts.json file in the same location as this file!
'''


def main(json_file):
    read_from_json(json_file)
    # de vragen voor het toevoegen van een contact
    add_questions = (
        'First name? ',
        'Last name? ',
        'Email? (seperate with comma\'s) ',
        'Phone number? (seperate with comma\'s) '
    )
    # print het menu uit
    print("""[L] List contacts
[A] Add contact
[R] Remove contact
[M] Merge contacts
[Q] Quit program""")
    quit_program = False
    while quit_program is False:
        command = input("> ").lower()
        if command in ('l', 'list'):
            # vraag voor de verschillende opties
            # what_input = input("First or last name sorting? (leave empty for none)\n")
            # asc_or_desc = input("Ascending order or descending? (leave empty for default)\n")
            # toon de lijst met de list_contact functie return
            # als de lijst die getoont wordt
            # ^ hoeft blijkbaar niet
            what_input = "first"
            asc_or_desc = "asc"
            display(list_contacts(what_input, asc_or_desc))
        elif command in ('a', 'add'):
            answers = []  # lijst met alle data voor een contact
            question = 0  # op welke vraag die nu is
            while question < len(add_questions):
                answer = input(add_questions[question])
                answers.append(answer)
                question += 1
            # stop alle data in variables voor duidelijkheid
            # bij emails en numbers moet je een lijstje maken
            # want dat is wat add_contacts begrijpt
            first_name = answers[0].capitalize()
            last_name = answers[1].capitalize()
            # maak een lijstje van de emails en nummers want
            # dat wilt de json hebben als data
            emails = answers[2].split(",")
            numbers = answers[3].split(",")
            add_contact(first_name, last_name, emails, numbers)
        elif command in ('r', 'remove'):
            # vraag voor de id om te verwijderen
            id_to_remove = int(input("Give the id of the contact to remove:\n"))
            if id_to_remove > 0:
                remove_contact(id_to_remove)
        elif command in ('m', 'merge'):
            # merge de contacts automatisch die kunnen mergen
            merge_contacts()
        elif command in ('q', 'quit'):
            # bij het sluiten wordt de json opgeslagen
            write_to_json('contacts.json')
            quit_program = True


'''
calling main function:
Do NOT change it.
'''
if __name__ == "__main__":
    main('contacts.json')
