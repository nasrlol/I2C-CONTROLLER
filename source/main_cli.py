import hardware_driver as lcd  # Simulated library for LCD hardware control
import features as fe  # Simulated library for app-specific features
import curses  # Library for terminal UI
import sys
import time

# Initialize feature and LCD objects
F = fe.feat()  # Instance of the feature class
L = lcd.LCD()  # Instance of the LCD driver class

# Define a list of actions, linking functions from the `features` library
actions = [
    F.temperature,  # Function to display temperature
    F.save_notes,  # Function to save notes
    F.recognize_speech,  # Function to recognize speech
    F.pomodoro,  # Function for the Pomodoro timer
    F.display_uptime,  # Function to display system uptime
    F.custom_greeting,  # Function for a custom greeting
    F.command_center,  # Function to launch a command center
]


# Menu drawing function
def draw_menu(stdscr):
    """
    This function creates a text-based menu using curses.
    """
    # Turn off the cursor and enable keypad input for better UX
    curses.curs_set(0)
    stdscr.keypad(True)

    # Define button names
    buttons = [
        "Display Temperature",
        "Save Notes",
        "Recognize Speech",
        "Pomodoro Timer",
        "Show Uptime",
        "Custom Greeting",
        "Command Center",
    ]

    current_selection = 0  # Track which button is selected

    while True:
        # Clear the screen before redrawing
        stdscr.clear()

        # Display buttons with proper alignment
        h, w = stdscr.getmaxyx()  # Get screen height and width
        for idx, button in enumerate(buttons):
            x = w // 2 - len(button) // 2  # Center-align text horizontally
            y = h // 2 - len(buttons) // 2 + idx  # Stack buttons vertically

            # Highlight the currently selected button
            if idx == current_selection:
                stdscr.attron(curses.A_REVERSE)  # Reverse color for highlight
                stdscr.addstr(y, x, button)
                stdscr.attroff(curses.A_REVERSE)  # Turn off highlight
            else:
                stdscr.addstr(y, x, button)

        stdscr.refresh()  # Refresh the screen to show changes

        # Wait for user input
        key = stdscr.getch()

        # Handle up arrow key to move selection up
        if key == curses.KEY_UP and current_selection > 0:
            current_selection -= 1

        # Handle down arrow key to move selection down
        elif key == curses.KEY_DOWN and current_selection < len(buttons) - 1:
            current_selection += 1

        # Handle Enter key to execute the selected action
        elif key == curses.KEY_ENTER or key in [10, 13]:
            stdscr.clear()  # Clear the screen
            try:
                # Execute the action corresponding to the selected button
                result = actions[current_selection]()
                if isinstance(result, str):  # If action returns a string, display it
                    stdscr.addstr(h // 2, w // 2 - len(result) // 2, result)
                else:  # For non-string results, display a generic message
                    stdscr.addstr(h // 2, w // 2 - 10, "Action executed successfully.")
            except Exception as e:
                # Handle any errors gracefully and display them
                error_message = f"Error: {e}"
                stdscr.addstr(h // 2, w // 2 - len(error_message) // 2, error_message)

            # Prompt user to return to the menu
            stdscr.addstr(h // 2 + 2, w // 2 - 10, "Press any key to return.")
            stdscr.refresh()
            stdscr.getch()  # Wait for any key press to return to the menu

        # Handle Escape key to exit the application
        elif key == 27:
            break  # Exit the while loop and terminate the program


def input_handling():
    while True:
        key = stdscr.getkey()
        stdcr.addstr(f"key: {key}")
        stdcr.refresh()
        stdcr.getch()


def main():
    """
    The main function wraps the curses functionality and runs the application.
    """
    curses.wrapper(draw_menu)  # Handles initialization and cleanup of curses


# Run the application if this script is executed directly
if __name__ == "__main__":
    main()
