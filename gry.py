#-*- coding: windows-1250 -*-
# Gry
# Demonstruje tworzenie modu�u

class Player(object):
    """ Uczestnik gry. """
    def __init__(self, name, score = 0):
        self.name = name
        self.score = score

    def __str__(self):
        rep = self.name + ":\t" + str(self.score)
        return rep

def ask_yes_no(question):
    """Zadaj pytanie, na kt�re mo�na odpowiedzie� tak lub nie."""
    response = None
    while response not in ("t", "n"):
        response = input(question).lower()
    return response

def ask_number(question, low, high):
    """Popro� o podanie liczby z okre�lonego zakresu."""
    response = None
    while response not in range(low, high):
        response = int(input(question))
    return response

  
if __name__ == "__main__":
    print("Uruchomi�e� ten modu� bezpo�rednio (zamiast go zaimportowa�).")
    input("\n\nAby zako�czy� program, naci�nij klawisz Enter.")


