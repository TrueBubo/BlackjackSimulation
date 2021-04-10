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
        while len(deck) >= 13:  # quarter of the deck
            player = 0
            dealer = 0
            while sorted(deck)[len(deck) // 2] < 21 - player:
                card = deck[-1]
                player += card
                del deck[-1]
            if player > 21:
                dealerWins += 1
                continue
            while dealer <= 16:
                card = deck[-1]
                dealer += card
                del deck[-1]
            if dealer > 21:
                playerWins += 1
                continue
            if player > dealer:
                playerWins += 1
            elif dealer > player:
                dealerWins += 1
            else:
                Draws += 1
    queue.put((playerWins, dealerWins, Draws))


def multiprocessingStarter(cores, batchSize):
    global playerWins, dealerWins, draws, queue

    processes = []
    for _ in range(cores):
        process = multiprocessing.Process(target=playBlackJack, args=(batchSize,))
        process.start()
        processes.append(process)
    for process in processes:
        process.join()
    for core in range(cores):
        result = queue.get()
        playerWins += result[0]
        dealerWins += result[1]
        draws += result[2]


queue = multiprocessing.Queue()
cores = multiprocessing.cpu_count()
simulations = 999_999
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