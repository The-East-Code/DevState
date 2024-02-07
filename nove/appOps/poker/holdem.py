import tkinter as tk
from tkinter import ttk
import random

# Define a deck of cards
suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']
deck = [{'rank': rank, 'suit': suit} for suit in suits for rank in ranks]

# Shuffle the deck
random.shuffle(deck)

# Function to deal hands
def deal_hands(num_players):
    hands = [deck[i::num_players] for i in range(num_players)]
    return hands

# Function to deal community cards
def deal_community_cards():
    return deck[num_players * 2:num_players * 2 + 5]

# Create the main application window
app = tk.Tk()
app.title("Texas Hold'em Game")

# Function to update the GUI with player hands and community cards
def update_ui():
    for i, hand in enumerate(player_hands):
        hand_label_var[i].set(f"Player {i + 1}'s hand: {hand}")

    community_cards_str = ', '.join([f"{card['rank']} of {card['suit']}" for card in community_cards])
    community_cards_label_var.set(f"Community Cards: {community_cards_str}")


# Shuffle the deck again and deal hands
num_players = 4
player_hands = deal_hands(num_players)
community_cards = deal_community_cards()

# Create labels for displaying player hands and community cards
hand_label_var = [tk.StringVar() for _ in range(num_players)]
hand_labels = [tk.Label(app, textvariable=var) for var in hand_label_var]
for label in hand_labels:
    label.pack()

community_cards_label_var = tk.StringVar()
community_cards_label = tk.Label(app, textvariable=community_cards_label_var)
community_cards_label.pack()

# Function to deal new hands and update the UI
def deal_new_hands():
    shuffle_deck()
    global player_hands
    player_hands = deal_hands(num_players)
    global community_cards
    community_cards = deal_community_cards()
    update_ui()

# Button to deal new hands
deal_button = tk.Button(app, text="Deal New Hands", command=deal_new_hands)
deal_button.pack()

# Initial UI update
update_ui()

# Run the application
app.mainloop()
