"""This file contains the method for running the maths portion of the game, which calibrates the upper limit of
attention.
"""

import pandas as pd

from display import *
import fonts
import math
import random
import color


# region Constants

MAX_TIME = 60

# endregion Constants


def generate_question():
    """This function generates a new maths question, and it's answer. Each operand has a maximum magnitude, nor
    can the total magnitude of the operands cannot exceed a maximum.

    :return question: Returns a question answer in the form (operand 1, operand 2, operation, answer)
    """

    # Randomly generate the operator
    operator_index = random.randint(0, 2)

    # If the operator is multiplication
    if operator_index == 0:

        # Set the operator string
        operator = '×'

        # Find the magnitude of each operand
        operand_1_magnitude = random.randint(1, 2)
        operand_2_magnitude = 4 - operand_1_magnitude

        # Randomly generate the operands
        operand_1 = random.randrange(10 ** (operand_1_magnitude-1), 10 ** operand_1_magnitude)
        operand_2 = random.randrange(10 ** (operand_2_magnitude-1), 10 ** operand_2_magnitude)

        # Randomly swap the two operators
        if random.random() > 0.5:
            operand = operand_1
            operand_1 = operand_2
            operand_2 = operand

        # Find the answer to the question
        answer = operand_1 * operand_2

    elif operator_index == 1:

        # Set the operator string
        operator = '+'

        # Randomly generate the operands
        operand_1 = random.randint(2, random.randrange(100, 1000))
        operand_2 = random.randint(2, random.randrange(100, 1000))

        # Find the answer to the question
        answer = operand_1 + operand_2

    else:

        # Set the operator string
        operator = '-'

        # Randomly generate the operands
        operand_1 = random.randint(2, random.randrange(100, 1000))
        operand_2 = random.randint(2, random.randrange(100, 1000))

        # Find the answer to the question
        answer = operand_1 - operand_2

    # Return the question
    return operand_1, operand_2, operator, str(answer)


def run_maths():
    """This function is a loop which runs a number of times per second, given by the FPS value in display."""

    # A list of data samples taken by the headset
    data = []

    # The current time left to answer questions
    time = MAX_TIME

    # Generate a starting maths question
    question = generate_question()

    # The answer to the question
    answer = ""

    # The number of correct responses
    correct = 0

    # Tick the clock once to remove delays
    clock.tick(FPS)

    # Run the game until it is quit
    while True:

        # Wait until the FPS time has passed.
        dt = clock.tick(FPS)

        # Find the current time
        time -= dt

        # Generate a new question if the current one is done
        if question is None: question = generate_question()

        # region Events

        # Check for events
        for event in pg.event.get():

            # If the game is quit, end the game
            if event.type == pg.QUIT:
                return True

            # Check for keyboard presses
            if event.type == pg.KEYDOWN:

                # End the game if the escape key is pressed
                if event.key == pg.K_ESCAPE:
                    return True

                # region Answer Writing

                # Check if the event is a digit
                if event.unicode.isdigit() and len(answer) < 5:
                    answer += event.unicode

                # Check if the answer is a minus sign
                if event.key == pg.K_MINUS:

                    # If the string has a minus, remove it
                    if len(answer) > 0 and answer[0] == '-': answer = answer[1:]

                    # Otherwise, add it
                    else: answer = "-" + answer

                # Check if the event is a backspace-
                if event.key == pg.K_BACKSPACE and len(answer) > 0:
                    answer = answer[:-1]

                # Check if the event is enter
                if event.key == pg.K_RETURN:

                    # If the answer is correct, increment the correct count
                    if answer == str(question[3]):
                        correct += 1

                    # Reset the answer and generate a new question
                    answer = ''
                    question = generate_question()

                # endregion Answer Writing

        #endregion Events

        # region Drawing

        # Draw the background
        display.fill(color.WHITE)

        # Draw the time
        time_surface = fonts.HUD.render('Time: ' + str(math.ceil(time/1000)), False, color.BLACK)
        display.blit(time_surface, (DISPLAY_WIDTH/2 - time_surface.get_width()/2, 32))

        # Draw the question
        question_surface = fonts.MATH.render(str(question[0]) + " " + question[2] + " " + str(question[1]),
                                             False, color.BLACK)
        display.blit(question_surface, (DISPLAY_WIDTH/2 - question_surface.get_width()/2,
                                        DISPLAY_HEIGHT/3 - question_surface.get_height()/2))

        # Draw the answer box
        pg.draw.rect(display, color.BLACK, (DISPLAY_WIDTH * (5/12), DISPLAY_HEIGHT/2 - 64, DISPLAY_WIDTH/6, 128), 2)

        # Draw the current answer
        answer_surface = fonts.MATH.render("".join(str(i) for i in answer), False, color.BLACK)
        display.blit(answer_surface, (DISPLAY_WIDTH/2 - answer_surface.get_width()/2,
                                      DISPLAY_HEIGHT/2 - answer_surface.get_height()/2))

        # Draw the current answer
        answer_surface = fonts.HUD.render(str(correct), False, color.BLACK)
        display.blit(answer_surface, (DISPLAY_WIDTH - answer_surface.get_width() - 32, 32))

        # endregion Drawing

        # Update the window
        pg.display.update()

        # If the timer is at 0, break the loop
        if time <= 0:

            # Exit the maths portion
            return False

