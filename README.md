# Status

## Working pages: 

login 

master control

active player

inactive player.  

## Working Functions:

reset

new deal

first bet - Proper control passing, proper hands shown, properactive player status, no control for the inactive player.  One small bug,: in the last round of checks, the display shows an object.  Need to trap for a string and display.


From the command line, run test program with:

## python fourth_deal.py



## login

Simple as it sounds.  access by pic-a-wheel-root/login

## master_control:

This page contains a list of actions: reset table, new deal, flips 1-3, and betting rounds.  The flips are working correctly, the new deal works correctly, but must be preceded by a reset table/submit.  A test needs to be run on whether you must refresh your page before the deal (active player only, inactive players reload automatically).  I have seen this page generate no errors.  In order to access this page, you must be logged in as either Bornstein or Clyde.  This may eventually change to be a dealer page, but for now to keep chaos to a minimum, anyone else gets an appropriate error message.

When logged in, access as pic-a-wheel-root/master_control

## active player:

The active and inactive screens are essentially the same, except that the inactive page has no controls for folding/keeping or betting.  Both pages are accessed by pointing your browser at the pic-a-wheel-root/full_table.  You are allowed to act if it is your turn.  This page is partially working.  For testing, active player= Bornstein.  Keep/Fold decisions are recorded correctly and passed back to the server.  Additionally, the betting is reported correctly to the server, but, nothing is done with it yet.


## inactive player:
See above.  Was working to show inactive players the hand status on an updating basis, but a lot of changes have been made since that was true.  Current status unknow, and will need to be rewritten to reflect the changes to active players page.

# Boilerplate
# pic_a_wheel
Pic-A-Wheel is the name of a particular game of poker that has a set of common cards arranged in multiple flips, usually arranged in groups of 3-2-2, but that is a dealer's choice decision.

This app is designed to automate that game, and provide a simple user interface.  
