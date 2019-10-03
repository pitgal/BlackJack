#-*- coding: windows-1250 -*-
# Blackjack.  Od 1 do 7 graczy wsp�zawodniczy z rozdaj�cym
import karty, gry


class BJ_Card(karty.Card):
    """ Karta do blackjacka. """
    ACE_VALUE = 1

    @property
    def value(self):
        if self.is_face_up:
            v = BJ_Card.RANKS.index(self.rank) + 1
            if v > 10:
                v = 10
        else:
            v = None
        return v


class BJ_Deck(karty.Deck):
    """ Talia kart do blackjacka. """

    def populate(self):
        for suit in BJ_Card.SUITS:
            for rank in BJ_Card.RANKS:
                self.cards.append(BJ_Card(rank, suit))


class BJ_Hand(karty.Hand):
    """ R�ka w blackjacku. """

    def __init__(self, name):
        super(BJ_Hand, self).__init__()
        self.name = name

    def __str__(self):
        rep = self.name + ":\t" + super(BJ_Hand, self).__str__()
        if self.total:
            rep += "(" + str(self.total) + ")"
        return rep

    @property
    def total(self):
        # je�li karta w r�ce ma warto�� None, to i warto�� sumy wynosi None
        for card in self.cards:
            if not card.value:
                return None

        # zsumuj warto�ci kart, traktuj ka�dego asa jako 1
        t = 0
        for card in self.cards:
            t += card.value

        # ustal, czy r�ka zawiera asa
        contains_ace = False
        for card in self.cards:
            if card.value == BJ_Card.ACE_VALUE:
                contains_ace = True

        # je�li r�ka zawiera asa, a suma jest wystarczaj�co niska,
        # potraktuj asa jako 11
        if contains_ace and t <= 11:
            # dodaj tylko 10, poniewa� ju� dodali�my 1 za asa
            t += 10

        return t

    def is_busted(self):
        return self.total > 21

    def is_21(self):
        return self.total == 21        


class BJ_Player(BJ_Hand):
    """ Gracz w blackjacku. """

    def is_hitting(self):
        response = gry.ask_yes_no("\n" + self.name + ", chcesz dobra� kart�? (T/N): ")
        return response == "t"

    def bust(self):
        print(self.name, "ma fur�.")
        self.lose()

    def lose(self):
        print(self.name, "przegrywa.")

    def win(self):
        print(self.name, "wygrywa.")

    def push(self):
        print(self.name, "remisuje.")


class BJ_Dealer(BJ_Hand):
    """ Rozdaj�cy w blackjacku. """

    def is_hitting(self):
        return self.total < 17

    def bust(self):
        print(self.name, "ma fur�.")

    def flip_first_card(self):
        first_card = self.cards[0]
        first_card.flip()


class BJ_Game(object):
    """ Gra w blackjacka. """

    def __init__(self, names):
        self.players = []
        for name in names:
            player = BJ_Player(name)
            self.players.append(player)

        self.dealer = BJ_Dealer("Rozdaj�cy")

        self.deck = BJ_Deck()
        self.deck.populate()

    @property
    def still_playing(self):
        sp = []
        for player in self.players:
            if not player.is_busted():
                sp.append(player)
        return sp

    def __additional_cards(self, player):
        while not(player.is_busted() or player.is_21()) and player.is_hitting():
            self.deck.deal([player])
            print(player)
            if player.is_busted():
                player.bust()

    def play(self):
        #przygotowanie tali kart
        self.deck.populate()

        # rozdaj ka�demu pocz�tkowe dwie karty
        self.deck.deal(self.players + [self.dealer], per_hand=2)
        self.dealer.flip_first_card()  # ukryj pierwsz� kart� rozdaj�cego
        for player in self.players:
            print(player)
        print(self.dealer)

        # rozdaj graczom dodatkowe karty
        for player in self.players:
            self.__additional_cards(player)

        self.dealer.flip_first_card()  # ods�o� pierwsz� kart� rozdaj�cego

        if not self.still_playing:
            # poniewa� wszyscy gracze dostali fur�, poka� tylko r�k� rozdaj�cego
            print(self.dealer)
        else:
            # daj dodatkowe karty rozdaj�cemu
            print(self.dealer)
            self.__additional_cards(self.dealer)

            if self.dealer.is_busted():
                # wygrywa ka�dy, kto jeszcze pozostaje w grze
                for player in self.still_playing:
                    player.win()
            else:
                # por�wnaj punkty ka�dego gracza pozostaj�cego w grze z punktami rozdaj�cego
                for player in self.still_playing:
                    if player.total > self.dealer.total:
                        player.win()
                    elif player.total < self.dealer.total:
                        player.lose()
                    else:
                        player.push()

        # usu� karty wszystkich graczy
        for player in self.players:
            player.clear()
        self.dealer.clear()


def main():
    print("\t\tWitaj w grze 'Blackjack'!\n")

    names = []
    number = gry.ask_number("Podaj liczb� graczy (1 - 7): ", low=1, high=8)
    for i in range(number):
        name = input("Wprowad� nazw� gracza: ")
        names.append(name)
    print()

    game = BJ_Game(names)

    again = None
    while again != "n":
        game.play()
        again = gry.ask_yes_no("\nCzy chcesz zagra� ponownie?: ")


main()