import colors
import heapq


class Agent:
    def __init__(self, board):
        self.position = board.get_agent_pos()
        self.current_state = board.get_current_state()
        for action in self.a_star(board):
            board.colorize(action[0], action[1])

    def get_position(self):
        return self.position

    def set_position(self, position, board):
        self.position = position
        board.set_agent_pos(position)
        board.update_board(self.current_state)

    def percept(self, board):
        # perception :
        # sets the current state
        # Use get_current_state function to get the maze matrix. - make your state
        self.current_state = board.get_current_state()

        pass

    def move(self, direction):
        # make your next move based on your perception
        # check if the move destination is not blocked
        # if not blocked , move to destination - set new position
        # something like :
        self.set_position(self.get_position() + direction)

        pass

    def expand(self, pos):
        tile = self.current_state[pos[0]][pos[1]]
        if tile.isGoal or tile.isStart:
            return
        tile.set_color(colors.selectionColor)

    @staticmethod
    def get_actions():
        actions = []
        return actions

    def get_neighbours(self, state):
        states = []
        for direction in [(-1, 0), (+1, 0), (0, -1), (0, +1)]:
            x, y = state[0] + direction[0], state[1] + direction[1]
            if x < 0 or x >= len(self.current_state):
                continue
            if y < 0 or y >= len(self.current_state[x]):
                continue
            tile = self.current_state[x][y]
            if not tile.is_blocked():
                states.append((x, y))
        return states

    def bfs(self, environment):
        self.percept(environment)
        queue = []
        visited = set()
        agent_pos = self.get_position()
        queue.append((agent_pos, []))
        goal_path = None
        while len(queue) > 0:
            state, path = queue.pop(0)
            self.expand(state)
            visited.add(state)
            if self.current_state[state[0]][state[1]].isGoal:
                goal_path = path
                break
            for next_state in self.get_neighbours(state):
                if not next_state in visited:
                    queue.append((next_state, path + [state]))
        return goal_path[1:]

    def dfs(self, environment):
        self.percept(environment)
        stack = []
        visited = set()
        agent_pos = self.get_position()
        stack.insert(0, (agent_pos, []))
        goal_path = None
        while len(stack) > 0:
            state, path = stack.pop(0)
            visited.add(state)
            self.expand(state)
            if self.current_state[state[0]][state[1]].isGoal:
                goal_path = path
                break
            for next_state in self.get_neighbours(state):
                if not next_state in visited:
                    stack.insert(0, (next_state, path + [state]))
        return goal_path[1:]

    def get_goal(self):
        for i in range(len(self.current_state)):
            for j in range(len(self.current_state[i])):
                if self.current_state[i][j].isGoal:
                    return i, j

    def heuristic(self, state):
        goal_pos = self.get_goal()
        return abs(state[0] - goal_pos[0]) + abs(state[1] - goal_pos[1])

    class PriorityQueue:
        def __init__(self):
            self.heap = []

        def push(self, item, priority):
            entry = (priority, item)
            heapq.heappush(self.heap, entry)

        def pop(self):
            (_, item) = heapq.heappop(self.heap)
            return item

        def isEmpty(self):
            return len(self.heap) == 0

        def update(self, item, priority):
            # If item already in priority queue with higher priority, update its priority and rebuild the heap.
            # If item already in priority queue with equal or lower priority, do nothing.
            # If item not in priority queue, do the same thing as self.push.
            for index, (p, i) in enumerate(self.heap):
                if i == item:
                    if p <= priority:
                        break
                    del self.heap[index]
                    self.heap.append((priority, item))
                    heapq.heapify(self.heap)
                    break
            else:
                self.push(item, priority)

    def a_star(self, environment):
        self.percept(environment)
        pqueue = Agent.PriorityQueue()
        visited = set()
        agent_pos = self.get_position()
        pqueue.push((agent_pos, [], 0), 0)
        goal_path = []
        while not pqueue.isEmpty():
            (state, path, g) = pqueue.pop()
            self.expand(state)
            visited.add(state)
            if self.current_state[state[0]][state[1]].isGoal:
                goal_path = path
                break
            for next_state in self.get_neighbours(state):
                if not next_state in visited:
                    pqueue.update(
                        (next_state, path + [state], g + 1), g + 1 + self.heuristic(next_state))
        return goal_path[1:]
