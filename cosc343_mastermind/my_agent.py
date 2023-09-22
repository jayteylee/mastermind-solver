__author__ = "Jay Lee"
__organization__ = "COSC343/AIML402, University of Otago"
__email__ = "leeja744@student.otago.ac.nz"

import collections
import itertools
import random

import numpy as np

class MastermindAgent:
    """
    A class that encapsulates the code dictating the
    behavior of the agent playing the game of Mastermind.

    ...

    Attributes
    ----------
    code_length: int
        the length of the code to guess
    colours : list of char
        a list of colours represented as characters
    num_guesses : int
        the max. number of guesses per game
    all_codes : list of strings
        a list of all possible codes
    remaining_guesses : list of strings
        a list of all possible codes after each guess

    Methods
    -------
    __init__(self, code_length, colours, num_guesses)
        Initializes the MastermindAgent with code_length, colours, and num_guesses

    generate_all_codes(self)
        Generates all possible codes using itertools.product

    reset_remaining_guesses(self)
        Resets the list of remaining guesses to all possible codes

    AgentFunction(self, percepts)
        Returns the next guess of the colours on the board based on the current game state

    evaluate_feedback(self, code, last_code)
        Compares two codes and calculates the in-place and in-color counts

    compare_feedback(self, code, last_code, last_in_place, last_in_colour)
        Compares feedback between two codes to check if it matches the previous feedback

    filter_remaining_codes(self, last_guess, in_place, in_colour)
        Filters remaining guesses based on feedback

    find_best_guess(self)
        Finds the best guess based on entropy

    calculate_entropy(self, guess, sampled_remaining_guesses)
        Calculates the entropy of a guess based on sampled remaining guesses
    """

    def __init__(self, code_length, colours, num_guesses):
        """
        Initializes the MastermindAgent.

        :param code_length: the length of the code to guess
        :param colours: list of character representing available colors
        :param num_guesses: the max. number of guesses per game
        """
        self.code_length = code_length
        self.colours = colours
        self.num_guesses = num_guesses
        self.all_codes = self.generate_all_codes()
        self.remaining_guesses = self.all_codes.copy()

    def generate_all_codes(self):
        """
        Generates all possible codes using itertools.product.

        :return: list of strings representing all possible codes
        """
        return [''.join(combination) for combination in itertools.product(self.colours, repeat=self.code_length)]

    def reset_remaining_guesses(self):
        """
        Resets the list of remaining guesses to all possible codes.
        """
        self.remaining_guesses = self.all_codes.copy()

    def AgentFunction(self, percepts):
        """
        Returns the next guess of the colours on the board based on the current game state.

        :param percepts: a tuple containing information about the current game state
        :return: list of characters representing the next guess
        """
        guess_counter, last_guess, in_place, in_colour = percepts

        if guess_counter == 0:
            self.reset_remaining_guesses()
            distinct_colors = random.sample(self.colours, 3)
            repeated_color1 = random.choice(distinct_colors)
            repeated_color2 = random.choice(distinct_colors)
            distinct_colors.append(repeated_color1)
            distinct_colors.append(repeated_color2)
            random.shuffle(distinct_colors)
            guess = distinct_colors
            return list(guess)

        self.remaining_guesses = self.filter_remaining_codes(last_guess, in_place, in_colour)
        print("Possible Codes Remaining:", len(self.remaining_guesses))
        best_guess = self.find_best_guess()
        return list(best_guess)

    def evaluate_feedback(self, code, last_code):
        """
        Compares two codes and calculates the in-place and in-color counts.

        :param code: the current code to evaluate
        :param last_code: the previous guess
        :return: a tuple (in_place, in_colour) indicating the feedback counts
        """
        code_array = np.array(list(code))
        last_code_array = np.array(list(last_code))
        in_place = np.sum(code_array == last_code_array)
        common_colours = collections.Counter(code) & collections.Counter(last_code)
        in_colour = sum(common_colours.values()) - in_place
        return in_place, in_colour

    def compare_feedback(self, code, last_code, last_in_place, last_in_colour):
        """
        Compares feedback between two codes to check if it matches the previous feedback.

        :param code: the current code to compare
        :param last_code: the previous guess
        :param last_in_place: in-place count from previous feedback
        :param last_in_colour: in-colour count from previous feedback
        :return: True if the feedback matches, False otherwise
        """
        place, colour = self.evaluate_feedback(code, last_code)
        return (place, colour) == (last_in_place, last_in_colour)

    def filter_remaining_codes(self, last_guess, in_place, in_colour):
        """
        Filters remaining guesses based on feedback.

        :param last_guess: the previous guess
        :param in_place: in-place count from previous feedback
        :param in_colour: in-colour count from previous feedback
        :return: a list of remaining guesses after filtering
        """
        return [guess for guess in self.remaining_guesses if self.compare_feedback(guess, last_guess, in_place, in_colour)]

    def find_best_guess(self):
        """
        Finds the best guess based on entropy.

        :return: the best guess based on entropy
        """
        best_guess = None
        max_entropy = -float('inf')
        sample_size = 100
        sampled_remaining_guesses = random.sample(self.remaining_guesses, min(sample_size, len(self.remaining_guesses)))

        for guess in self.remaining_guesses:
            entropy = self.calculate_entropy(guess, sampled_remaining_guesses)

            if entropy > max_entropy:
                max_entropy = entropy
                best_guess = guess

        return best_guess

    def calculate_entropy(self, guess, sampled_remaining_guesses):
        """
        Calculates the entropy of a guess based on sampled remaining guesses.

        :param guess: the guess to calculate entropy for
        :param sampled_remaining_guesses: a list of sampled remaining guesses
        :return: the calculated entropy
        """
        feedback_distribution = collections.defaultdict(int)
        total_feedback = len(sampled_remaining_guesses)

        for sampled_guess in sampled_remaining_guesses:
            in_place_guess, in_colour_guess = self.evaluate_feedback(guess, sampled_guess)
            feedback_distribution[(in_place_guess, in_colour_guess)] += 1

        entropy = -sum(
            count / total_feedback * np.log2(count / total_feedback) for count in feedback_distribution.values())

        return entropy
