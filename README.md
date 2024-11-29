# I2C

An application to control an I2C display on RPI.
This application should represent a multi-use software with features ranging from a bus line analyser, bus delay analiser, an generative AI command line, weather reports, note's saving and much more.

This is a starter project with the goal of expanded everything later on to let's say an e-ink display or small LCD.
After some tinkering with GTK i decided to switch qt for the gui application.

The program is Multi-platform and even supports a web-console

MAIN USE OF THE PROGRAM :
the main feature of the program is the ability to control and I2C display really extensivly and be abel to do alot of things with it

CURRENT FEATURES ->

-   Weather display
-   Random generated greeting quote ( still dont know what to really do about that, could add a joke of the day system or something like that)
-   A button powered button pomodore timer
-   Some sort of clock mechanisme that adds an alarm clock, timer and stopwatch
-   System monitor dashbord ( cpu , ram , disk , temp , ... )
-   Speech command center
-   Generative AI model that uses meta's llama
-   Current playing audio
-   Voice based notes
-   To do list integration based on the personal calender

A nice idea is to make it somehting easily installable and configurable in the future without to much tinkering need
At the moment the software only supports a CLI version.

Support wil be kept to Linux and MacOS for now.
