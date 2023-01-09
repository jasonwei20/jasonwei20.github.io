# From http://rl-gym-doc.s3-website-us-west-2.amazonaws.com/mlss/pg-startercode.py
import gymnasium as gym
import numpy as np
import torch
device = torch.device("cpu")
torch.manual_seed(0)


def discount(rewards, gamma):
    """
    Given vector rewards, computes a vector y such that
    discounted_reward_to_go[i] = rewards[i] + gamma * rewards[i+1] + gamma^2 * rewards[i+2] + ...
    Example: discount(np.array([1, 1, 1]), gamma=0.9) returns [2.71 1.9  1.  ]
    """
    discounted_reward_to_go = np.zeros(len(rewards), 'float64')
    discounted_reward_to_go[-1] = rewards[-1]
    for i in reversed(range(len(rewards)-1)):
        discounted_reward_to_go[i] = rewards[i] + gamma * discounted_reward_to_go[i+1]
    assert rewards.ndim >= 1
    return discounted_reward_to_go


def categorical_sample(prob_n):
    """
    Sample from categorical distribution, specified by a vector of class probabilities.
    """
    if type(prob_n) == torch.Tensor:
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

        self.config = dict(
            episode_max_length=100, 
            timesteps_per_batch=10000, 
            num_iterations=100, 
            gamma=1.0, 
            stepsize=0.05, 
            hidden_units=20
        )
        self.config.update(userconfig)

        self.fc1 = torch.nn.Linear(num_inputs, self.config['hidden_units'])
        self.fc2 = torch.nn.Linear(self.config['hidden_units'], num_outputs)

    def forward(self, observations):
        x = torch.tanh(self.fc1(observations))
        x = self.fc2(x)
        return torch.softmax(x, dim=1)

    def act(self, ob):
        if type(ob) == tuple:
            torch_input = torch.from_numpy(ob[0].reshape(1,-1))
        else:
            torch_input = torch.from_numpy(ob.reshape(1,-1))
        prob = self.forward(torch_input)
        action = categorical_sample(prob)
        return action

    def policy_gradient_update(self, observations, actions, advantages, stepsize):

        observations = torch.from_numpy(observations)
        actions = torch.from_numpy(actions)
        advantages = torch.from_numpy(advantages)
        num_examples = observations.shape[0]

        # Forward pass. 
        # Input is observations, shape [timesteps_per_batch, observation space].
        # Output is predicted_softmax_probabilities, shape [timesteps_per_batch, action space].
        # E.g., for Cartpole actions are {0, 1}, so action space is length 2.
        predicted_softmax_probabilities = self.forward(observations)

        # Use the softmax probabilities to get the probabilities of each action.
        # predicted_action_probabilities is shape [timesteps_per_batch, ]
        predicted_action_probabilities = predicted_softmax_probabilities[torch.arange(num_examples), actions]

        # Compute the reward.
        advantages = advantages.type(predicted_action_probabilities.type())
        J_value = torch.log(predicted_action_probabilities).dot(advantages) / num_examples
        print(f'J_value: \t {J_value}') # Is this variable supposed to go down or up throughout training?

        # Backprop.
        J_value.backward()

        # Update with the gradient step.
        with torch.no_grad():
            for param in self.parameters():
                param.data += stepsize * param.grad
        self.zero_grad()

    def learn(self, env):
        config = self.config

        for iteration in range(config["num_iterations"]):

            # Collect trajectories until we get timesteps_per_batch total timesteps.
            trajectories = []
            total_timesteps = 0
            while total_timesteps < config["timesteps_per_batch"]:
                trajectory = get_trajectory(self, env, config["episode_max_length"])
                trajectories.append(trajectory)
                total_timesteps += len(trajectory["reward"])

            # Each trajectory has observation, action, and reward.
            # Observation is shape [length of trajectory, size of state space]
            # Action is shape [length of trajectory, size of action space]
            # Reward is shape [length of trajectory, ]

            # After concatenating all observations, this is shape [timesteps_per_batch, size of state space]
            observations = np.concatenate([trajectory["ob"] for trajectory in trajectories])

            # After concatenating all actions, this is shape [timesteps_per_batch, size of action space].
            actions = np.concatenate([trajectory["action"] for trajectory in trajectories])

            # Compute returns, which is the discounted sums of rewards to-go.
            # This is a list of returns. Each return is shape [length of trajectory, ].
            returns = [discount(trajectory["reward"], config["gamma"]) for trajectory in trajectories]

            # Compute time-dependent baseline.
            # baseline is a list of scalars, one for each time-step.
            # The shape of baselines [max trajectory length, ]
            max_trajectory_len = max(len(_return) for _return in returns)
            padded_returns = [np.concatenate(
                [_return, np.zeros(max_trajectory_len-len(_return))]) for _return in returns]
            baseline = np.mean(padded_returns, axis=0)

            # Subtract baseline to compute advantages.
            # advantages is shape [timesteps_per_batch, ]
            advantages = [_return - baseline[:len(_return)] for _return in returns]
            advantages = np.concatenate(advantages)

            # Do the policy gradient step.
            self.policy_gradient_update(
                observations,
                actions,
                advantages,
                config["stepsize"]
            )

            # Log information.
            episode_rewards = np.array([trajectory["reward"].sum() for trajectory in trajectories]) # episode total rewards
            episode_lengths = np.array([len(trajectory["reward"]) for trajectory in trajectories]) # episode lengths

            print(f'------ Iteration {iteration} ------')
            print(f'# Trajectories: {len(episode_rewards)}')
            print(f'# Timesteps:    {np.sum(episode_lengths)}')
            print(f'Max reward:     {episode_rewards.max():.1f}')
            print(f'Mean reward:    {episode_rewards.mean():.1f} std= {episode_rewards.std():.1f}')
            print(f'Mean length:    {episode_lengths.mean():.1f} std= {episode_lengths.std():.1f}')
            print('\n\n')
            # get_trajectory(self, env, config["episode_max_length"], render=True)

environment = gym.make("CartPole-v1")
# Actually run the experiment.
agent = REINFORCEAgent(environment, episode_max_length=100, num_iterations=1000, timesteps_per_batch=100000)

# Debug to print the shapes.
# agent = REINFORCEAgent(environment, episode_max_length=30, num_iterations=1, timesteps_per_batch=150)
agent.learn(environment)
