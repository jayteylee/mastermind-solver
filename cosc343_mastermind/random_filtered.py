__author__ = "Jay Lee"
__organization__ = "COSC343/AIML402, University of Otago"
__email__ = "leeja744@student.otago.ac.nz"

import collections

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
        self.guesses_distribution = collections.defaultdict(int)

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
            action = random.choice(self.copied_array)
            return action
        else:
            self.filter_possible_codes(last_guess, in_colour, in_place)
            print("Possible Codes Remaining", len(self.copied_array))

            action = random.choice(self.copied_array)

            if in_place == 5:
                # Update the guesses count only when the puzzle is solved
                print("added to guesses!")
                # Update the guesses distribution dictionary
                if guess_counter in self.guesses_distribution:
                    self.guesses_distribution[self.guess_counter] += 1
                else:
                    self.guesses_distribution[self.guess_counter] = 1

                print(self.guesses_distribution)

            return action
