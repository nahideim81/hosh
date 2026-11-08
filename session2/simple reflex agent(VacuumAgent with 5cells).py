class VacuumAgent:
    def __init__(self):
        self.location = 2  # percept (start cell)
        self.environment = ['dirty', 'dirty', 'dirty', 'clean', 'dirty']
        self.cleaned = 0   # number of cleaned cells

    def interpret_input(self):
        return self.environment[self.location]  # state

    def rule_action(self, state):
        if state == 'dirty':
            self.environment[self.location] = 'clean'
            self.cleaned += 1
            print(f"Cleaning cell {self.location} -> {self.environment}")
        else:
            # move to the next cell (wrap around)
            self.location = (self.location + 1) % len(self.environment)
            print(f"Cell {self.location} is clean, moving to cell {self.location}")

    def is_all_clean(self):
        return 'dirty' not in self.environment


agent = VacuumAgent()
print("Initial environment:", agent.environment)

# Keep acting until every cell is clean (with a safety limit)
step = 0
while not agent.is_all_clean() and step < 20:
    step += 1
    print(f"Step {step}:", end=" ")
    state = agent.interpret_input()
    agent.rule_action(state)

if agent.is_all_clean():
    print("All cells are clean!")
else:
    print("Stopped: max steps reached")
print("Final environment:", agent.environment)
