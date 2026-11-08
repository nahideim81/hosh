class MazeAgent:
    def __init__(self, start, goal, maze):
        self.position = start
        self.goal = goal
        self.maze = maze
        self.path = [start]
        self.visited = {start}   # remember visited cells (avoids infinite loops)

    def perceive(self):
        return self.position

    def act(self):
        if self.position == self.goal:
            return 'GoalReached'

        x, y = self.position
        # Simple right-hand rule, skipping walls AND already visited cells
        for action, (nx, ny) in [('Right', (x, y + 1)),
                                  ('Down', (x + 1, y)),
                                  ('Left', (x, y - 1)),
                                  ('Up', (x - 1, y))]:
            if self._is_open(nx, ny) and (nx, ny) not in self.visited:
                return action

        # Dead end: backtrack to the previous cell in the path
        if len(self.path) >= 2:
            px, py = self.path[-2]
            if px == x and py + 1 == y:
                return 'Left'
            if px == x and py - 1 == y:
                return 'Right'
            if px - 1 == x and py == y:
                return 'Down'
            return 'Up'
        return 'Trapped'  # no path to goal

    def _is_open(self, x, y):
        return 0 <= x < len(self.maze) and 0 <= y < len(self.maze[0]) \
            and self.maze[x][y] == 0

    def update_position(self, action):
        if action in ('GoalReached', 'Trapped'):
            return
        x, y = self.position
        moves = {'Right': (x, y + 1), 'Down': (x + 1, y),
                 'Left': (x, y - 1), 'Up': (x - 1, y)}
        self.position = moves[action]
        self.path.append(self.position)
        self.visited.add(self.position)

    def run(self, max_steps=50):
        for _ in range(max_steps):
            if self.position == self.goal:
                return True
            action = self.act()
            print(f"Position: {self.position}, Action: {action}")
            if action in ('GoalReached', 'Trapped'):
                break
            self.update_position(action)
        return self.position == self.goal


# Maze setup (0 = path, 1 = wall)
maze = [
    [1, 1, 1, 1, 1],
    [1, 0, 0, 0, 1],
    [1, 0, 1, 0, 1],
    [1, 0, 1, 0, 1],
    [1, 1, 1, 0, 1]
]

agent = MazeAgent(start=(1, 1), goal=(3, 3), maze=maze)
if agent.run():
    print("Path to goal:", agent.path)
else:
    print("Goal could not be reached")
