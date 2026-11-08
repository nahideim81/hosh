class VacuumAgent:
    def __init__(self):
        # 2x2 environment: 'dirty' or 'clean'
        self.environment = [['dirty', 'clean'],
                            ['clean', 'dirty']]
        self.row = 0
        self.col = 0

    def interpret_input(self):
        return self.environment[self.row][self.col]  # percept

    def rule_action(self, state):
        if state == 'dirty':
            print("Cleaning cell", (self.row, self.col))
            self.environment[self.row][self.col] = 'clean'
        else:
            # move to the next cell of the 2x2 grid (zigzag)
            idx = (self.row * 2 + self.col + 1) % 4
            self.row, self.col = divmod(idx, 2)
            print("Moving to cell", (self.row, self.col))

    def is_all_clean(self):
        return all(cell == 'clean'
                   for row in self.environment for cell in row)


agent = VacuumAgent()
print("Initial environment:", agent.environment)
while not agent.is_all_clean():
    state = agent.interpret_input()
    agent.rule_action(state)
print("Final environment:", agent.environment)
