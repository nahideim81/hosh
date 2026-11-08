# Simple Reflex Agent - Light Switch
# Environment: 2x2 grid (4 cells), each cell has a light
# Goal: turn off all the lights

class LightSwitchAgent:
    def __init__(self):
        # cells 0,1,2,3 = (0,0), (0,1), (1,0), (1,1) of the 2x2 grid
        self.lights = ['on', 'on', 'on', 'off']
        self.location = 0

    def interpret_input(self):
        return self.lights[self.location]  # percept

    def rule_action(self, state):
        if state == 'on':
            print("Turning off light in cell", self.location)
            self.lights[self.location] = 'off'
        else:
            print("Moving to the next cell")
            self.location = (self.location + 1) % len(self.lights)


agent = LightSwitchAgent()
print("Initial lights:", agent.lights)
for _ in range(7):
    state = agent.interpret_input()
    agent.rule_action(state)
    print("Lights:", agent.lights, "| Location:", agent.location)
print("Final lights:", agent.lights)
