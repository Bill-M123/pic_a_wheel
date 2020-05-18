# Status

Currently Running tenth_deal.py:  This has the following fixes:

Fixes:  

Remove player working correctly.

Scoring on a hand basis working correctly.

Cummulative scoring working correctly.

Declare list dynamic and displayed for all to see.

A new message/holding page for players in waiting room.

requirments: unchanged

mastercontrols changes.  None.


## Working pages:

login/login_wait_state

master control (including add and remove players)

active player

inactive player.

declare/declare_wait_state

hand show_down

## Working Functions:

reset

accept and seat new players

remove players

new deal

first bet - Proper control passing, proper hands shown, properactive player status, no control for the inactive player.  One small bug,: in the last round of checks, the display shows an object.  Need to trap for a string and display.

All flip_controls

Declare

master_control:  everything but evaluate hands


From the command line, run test program with:

## python tenth_deal.py



## login

Simple as it sounds.  access by pic-a-wheel-root/login

## master_control:

This page contains a list of actions: reset table, new deal, flips 1-3, declare and betting rounds.   It also contains some housekeeping functions, specifically the ability to dynamically add players and remove them.  The page is not currently set to autoupdate, but on any refresh (and any other action) it will check for players logged in and add them to the waiting list (appears only when there are players in queue.)

Also note:  defaults for players_to_remove do not reset automatically, and currently the user is responsible for making sure that the player_to_remove selection and the verification box are always in the right state, otherwise, it is possible to generate unwanted results.

I have seen this page generate no errors, but order of actions is critical, and an incorrect sequence can generate errors.  In order to access this page, you must be logged in as either Bornstein or Clyde.  This may eventually change to be a dealer page, but for now to keep chaos to a minimum, anyone else gets an appropriate error message.

When logged in, access as pic-a-wheel-root/master_control

## active player:

The active and inactive screens are essentially the same, except that the inactive page has no controls for folding/keeping or betting.  Both pages are accessed by pointing your browser at the pic-a-wheel-root/full_table.  You are allowed to act if it is your turn.  This page is working.  Additionally, the betting is reported correctly to the server, but, nothing is done with it yet.


## inactive player:
See above.  

# Boilerplate
# pic_a_wheel
Pic-A-Wheel is the name of a particular game of poker that has a set of common cards arranged in multiple flips, usually arranged in groups of 3-2-2, but that is a dealer's choice decision.

This app is designed to automate that game, and provide a simple user interface.  
