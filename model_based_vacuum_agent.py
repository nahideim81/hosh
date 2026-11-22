class ModelBasedVacuumAgent:
    def __init__(self):
        # 2x2 environment: 'dirty' or 'clean'
        self.environment = [['dirty', 'clean'],
                            ['clean', 'dirty']]
        self.row = 0
        self.col = 0
        # internal state (model): what the agent remembers about each cell
        self.model = {(0, 0): 'unknown',
                      (0, 1): 'unknown',
                      (1, 0): 'unknown',
                      (1, 1): 'unknown'}

    def perceive(self):
        # step 1: perceive the current cell
        return self.environment[self.row][self.col]

    def update_model(self, percept):
        # step 2: update internal state with the new percept
        self.model[(self.row, self.col)] = percept

    def rule_action(self):
        # step 3: act based on the MODEL, not only the current percept
        here = self.model[(self.row, self.col)]

        if here == 'dirty':
            self.environment[self.row][self.col] = 'clean'
            self.model[(self.row, self.col)] = 'clean'
            print("Cleaning cell", (self.row, self.col))
            return

        # this cell is clean in the model -> go to an unknown/dirty cell
        for pos, state in self.model.items():
            if state in ('unknown', 'dirty'):
                return self.move_towards(pos)

        print("All cells are clean (from memory)")

    def move_towards(self, target):
        # move one step towards the target cell
        tr, tc = target
        if self.col < tc:
            self.col += 1
            print("Moving to cell", (self.row, self.col))
        elif self.col > tc:
            self.col -= 1
            print("Moving to cell", (self.row, self.col))
        elif self.row < tr:
            self.row += 1
            print("Moving to cell", (self.row, self.col))
        else:
            self.row -= 1
            print("Moving to cell", (self.row, self.col))

    def is_finished(self):
        # finished when memory says every cell is clean
        return all(s == 'clean' for s in self.model.values())


agent = ModelBasedVacuumAgent()
print("Initial environment:", agent.environment)
print("Initial model:", agent.model)

step = 0
while not agent.is_finished() and step < 12:
    step += 1
    percept = agent.perceive()          # درک
    agent.update_model(percept)         # آپدیت مدل
    agent.rule_action()                 # تصمیم بر اساس مدل

print("Final environment:", agent.environment)
print("Final model:", agent.model)
