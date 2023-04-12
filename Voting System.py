import os
import csv
from collections import Counter
from termcolor import colored

# check if voters.txt file exists
if os.path.isfile("voters.txt"):
    # read the file and load candidates, candidate_votes and voters list
    with open("voters.txt", "r") as f:
        reader = csv.reader(f)
        candidates = next(reader)
        candidate_votes = dict(zip(candidates, [int(votes) for votes in next(reader)]))
        voters = set(next(reader))

else:
    # create empty candidates, candidate_votes and voters list
    candidates = []
    candidate_votes = {}
    voters = set()

password = "admin123"  # set the password globally
logged_in = False   # keep track of whether the user is logged in or not


def save_data():
    # write the candidates, candidate_votes and voters list to the file
    with open("voters.txt", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(candidates)
        writer.writerow(candidate_votes.values())
        writer.writerow(voters)


def login_menu():
    global logged_in
    print(colored("Welcome to the Voting System!", "cyan"))
    print(colored("Please select an option from the menu below:", "magenta"))
    print("1. Login as Admin")
    print("2. Login as User")
    print("3. Exit")

    option = input("> ")
    try:
        selected_option = int(option)
        if selected_option == 1:
            admin_login()
        elif selected_option == 2:
            user_login()
        elif selected_option == 3:
            print(colored("Goodbye!", "green"))
            exit()
        else:
            print(colored("Invalid input, please enter a valid option.", "red"))
            login_menu()
    except ValueError:
        print(colored("Invalid input, please enter a valid option.", "red"))
        login_menu()


def admin_login():
    global logged_in
    print("Please enter the password to access the admin menu:")
    user_password = input("> ")
    if user_password == password:
        logged_in = True
        admin_menu()
    else:
        print(colored("Access denied. Incorrect password.", "red"))
        login_menu()


def admin_menu():
    global logged_in  # use the global logged_in variable
    print(colored("Welcome Admin!", "cyan"))
    while logged_in: # run the loop while the admin is logged in
        print("Please select an option from the menu below:")
        print("1. Add Candidate")
        print("2. Remove Candidate")
        print("3. View Candidate List with Total Votes")
        print("4. View Total Votes")
        print("5. Logout and Return to Login Menu")

        option = input("> ")
        try:
            selected_option = int(option)
            if selected_option == 1:
                add_candidate()
            elif selected_option == 2:
                remove_candidate()
            elif selected_option == 3:
                view_candidates()
            elif selected_option == 4:
                view_total_votes()
            elif selected_option == 5:
                logged_in = False  # set logged_in to False to return to login menu
                save_data()
            else:
                print(colored("Invalid input, please enter a valid option.", "red"))
                admin_menu()
        except ValueError:
            print(colored("Invalid input, please enter a valid option.", "red"))       
            admin_menu()
    login_menu()  # go back to the login menu after logging out


def add_candidate():
    print("Enter the name of the candidate you wish to add:")
    candidate_name = input("> ")
    candidates.append(candidate_name)
    candidate_votes[candidate_name] = 0
    print(f"{candidate_name} has been added to the candidate list.")
    admin_menu()


def remove_candidate():
    if not candidates:
        print(colored("No candidates to remove.", "yellow"))
        admin_menu()
    else:
        candidate_list()
        print("Enter the number of the candidate you wish to remove:")
        try:
            selected_candidate = int(input("> "))
            if selected_candidate == -1:
                admin_menu()
            else:
                candidate_name = candidates[selected_candidate - 1]
                candidates.remove(candidate_name)
                del candidate_votes[candidate_name]
                print(f"{candidate_name} has been removed from the candidate list.")
                admin_menu()
        except (IndexError, ValueError):
            print("Invalid input, please enter a valid option.")
            remove_candidate()



def view_candidates():
    print("Candidate List with Total Votes:")
    for candidate in candidates:
        print(f"{candidate}: {candidate_votes.get(candidate, 0)}")
    admin_menu()


def view_total_votes():
    total_votes = sum(candidate_votes.values())
    print(f"Total Votes: {total_votes}")
    admin_menu()


def user_login():
    print("Please enter your voter ID:")
    voter_id = input("> ")
    if not voter_id.isnumeric() or len(voter_id) != 3 or int(voter_id) < 1 or int(voter_id) > 500:
        # check if voter ID does not contain exactly 3 numbers or is not between 001 to 500
        print(colored("Invalid input. Voter ID must be a 3-digit number between 001 to 500.", "red"))
        user_login()
    elif check_voter(voter_id):
        print(colored("You have already voted. Thank you for your participation!", "yellow"))
    else:
        candidate_list()
        vote(voter_id)
    save_data()
    login_menu()



def candidate_list():
    print(colored("Please select your candidate from the list below:", "yellow"))
    for i, candidate in enumerate(candidates):
        print(f"{i+1}. {candidate}")


def vote(voter_id):
    print("Please enter the number of your selected candidate:")
    try:
        selected_candidate = int(input("> "))
        candidate_name = candidates[selected_candidate - 1]
        candidate_votes[candidate_name] += 1
        print(f"Thank you for voting {candidate_name}!")
        voters.add(voter_id)
    except (IndexError, ValueError):
        print("Invalid input, please enter a valid option.")
        vote(voter_id)


def check_voter(voter_id):
    if voter_id in voters:
        return True
    else:
        return False


login_menu()
