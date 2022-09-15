# vragen voor benodigheden
benodigheden = ["is het huis Duurzaam?",
                "Zijn er Zonnepanelen?",
                "Is er een tuin van 20m2?",
                "Is het niet duurder dan 1 miljoen?"]
benodigheden_aanwezig = [] # de antwoorden bij elke vraag

print("Geef ja/nee als antwoord op de vragen")
for vraag in benodigheden:
    antwoord = input(f"{vraag}\n")
    if antwoord == "ja":
        benodigheden_aanwezig.append(True)
    else:
        benodigheden_aanwezig.append(False)

if all(i for i in benodigheden_aanwezig):
    print("Je kan het huis bouwen")
else:
    print("Je kan het huis niet bouwen")
