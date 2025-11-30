import random
import os
import time

# Wörter und Reaktionen
WORDS = ['crazy', 'checkste', 'lowkey', 'tuff', 'tot', 'rede', 'Schere']

WRONG_REACTIONS = [
    "Ist das wirklich alles, was du drauf hast?",
    "Schon wieder falsch! So langsam tut es mir leid um dich...",
    "Oof ... Dieser Versuch hat schon beim Zuschauen wehgetan.",
    "Versuch’s noch mal, Verlierer!",
    "Nope!!!! Du bist nicht einmal annähernd richtig!",
]

RIGHT_REACTIONS = [
    "Warte ... das war richtig, oh nein!",
    "Das kann nicht wahr sein ... du könntest mich tatsächlich schlagen!",
    "Woher wusstest du das? Ich bin beeindruckt!",
    "Hör auf damit! Du kommst mir zu nah!",
    "Arrghhh ... du hast einen Buchstaben gefunden!",
]

HANGMAN_PICS = [
    """
      +---+
      |   |
          |
          |
          |
          |
    =========""",
    """
      +---+
      |   |
      O   |
          |
          |
          |
    =========""",
    """
      +---+
      |   |
      O   |
      |   |
          |
          |
    =========""",
    """
      +---+
      |   |
      O   |
     /|   |
          |
          |
    =========""",
    """
      +---+
      |   |
      O   |
     /|\\  |
          |
          |
    =========""",
    """
      +---+
      |   |
      O   |
     /|\\  |
     /    |
          |
    =========""",
    """
      +---+
      |   |
      O   |
     /|\\  |
     / \\  |
          |
    ========="""
]

ASCII_START = r"""
  o         o                                                                               
 <|>       <|>                                                                              
 < >       < >                                                                              
  |         |      o__ __o/  \o__ __o     o__ __o/  \o__ __o__ __o      o__ __o/  \o__ __o  
  o__/_ _\__o     /v     |    |     |>   /v     |    |     |     |>    /v     |    |     |> 
  |         |    />     / \  / \   / \  />     / \  / \   / \   / \   />     / \  / \   / \ 
 <o>       <o>   \      \o/  \o/   \o/  \      \o/  \o/   \o/   \o/   \      \o/  \o/   \o/ 
  |         |     o      |    |     |    o      |    |     |     |     o      |    |     |  
 / \       / \    <\__  / \  / \   / \   <\__  < >  / \   / \   / \    <\__  / \  / \   / \ 
                                                |                                           
                                        o__     o                                           
                                        <\__ __/>                                           
"""

ASCII_WIN = r"""
  \o       o/                         o              o     o              
   v\     /v                         <|>            <|>  _<|>_            
    <\   />                          / \            / \                   
      \o/    o__ __o     o       o   \o/            \o/    o    \o__ __o  
       |    /v     v\   <|>     <|>   |              |    <|>    |     |> 
      / \  />       <\  < >     < >  < >            < >   / \   / \   / \ 
      \o/  \         /   |       |    \o    o/\o    o/    \o/   \o/   \o/ 
       |    o       o    o       o     v\  /v  v\  /v      |     |     |  
      / \   <\__ __/>    <\__ __/>      <\/>    <\/>      / \   / \   / \ 
                                                                          
                                                                          
"""

ASCII_LOSE = r"""
      o__ __o                                                     o__ __o                                          
     /v     v\                                                   /v     v\                                         
    />       <\                                                 />       <\                                        
  o/                 o__ __o/  \o__ __o__ __o     o__  __o    o/           \o    o      o     o__  __o   \o__ __o  
 <|       _\__o__   /v     |    |     |     |>   /v      |>  <|             |>  <|>    <|>   /v      |>   |     |> 
  \\          |    />     / \  / \   / \   / \  />      //    \\           //   < >    < >  />      //   / \   < > 
    \         /    \      \o/  \o/   \o/   \o/  \o    o/        \         /      \o    o/   \o    o/     \o/       
     o       o      o      |    |     |     |    v\  /v __o      o       o        v\  /v     v\  /v __o   |        
     <\__ __/>      <\__  / \  / \   / \   / \    <\/> __/>      <\__ __/>         <\/>       <\/> __/>  / \       
                                                                                                                   
                                                                                                                   
                                                                                                                   
"""


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


def choose_word():
    return random.choice(WORDS)


def display_state(word_display, attempts_left, guessed_letters):
    print(HANGMAN_PICS[6 - attempts_left])
    print("\nWort: " + ' '.join(word_display))
    print(f"Versuche übrig: {attempts_left}")
    print(f"Geratene Buchstaben: {', '.join(guessed_letters)}")


def handle_guess(guess, word, word_display, guessed_letters, attempts_left):
    if guess in guessed_letters:
        print("Das hast du schon erraten! Versuch etwas Neues.")
        return attempts_left

    guessed_letters.append(guess)

    if guess in word.lower():
        for idx, letter in enumerate(word.lower()):
            if letter == guess:
                word_display[idx] = word[idx]
        print(random.choice(RIGHT_REACTIONS))
    else:
        attempts_left -= 1
        print(random.choice(WRONG_REACTIONS))

    return attempts_left


def play_hangman():
    clear()
    print(ASCII_START)
    time.sleep(1.5)

    word = choose_word()
    word_display = ['_'] * len(word)
    attempts_left = 6
    guessed_letters = []

    name = input("Willkommen bei Hangman! Wie heißt du? ")
    print(f"\nHi {name}! Mach dich bereit, dich dem Hangmanmeister zu stellen! 😈")
    print("Ich denke an ein Wort ... kannst du es erraten?\n")

    while attempts_left > 0 and '_' in word_display:
        display_state(word_display, attempts_left, guessed_letters)
        guess = input(f"{name}, gib einen Buchstaben ein (oder 'exit' zum Beenden): ").strip().lower()

        if guess in ["exit", "quit", "stop", "ende"]:
            print("\nSpiel wird beendet. Danke fürs Spielen! 👋")
            return

        if len(guess) != 1 or not guess.isalpha():
            print("Bitte gib einen einzelnen Buchstaben ein.")
            continue

        attempts_left = handle_guess(guess, word, word_display, guessed_letters, attempts_left)

    clear()
    if '_' not in word_display:
        print(ASCII_WIN)
        print(f"NEIN! Du hast es erraten! Das Wort war '{word}'.")
        print(f"Gut gespielt, {name} – du bist jetzt der Hangmanmeister! 👑")
    else:
        print(ASCII_LOSE)
        print(f"Das Wort war '{word}'.")
        print("Beim nächsten Mal hast du vielleicht Glück 😏")


if __name__ == "__main__":
    play_hangman()
