from donatellopyzza import RLGame, Action, Feedback
import random
import time
from collections import defaultdict
from typing import Dict, Tuple


class QLearningAgent:
    def __init__(
        self,
        learning_rate: float = 0.1,
        discount_factor: float = 0.9,
        epsilon: float = 0.3,
        epsilon_decay: float = 0.995,
        epsilon_min: float = 0.01
    ):
        # Hyperparamètres Q-Learning
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.epsilon = epsilon
        self.epsilon_decay = epsilon_decay
        self.epsilon_min = epsilon_min

        # Table Q : état -> {action: valeur_Q}
        self.q_table: Dict[str, Dict[int, float]] = defaultdict(lambda: defaultdict(float))

        # Actions possibles
        self.actions = [Action.MOVE_FORWARD, Action.TURN_LEFT, Action.TURN_RIGHT, Action.TOUCH]

        # Récompenses ajustées
        self.rewards = {
            'pizza_found': 100.0,
            'pizza_touched': 50.0,
            'collision': -15.0,
            'step': -0.5,
            'wall_touched': -8.0,
            'new_state': 8.0,
            'proximity_bonus': 3.0,
            'efficiency_bonus': 10.0
        }

        self.episode_count = 0
        self.best_steps = float('inf')
        self.visited_states = set()
        self.pizza_position = None

    def get_state(self, position: Tuple[int, int], orientation: int, feedback: Feedback = None) -> str:
        state = f"pos_{position[0]}_{position[1]}_ori_{orientation}"
        if feedback == Feedback.TOUCHED_WALL:
            state += "_wall"
        elif feedback == Feedback.TOUCHED_PIZZA:
            state += "_pizza"
        elif feedback == Feedback.TOUCHED_NOTHING:
            state += "_empty"
        return state

    def calculate_reward(self, feedback: Feedback, state: str, position: Tuple[int, int]) -> float:
        # Calcule la récompense selon le feedback et le contexte
        base_reward = self.rewards['step']
        if feedback == Feedback.MOVED_ON_PIZZA:
            base_reward = self.rewards['pizza_found']
        elif feedback == Feedback.TOUCHED_PIZZA:
            base_reward = self.rewards['pizza_touched']
        elif feedback == Feedback.COLLISION:
            base_reward = self.rewards['collision']
        elif feedback == Feedback.TOUCHED_WALL:
            base_reward = self.rewards['wall_touched']

        # Bonus d'exploration pour un nouvel état
        if state not in self.visited_states:
            base_reward += self.rewards['new_state']
            self.visited_states.add(state)

        # Bonus de proximité de la pizza
        if self.pizza_position:
            distance = abs(position[0] - self.pizza_position[0]) + abs(position[1] - self.pizza_position[1])
            if distance <= 2:
                base_reward += self.rewards['proximity_bonus']

        return base_reward

    def choose_action(self, state: str) -> Action:
        # Politique epsilon-greedy : exploration ou exploitation
        if random.random() < self.epsilon:
            return random.choice(self.actions)

        if state in self.q_table and self.q_table[state]:
            best_action = max(self.q_table[state], key=self.q_table[state].get)
            for action in self.actions:
                if int(action.value) == best_action:
                    return action
        return random.choice(self.actions)

    def update_q_value(self, state: str, action: Action, reward: float, next_state: str):
        action_key = int(action.value)
        current_q = self.q_table[state][action_key]
        max_next_q = max(self.q_table[next_state].values()) if next_state in self.q_table else 0.0
        td_target = reward + self.discount_factor * max_next_q
        self.q_table[state][action_key] = current_q + self.learning_rate * (td_target - current_q)

    def decay_epsilon(self):
        # Réduction progressive de l’exploration
        self.epsilon = max(self.epsilon_min, self.epsilon * self.epsilon_decay)

    def train_episode(self, game: RLGame, turtle, show_gui: bool = True) -> Tuple[float, int, bool]:
        total_reward = 0.0
        steps = 0
        current_position = game.getTurtlePosition(turtle)
        current_orientation = game.getTurtleOrientation(turtle)
        current_state = self.get_state(current_position, current_orientation)

        while True:
            steps += 1
            action = self.choose_action(current_state)
            feedback, _ = turtle.execute(action)

            new_position = game.getTurtlePosition(turtle)
            new_orientation = game.getTurtleOrientation(turtle)
            next_state = self.get_state(new_position, new_orientation, feedback)

            reward = self.calculate_reward(feedback, current_state, new_position)
            total_reward += reward

            if feedback == Feedback.MOVED_ON_PIZZA and not self.pizza_position:
                self.pizza_position = new_position

            self.update_q_value(current_state, action, reward, next_state)

            if show_gui:
                time.sleep(0.01)

            if game.isWon(prnt=False):
                break

            current_state = next_state

        self.decay_epsilon()
        self.visited_states.clear()
        self.episode_count += 1

        success = game.isWon(prnt=False)
        if success and steps < self.best_steps:
            self.best_steps = steps

        return total_reward, steps, success


def train_agent(environment_name: str = "maze", max_episodes: int = 50, show_gui: bool = True) -> QLearningAgent:
    agent = QLearningAgent()
    print(f"\n=== Entraînement de l'agent sur {max_episodes} épisodes ===")
    for episode in range(max_episodes):
        game = RLGame(environment_name, gui=show_gui)
        turtle = game.start()
        reward, steps, success = agent.train_episode(game, turtle, show_gui)
        print(f"Épisode {episode + 1:3d} | Étapes: {steps:3d} | Récompense: {reward:7.1f} | Succès: {success}")
    print(f"\nEntraînement terminé. Meilleur chemin: {agent.best_steps} étapes.")
    return agent


def main():
    agent = train_agent(environment_name="test", max_episodes=30, show_gui=True)


if __name__ == "__main__":
    main()
