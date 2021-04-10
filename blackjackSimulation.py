from random import shuffle
import multiprocessing


def newDeck():  # creates a new deck for us
    return list(range(2, 14)) * 4

def playBlackJack(batchSize):
    playerWins = 0
    dealerWins = 0
    Draws = 0
    for i in range(batchSize):
        deck = newDeck()
        shuffle(deck)
        while len(deck) >= 13:  # plays until we only have quarter of the deck
            player = 0
            dealer = 0
            playerAces = 0
            while sorted(deck)[len(deck) // 2] + player < 21:  # there are more cards, than wouldn't get us beyond our limit, than card, that would
                card = deck[-1]
                player += card
                if card == 11:  # player got an ace
                    playerAces += 1
                del deck[-1]
            if player > 21:  # player busted
                if playerAces > 0:  # has aces to transform
                    player -= 10  # transforming an ace to 1
                    playerAces -= 1
                    while sorted(deck)[len(deck) // 2] + player < 21 and playerAces > 0: # there are more cards, than wouldn't get us beyond our limit, than card, that would, and player can still trasform their aces
                        card = deck[-1]
                        player += card
                        if card == 11:
                            playerAces += 1
                        del deck[-1]
                if player > 21:  # still over
                    dealerWins += 1
                    continue
            while dealer <= 16:  # must have >= 16 on cards at the end
                card = deck[-1]
                dealer += card
                del deck[-1]
            #dealer busted
            if dealer > 21:
                playerWins += 1
                continue
            #player won
            if player > dealer:
                playerWins += 1
            #dealer won
            elif dealer > player:
                dealerWins += 1
            #they drew
            else:
                Draws += 1
    queue.put((playerWins, dealerWins, Draws))  # writes out our results


def multiprocessingStarter(cores, batchSize):
    global playerWins, dealerWins, draws, queue

    processes = []
    for _ in range(cores):
        process = multiprocessing.Process(target=playBlackJack, args=(batchSize,))
        process.start()
        processes.append(process)
    for process in processes:
        process.join()
    #returns our results
    for core in range(cores):
        result = queue.get()
        playerWins += result[0]
        dealerWins += result[1]
        draws += result[2]


queue = multiprocessing.Queue()
cores = multiprocessing.cpu_count()
simulations = 1_000_000
playerWins = 0
dealerWins = 0
draws = 0

multiprocessingStarter(cores, simulations // cores)

rounds = playerWins + dealerWins + draws
print(f"""
Player won {round(playerWins / rounds * 100, 2)}% of the time
Dealer won {round(dealerWins / rounds * 100, 2)}% of the time
They drew {round(draws / rounds * 100, 2)}% of the time
""")
