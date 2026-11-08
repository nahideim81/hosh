import random

BEATS = {'rock': 'scissors', 'paper': 'rock', 'scissors': 'paper'}
# inverse: what move WINS against each move
WINS_WITH = {'scissors': 'rock', 'rock': 'paper', 'paper': 'scissors'}


def utility_function(user, agent):
    """Returns 1 if agent wins, 0 if tie, -1 if user wins."""
    if BEATS[agent] == user:
        return 1
    elif agent == user:
        return 0
    else:
        return -1


def predict_user_move(memory):
    """Utility-based: use internal memory to predict the user's next move."""
    if not memory:
        return random.choice(list(BEATS))
    # most frequent choice of the user so far
    return max(set(memory), key=memory.count)


def Internal_memory(user, memory):
    """Remember the user's move in internal memory."""
    memory.append(user)


agent_choices = ["rock", "paper", "scissors"]
memory = []                     # internal memory of user moves
target = int(input("Enter the winning score: "))
user_score, agent_score = 0, 0

while user_score != target and agent_score != target:
    user_choice = input("Enter your choice (rock/paper/scissors): ").strip().lower()
    if user_choice not in BEATS:
        print("Invalid choice, try again (rock/paper/scissors)")
        continue

    # Agent predicts the user and plays the move that beats the prediction
    predicted = predict_user_move(memory)
    agent_choice = WINS_WITH[predicted]
    print(f"Agent chose {agent_choice}")

    result = utility_function(user_choice, agent_choice)
    if result == 1:
        agent_score += 1
    elif result == -1:
        user_score += 1
    else:
        print("It's a tie, no points")

    Internal_memory(user_choice, memory)
    print(f"user score = {user_score} , agent score = {agent_score}")

if agent_score == target:
    print("Winer is agent :)")
else:
    print("User is winer :(")
print("The final agent choices based update with internal memory is", agent_choices)
print("User move history (internal memory):", memory)
