# From http://rl-gym-doc.s3-website-us-west-2.amazonaws.com/mlss/pg-startercode.py

import gymnasium as gym
import numpy as np
import torch
device = torch.device("cpu")
torch.manual_seed(0)


def discount(x, gamma):
    """
    Given vector x, computes a vector y such that
    y[i] = x[i] + gamma * x[i+1] + gamma^2 x[i+2] + ...
    """
    out = np.zeros(len(x), 'float64')
    out[-1] = x[-1]
    for i in reversed(range(len(x)-1)):
        out[i] = x[i] + gamma*out[i+1]
    assert x.ndim >= 1
    # More efficient version:
    # scipy.signal.lfilter([1],[1,-gamma],x[::-1], axis=0)[::-1]
    return out


def categorical_sample(prob_n):
    """
    Sample from categorical distribution,
    specified by a vector of class probabilities
    """
    prob_n = prob_n.detach().numpy()
    csprob_n = np.cumsum(prob_n)
    return (csprob_n > np.random.rand()).argmax()


def get_trajectory(agent, environment, episode_max_length=1, render=False):
    """
    Run agent-environment loop for one whole episode (trajectory).
    Returns a dictionary of results.
    """
    ob = environment.reset()
    obs = []
    actions = []
    rewards = []
    environment.step(environment.action_space.sample())
    for _ in range(episode_max_length):
        action = agent.act(ob)
        # action = environment.action_space.sample()
        (ob, reward, done, _, _) = environment.step(action)
        obs.append(ob)
        actions.append(action)
        rewards.append(reward)
        if done: break
        if render: environment.render()
    return {
        'reward' : np.array(rewards),
        'ob' : np.array(obs),
        'action' : np.array(actions)
    }


class REINFORCEAgent(torch.nn.Module):
    def __init__(self, environment, **userconfig):
        super().__init__()
        num_inputs = environment.observation_space.shape[0]
        num_outputs = environment.action_space.n

        # Set algorithm parameters
        self.config = dict(episode_max_length=100, timesteps_per_batch=10000, n_iter=100, 
            gamma=1.0, stepsize=0.05, hidden_units=20)
        self.config.update(userconfig)

        # Define neural network with one hidden layer
        self.fc1 = torch.nn.Linear(num_inputs, self.config['hidden_units'])
        self.fc2 = torch.nn.Linear(self.config['hidden_units'], num_outputs)

    def forward(self, observations):
        x = torch.tanh(self.fc1(observations))
        x = self.fc2(x)
        return torch.softmax(x, dim=1)
    
    def compute_prob(self, observations):
        return self.forward(observations)

    def policy_gradient_update(self, observations, actions, advantages, stepsize):
        predicted_softmax_probabilities = self.forward(observations)
        num_examples = observations.shape[0]
        predicted_action_probabilities = predicted_softmax_probabilities[torch.arange(num_examples), actions]
        loss = torch.log(predicted_action_probabilities).dot(advantages.type(predicted_action_probabilities.type())) / num_examples
        # print(f'Advantage sum: {torch.sum(advantages)}')
        print(f'loss: \t {loss}')
        loss.backward()
        with torch.no_grad():
            for param in self.parameters():
                param.data += stepsize * param.grad  # +=?
        self.zero_grad()

    def act(self, ob):
        if type(ob) == tuple:
            torch_input = torch.from_numpy(ob[0].reshape(1,-1))
        else:
            torch_input = torch.from_numpy(ob.reshape(1,-1))
        prob = self.compute_prob(torch_input)
        action = categorical_sample(prob)
        return action

    def learn(self, env):
        config = self.config

        for iteration in range(config["n_iter"]):

            # Collect trajectories until we get timesteps_per_batch total timesteps.
            trajectories = []
            total_timesteps = 0
            while total_timesteps < config["timesteps_per_batch"]:
                trajectory = get_trajectory(self, env, config["episode_max_length"])
                trajectories.append(trajectory)
                total_timesteps += len(trajectory["reward"])

            # Compute discounted sums of rewards.
            returns = [discount(trajectory["reward"], config["gamma"]) for trajectory in trajectories]
            maxlen = max(len(_return) for _return in returns)
            padded_returns = [np.concatenate([_return, np.zeros(maxlen-len(_return))]) for _return in returns]

            # Compute time-dependent baseline.
            baseline = np.mean(padded_returns, axis=0)

            # Compute advantage function.
            observations = np.concatenate([trajectory["ob"] for trajectory in trajectories])
            actions = np.concatenate([trajectory["action"] for trajectory in trajectories])
            advantages = [_return - baseline[:len(_return)] for _return in returns]
            advantages = np.concatenate(advantages)
            # print(advantages[:10])

            observations = torch.from_numpy(observations)
            actions = torch.from_numpy(actions)
            advantages = torch.from_numpy(advantages)

            # Do the gradient step.
            self.policy_gradient_update(observations, actions, advantages, config["stepsize"])

            eprews = np.array([trajectory["reward"].sum() for trajectory in trajectories]) # episode total rewards
            eplens = np.array([len(trajectory["reward"]) for trajectory in trajectories]) # episode lengths

            print(f'------ Iteration {iteration} ------')
            print(f'# Trajectories: {len(eprews)}')
            print(f'# Timesteps:    {np.sum(eplens)}')
            print(f'Max Reward:     {eprews.max():.1f}')
            print(f'Mean Reward:    {eprews.mean():.1f} +- {eprews.std()/np.sqrt(len(eprews)):.1f}')
            print(f'Mean Length:    {eplens.mean():.1f} +- {eplens.std()/np.sqrt(len(eplens)):.1f}')
            print('\n\n')
            get_trajectory(self, env, config["episode_max_length"], render=True)

environment = gym.make("CartPole-v1")
agent = REINFORCEAgent(environment, episode_max_length=100, n_iter=1000, timesteps_per_batch=100000)
agent.learn(environment)
