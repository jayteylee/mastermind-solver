import collections
import itertools
import random

import numpy as np


class MastermindAgent():
    def __init__(self, code_length, colours, num_guesses):
        self.code_length = code_length
        self.colours = colours
        self.num_guesses = num_guesses
        self.all_codes = [''.join(p) for p in itertools.product(colours, repeat=code_length)]
        self.remaining_guesses = self.all_codes.copy()
        self.distinct_entropy_dict = collections.defaultdict(list)

    def AgentFunction(self, percepts):
        guess_counter, last_guess, in_place, in_colour = percepts

        best_guess = None
        max_entropy = -float('inf')

        # Iterate through all possible remaining guesses
        count = 0;
        for guess in self.all_codes:
            feedback_distribution = collections.defaultdict(int)

            # Iterate through sampled remaining solutions to calculate feedback distribution
            for sampled_guess in self.all_codes:
                in_place_guess, in_colour_guess = self.EvaluateFeedback(guess, sampled_guess)
                feedback_distribution[(in_place_guess, in_colour_guess)] += 1

            count += 1
            # Calculate entropy
            total_feedback = sum(feedback_distribution.values())
            entropy = -sum(
                count / total_feedback * np.log2(count / total_feedback) for count in feedback_distribution.values())
            # Max min entropy?
            print("count", count, ":", entropy, guess)

            distinct_colors = len(set(guess))

            self.distinct_entropy_dict[distinct_colors].append(entropy)

            # Update best guess if this guess has higher entropy
            if entropy > max_entropy:
                max_entropy = entropy
                best_guess = guess

        average_entropies = {}
        for distinct_colors, entropies in self.distinct_entropy_dict.items():
            average_entropy = sum(entropies) / len(entropies)
            average_entropies[distinct_colors] = average_entropy
        print(average_entropies)

        return list(best_guess)

    def EvaluateFeedback(self, code, last_code):
        code_array = np.array(list(code))
        last_code_array = np.array(list(last_code))

        place = np.sum(code_array == last_code_array)
        common = collections.Counter(code) & collections.Counter(last_code)
        colour = sum(common.values()) - place

        return place, colour

    def CompareFeedback(self, code, last_code, last_in_place, last_in_colour):
        place, colour = self.EvaluateFeedback(code, last_code)
        return (place, colour) == (last_in_place, last_in_colour)
