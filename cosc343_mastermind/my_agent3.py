__author__ = "Jay Lee"
__organization__ = "COSC343/AIML402, University of Otago"
__email__ = "leeja744@student.otago.ac.nz"

import numpy as np
import itertools
import random
from collections import Counter
import math


class MastermindAgent():
    """
              A class that encapsulates the code dictating the
              behaviour of the agent playing the game of Mastermind.

              ...

              Attributes
              ----------
              code_length: int
                  the length of the code to guess
              colours : list of char
                  a list of colours represented as characters
              num_guesses : int
                  the max. number of guesses per game

              Methods
              -------
              AgentFunction(percepts)
                  Returns the next guess of the colours on the board
              """

    def __init__(self, code_length, colours, num_guesses):
        """
        :param code_length: the length of the code to guess
        :param colours: list of letter representing colours used to play
        :param num_guesses: the max. number of guesses per game
        """

        self.code_length = code_length
        self.colours = colours
        self.num_guesses = num_guesses
        self.possible_codes_tuples = list(itertools.product(colours, repeat=code_length))
        self.possible_codes_arrays = [np.array(inner_tuple) for inner_tuple in self.possible_codes_tuples]
        self.copied_array = self.possible_codes_arrays[:]

    def match_feedback(self, code, last_guess, in_colour, in_place):
        # Count the occurrences of each color in 'code' and 'last_guess'
        code_counts = Counter(code)
        last_guess_counts = Counter(last_guess)

        # Calculate the overall number of in_place and in_colour colors
        in_place_count = sum(1 for i in range(len(code)) if code[i] == last_guess[i])
        in_colour_count = sum(min(code_counts[color], last_guess_counts[color]) for color in set(code))

        # Return True if the calculated counts match the provided in_colour and in_place values, otherwise return False
        return in_place_count == in_place and in_colour_count - in_place_count == in_colour

    def filter_possible_codes(self, last_guess, in_colour, in_place):
        self.copied_array = [code for code in self.copied_array if
                             self.match_feedback(code, last_guess, in_colour, in_place)]

    def calculate_entropy(self, remaining_pool):
        total_remaining_guesses = len(remaining_pool)
        colour_counts = {}

        for guess in self.copied_array:
            for colour in guess:
                if colour in colour_counts:
                    colour_counts[colour] += 1
                else:
                    colour_counts[colour] = 1

        entropy_dict = {}

        # Calculate the entropy using the formula
        for color, count in colour_counts.items():
            probability = count / total_remaining_guesses
            entropy = -probability * math.log2(probability)
            entropy_dict[color] = entropy

        return entropy_dict

    # Function to calculate the entropy of a list of probabilities
    def calculate_entropy(self, probabilities):
        entropy = -sum(p * math.log2(p) for p in probabilities if p > 0)
        return entropy

    def calculate_entropy_dict(self, remaining_pool):
        color_counts = {}
        total_colors = 0

        # Count the occurrences of each color in the remaining pool
        for guess in remaining_pool:
            for color in guess:
                if color in color_counts:
                    color_counts[color] += 1
                else:
                    color_counts[color] = 1
                total_colors += 1

        # Calculate the probabilities of each color based on the occurrences
        color_probabilities = {color: count / total_colors for color, count in color_counts.items()}

        # Calculate the entropy of each color based on the probabilities
        color_entropies = {color: self.calculate_entropy([probability]) for color, probability in
                           color_probabilities.items()}

        # Sort the colors based on their entropy values in descending order
        entropy_dict = dict(sorted(color_entropies.items(), key=lambda x: x[1], reverse=True))
        return entropy_dict

    # def select_colours_with_highest_entropy(self, entropy_dict):
    #     max_entropy = max(entropy_dict.values())
    #     highest_entropy_colors = [color for color, entropy in entropy_dict.items() if entropy == max_entropy]
    #     return highest_entropy_colors

    # Function to select colors with the highest entropy and the next two highest entropies
    def select_colours_with_highest_entropy(self, entropy_dict):
        sorted_entropies = sorted(entropy_dict.items(), key=lambda x: x[1], reverse=True)
        highest_entropy_colors = [color for color, entropy in sorted_entropies[:3]]
        return highest_entropy_colors

    # Function to select colors with the lowest entropy and the next two lowest entropies
    def select_colours_with_lowest_entropy(self, entropy_dict):
        sorted_entropies = sorted(entropy_dict.items(), key=lambda x: x[1])
        lowest_entropy_colors = [color for color, entropy in sorted_entropies[:3]]
        return lowest_entropy_colors

    #
    # def select_colours_with_lowest_entropy(self, entropy_dict):
    #     max_entropy = min(entropy_dict.values())
    #     highest_entropy_colors = [color for color, entropy in entropy_dict.items() if entropy == max_entropy]
    #     return highest_entropy_colors

    def AgentFunction(self, percepts):
        """Returns the next board guess given state of the game in percepts

              :param percepts: a tuple of four items: guess_counter, last_guess, in_place, in_colour

                       , where

                       guess_counter - is an integer indicating how many guesses have been made, starting with 0 for
                                       initial guess;

                       last_guess - is a num_rows x num_cols structure with the copy of the previous guess

                       in_place - is the number of character in the last guess of correct colour and position

                       in_colour - is the number of characters in the last guess of correct colour but not in the
                                   correct position

              :return: list of chars - a list of code_length chars constituting the next guess
              """

        # Extract different parts of percepts.
        guess_counter, last_guess, in_place, in_colour = percepts

        # Create an list of colour caracters. Currently all the guesses are the first colour,
        # 'B' - probably good idea to replace this logic with a better guess
        if guess_counter == 0:
            self.copied_array = self.possible_codes_arrays[:]
            # action = random.choice(self.copied_array)
            action = [self.colours[0]] * 3 + [self.colours[1]] * 2
            return action
        else:
            self.filter_possible_codes(last_guess, in_colour, in_place)
            print("Possible Codes Remaining", len(self.copied_array))
            entropy_dict = self.calculate_entropy_dict(self.copied_array)
            for colour, count in entropy_dict.items():
                print(colour, count)

            # action = random.choice(self.copied_array)

            highest_entropy_colors = self.select_colours_with_highest_entropy(entropy_dict)
            lowest_entropy_colors = self.select_colours_with_lowest_entropy(entropy_dict)

            # Start with an empty list for the next guess
            action = []

            for color, entropy in entropy_dict.items():
                if len(action) < 5:
                    if color in highest_entropy_colors:
                        action.append(color)

            for color in highest_entropy_colors:
                if len(action) < 5:
                    action.append(color)

            # Fill in the remaining slots with random colors from the remaining pool
            while len(action) < 5:
                available_colors = set(self.colours) - set(action)
                remaining_pool_colors = set(self.copied_array[0])
                possible_colors = available_colors.intersection(remaining_pool_colors)

                if possible_colors:
                    random_color = random.choice(list(possible_colors))
                    if all(c in self.copied_array[0] for c in action + [random_color]):
                        action.append(random_color)
                else:
                    random_color = random.choice(list(available_colors))
                    if all(c in self.copied_array[0] for c in action + [random_color]):
                        action.append(random_color)

        return action
