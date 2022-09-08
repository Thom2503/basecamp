number = int(input("Enter a number:\n"))

def even_odd(n):
    """
    Functie om te checken of n (int) een even getal is.
    @param int n - nummer

    @return bool - of het een even nummer is
    """
    return n % 2 == 0

is_even = lambda n : n % 2 == 0

print("even") if is_even(number) == True else print("odd")
