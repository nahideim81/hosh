class RobotVacuumCleaner:
    def __init__(self):
        self.environment = ['clean', 'dirty', 'dirty', 'clean', 'dirty']
        self.position = 2
        self.model = {}          # internal state: {position: last percept}

    def perceive(self):
        return self.environment[self.position]

    def update_model(self, perception):
        self.model[self.position] = perception

    def predict_future_state(self):
        # Model-based: predict from internal memory, not only current percept
        if self.model.get(self.position) == 'dirty':
            return 'dirty'
        return 'clean'

    def decide_action(self):
        perception = self.perceive()
        self.update_model(perception)
        if perception == 'dirty':
            return 'suck'
        future_state = self.predict_future_state()
        if future_state == 'dirty':
            return 'suck'
        return 'move'

    def act(self, action):
        if action == 'suck':
            self.environment[self.position] = 'clean'
            # after cleaning, refresh the model of this cell
            self.model[self.position] = 'clean'
        elif action == 'move':
            self.position = (self.position + 1) % len(self.environment)
            # re-observe the new cell so the model stays accurate
            self.update_model(self.perceive())

    def is_all_clean(self):
        return 'dirty' not in self.environment


agent = RobotVacuumCleaner()
print("Initial environment:", agent.environment)

step = 0
while not agent.is_all_clean() and step < 20:
    step += 1
    action = agent.decide_action()
    agent.act(action)
    print(f"Step {step}: Position={agent.position}, Action={action}, "
          f"Environment={agent.environment}, Model={agent.model}")

if agent.is_all_clean():
    print("All cells are clean!")
else:
    print("Stopped: max steps reached")
print("Final environment:", agent.environment)
