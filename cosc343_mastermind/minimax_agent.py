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

    def AgentFunction(self, percepts):
        guess_counter, last_guess, in_place, in_colour = percepts
        if guess_counter == 0:
            self.remaining_guesses = self.all_codes.copy()
            guess = random.choice(self.remaining_guesses)  # Initial random guess
            # guess = ['B', 'G', 'R', 'R', 'G']

            # Generate a first guess with four distinct colors (one color repeated)
            # distinct_colors = random.sample(self.colours, 3)
            # repeated_color1 = random.choice(distinct_colors)
            # repeated_color2 = random.choice(distinct_colors)
            # distinct_colors.append(repeated_color1)
            # distinct_colors.append(repeated_color2)
            # random.shuffle(distinct_colors)
            # guess = distinct_colors

            return list(guess)

        # Remove guesses that don't match the feedback
        self.remaining_guesses = [guess for guess in self.remaining_guesses if
                                  self.CompareFeedback(guess, last_guess, in_place, in_colour)]

        print("Possible Codes Remaining", len(self.remaining_guesses))
        best_guess = None
        max_entropy = -float('inf')
        min_entropy = 100;
        sample_size = 100  # Adjust this value based on your needs
        feedback_distribution_max = collections.defaultdict(int)
        feedback_distribution_min = collections.defaultdict(int)

        max_guess_count = 0
        min_guess_count = 0

        # Sample from remaining guesses
        sampled_remaining_guesses = random.sample(self.remaining_guesses, min(sample_size, len(self.remaining_guesses)))
        guess_count = 0
        # Iterate through all possible remaining guesses
        for guess in self.remaining_guesses:
            guess_count += 1
            feedback_distribution = collections.defaultdict(int)

            # Iterate through sampled remaining solutions to calculate feedback distribution
            for sampled_guess in sampled_remaining_guesses:
                in_place_guess, in_colour_guess = self.EvaluateFeedback(guess, sampled_guess)
                feedback_distribution[(in_place_guess, in_colour_guess)] += 1

            # Calculate entropy
            # total_feedback = sum(feedback_distribution.values())

            # Sum of all values would be the same as the number of sampled_remaining_guesses
            total_feedback = len(sampled_remaining_guesses)

            # print(guess_count, ":", feedback_distribution)

            #Shannon's Entropy
            entropy = -sum(
                count / total_feedback * np.log2(count / total_feedback) for count in feedback_distribution.values())

            # Update best guess if this guess has higher entropy
            if entropy > max_entropy:
                max_entropy = entropy
                best_guess = guess
                feedback_distribution_max = feedback_distribution
                max_guess_count = guess_count

            if entropy < min_entropy:
                min_entropy = entropy
                feedback_distribution_min = feedback_distribution
                min_guess_count = guess_count

        print("Highest entropy guess:", max_guess_count, feedback_distribution_max)
        print("Lowest entropy guess:", min_guess_count, feedback_distribution_min)
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
