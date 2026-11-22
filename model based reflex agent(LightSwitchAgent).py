# Model-Based Reflex Agent - Light Switch
# Environment: 2x2 grid (4 cells), each cell has a light
# Goal: turn off all the lights
#
# Unlike the simple reflex agent, this agent keeps an internal model
# of every cell it has seen, so it does not wander blindly and it
# knows when the goal is reached.

class LightSwitchAgent:
    def __init__(self):
        self.lights = ['on', 'on', 'on', 'off']   # real environment
        self.model = [None, None, None, None]     # internal model (None = unknown)
        self.location = 0

    def perceive(self):
        return self.lights[self.location]         # percept

    def update_model(self, percept):
        self.model[self.location] = percept       # remember what I saw here

    def decide_action(self):
        here = self.model[self.location]          # decide from the MODEL
        if here == 'on':                          # light on here -> turn it off
            return 'turn_off'
        if None in self.model:                    # unknown cells -> explore
            return 'move'
        if 'on' in self.model:                    # model says a light is still on
            return 'move'
        return 'done'                             # model: every light is off

    def act(self, action):
        n = len(self.lights)
        if action == 'turn_off':
            print("Turning off light in cell", self.location)
            self.lights[self.location] = 'off'
            self.model[self.location] = 'off'
        elif action == 'move':
            # go to the nearest cell that is unknown or known 'on'
            for i in range(1, n + 1):
                idx = (self.location + i) % n
                if self.model[idx] is None or self.model[idx] == 'on':
                    self.location = idx
                    break
            print("Moving to cell", self.location)


agent = LightSwitchAgent()
print("Initial lights:", agent.lights)
print("Initial model :", agent.model)

while True:
    percept = agent.perceive()               # 1) perceive
    agent.update_model(percept)              # 2) update internal model
    action = agent.decide_action()           # 3) decide from the model
    print(f"Cell {agent.location} | percept={percept} | action={action} | model={agent.model}")
    if action == 'done':
        break
    agent.act(action)                        # 4) act

print("Final lights:", agent.lights)
