import torch


class DQNPolicy:
    def __init__(self, n_actions, station_space, n_hidden=128, lr=0.005):
        super().__init__()
        self.n_actions = n_actions

        self.dqn = torch.nn.Sequential(
            torch.nn.Linear(station_space, n_hidden),
            torch.nn.ReLU(),
            torch.nn.Linear(n_hidden, n_actions),
        )
        self.loss = torch.nn.MSELoss()
        self.optimizer = torch.optim.Adam(self.dqn.parameters(), lr=0.001)

    def make_action(self, state, eps=0):
        with torch.no_grad():
            best_action = torch.argmax(self.dqn(torch.Tensor(state)))
            if torch.rand((1,)).item() > eps:
                return best_action.item()
            return torch.randint(self.n_actions, (1,)).item()

    def update(self, state, next_state, action, reward, gamma=1):
        q_values = self.dqn(torch.Tensor(state))
        q_values_next = self.dqn(torch.Tensor(next_state))

        q_values_should_be = self.dqn(torch.Tensor(state)).tolist().copy()
        q_values_should_be[action] = reward + gamma * torch.max(q_values_next).item()

        self.optimizer.zero_grad()
        self.loss(q_values, torch.Tensor(q_values_should_be)).backward()
        self.optimizer.step()