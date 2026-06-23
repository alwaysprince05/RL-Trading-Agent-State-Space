import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from mpl_toolkits.mplot3d import Axes3D
import random

# Simulate RL agent state transitions
class RLTradingAgentSimulator:
    def __init__(self, n_steps=300):
        self.n_steps = n_steps
        self.states = []  # (price, momentum, volatility)
        self.actions = []  # 0: hold, 1: buy, 2: sell
        self.q_values = []  # Q-value for each state
        self._simulate()

    def _simulate(self):
        price = 100
        momentum = 0
        volatility = 1
        q = 0.0
        for t in range(self.n_steps):
            # Simulate state
            price += np.random.normal(momentum, volatility)
            momentum += np.random.normal(0, 0.1)
            volatility = max(0.5, volatility + np.random.normal(0, 0.05))
            state = (price, momentum, volatility)
            # Simulate action (random at first, more structured later)
            if t < self.n_steps // 3:
                action = random.choice([0, 1, 2])
            elif t < 2 * self.n_steps // 3:
                action = np.argmax([momentum, -momentum, 0])  # buy if momentum up, sell if down
            else:
                action = np.argmax([momentum + 0.5*q, -momentum + 0.5*q, 0.1*q])
            # Simulate Q-value (increases as agent "learns")
            q = 0.9 * q + 0.1 * (1 if action == 1 else -1 if action == 2 else 0)
            self.states.append(state)
            self.actions.append(action)
            self.q_values.append(q)

    def get_data(self):
        return np.array(self.states), np.array(self.actions), np.array(self.q_values)

# Visualization
class RLTrading3DVisualizer:
    def __init__(self, states, actions, q_values):
        self.states = states
        self.actions = actions
        self.q_values = q_values
        self.colors = np.array(['gray', 'limegreen', 'crimson'])  # hold, buy, sell
        self.fig = plt.figure(figsize=(10, 7))
        self.ax = self.fig.add_subplot(111, projection='3d')
        self.scat = None
        self.line = None
        self.qsurf = None

    def _plot_q_surface(self):
        # Q-value surface overlay (bonus)
        grid_size = 20
        px = np.linspace(self.states[:,0].min(), self.states[:,0].max(), grid_size)
        my = np.linspace(self.states[:,1].min(), self.states[:,1].max(), grid_size)
        pxx, myy = np.meshgrid(px, my)
        # Fake Q-value surface for illustration
        q_surf = np.tanh((pxx-100)/10) * np.tanh(myy)
        self.qsurf = self.ax.plot_surface(pxx, myy, np.ones_like(pxx)*self.states[:,2].mean(),
                                          facecolors=plt.cm.viridis((q_surf+1)/2), alpha=0.3, linewidth=0)

    def animate(self):
        def update(frame):
            self.ax.clear()
            # Plot Q-value surface
            self._plot_q_surface()
            # Plot trajectory
            idx = slice(0, frame+1)
            c = self.colors[self.actions[idx]]
            self.scat = self.ax.scatter(self.states[idx,0], self.states[idx,1], self.states[idx,2],
                                        c=c, s=40, alpha=0.7, edgecolor='k')
            self.line = self.ax.plot(self.states[idx,0], self.states[idx,1], self.states[idx,2],
                                     color='black', linewidth=1, alpha=0.5)[0]
            self.ax.set_xlabel('Price')
            self.ax.set_ylabel('Momentum')
            self.ax.set_zlabel('Volatility')
            self.ax.set_title(f'RL Trading Agent State Space (Step {frame+1})')
            self.ax.set_xlim(self.states[:,0].min(), self.states[:,0].max())
            self.ax.set_ylim(self.states[:,1].min(), self.states[:,1].max())
            self.ax.set_zlim(self.states[:,2].min(), self.states[:,2].max())
            # Legend
            for i, label in enumerate(['Hold', 'Buy', 'Sell']):
                self.ax.scatter([], [], [], c=self.colors[i], label=label)
            self.ax.legend(loc='upper left')

        anim = FuncAnimation(self.fig, update, frames=len(self.states), interval=40, repeat=False)
        plt.show()

if __name__ == '__main__':
    sim = RLTradingAgentSimulator(n_steps=300)
    states, actions, q_values = sim.get_data()
    vis = RLTrading3DVisualizer(states, actions, q_values)
    vis.animate()
