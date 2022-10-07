def next_verse(number):
    """
    Functie de de zin van twelve days of christmas met number als welke dag
    @param int number - welke dag van de tekst

    @return string - welke zin het is
    """
    # correcte nummer om bij te beginnen en in de tuples te kunnen zoeken
    correct_number = number - 1
    # welke kadootjes gegeven moeten worden
    gifts = (
        'A partridge in a pear tree',
        'Two turtle doves And ',
        'Three french hens, ',
        'Four calling birds, ',
        'Five gold rings (Five golden rings), ',
        'Six geese a-laying, ',
        'Seven swans a-swimming, ',
        'Eight maids a-milking, ',
        'Nine ladies dancing, ',
        'Ten lords a-leaping, ',
        'Eleven pipers piping, ',
        'Twelve drummers drumming, '
    )
    # om de kadootjes naast elkaar te krijgen voor in de tekst
    gifts_given = ""
    # als het nummer 1 is moet de for loop optellen als het niet
    # 1 is moet het aftellen want het moet voor elkaar geprint worden van
    # groot naar klein
    if number == 1:
        start = 0
        end = number
        steps = 1
        day = f"{number}st"  # als het het eerste dag is moet het 1st zijn
    else:
        start = correct_number
        end = -1
        steps = -1
        day = f"{number}nd"  # bij de andere dagen moet er nd achter staan zoals 2nd
    for i in range(start, end, steps):
        gifts_given += gifts[i]

    return f"On the {day} day of christmas, my true love sent to me {gifts_given}"


if __name__ == "__main__":
    # loop van dag 1 tot 13 want 12 moet volledig afgemaakt worden
    for d in range(1, 13):
        print(next_verse(d))
