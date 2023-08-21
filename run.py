import random
import pickle

def main():
    print("Welcome to Battle at Sea!")

    while True:
        new_user = input("Are you a new user? (Y/N): ").upper()

        if new_user == 'Y':
            print("Welcome to Battleship! Let's set up your game.")
            username = input("Enter your username: ")
            password = input("Enter your password: ")
            game = BattleshipGame()
            game.reset_boards()  # Resetting the boards here
            game.save_state(username + '.pkl')
            game.play()
        elif new_user == 'N':
            print("Welcome back! Let's continue your existing game.")
            username = input("Enter your username: ")
            entered_password = input("Enter your password: ")
            game_filename = username + '.pkl'
            if check_password(username, entered_password):
                game = BattleshipGame.load_state(game_filename)
                game.print_boards()
                game.play()
            else:
                print("Invalid password.You can't continue the existing game.")
        else:
            print("Invalid input. Please enter Y or N.")
