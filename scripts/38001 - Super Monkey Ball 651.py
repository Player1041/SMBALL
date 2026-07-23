from pycheevos.core.helpers import *  
from pycheevos.core.constants import *
from pycheevos.core.condition import Condition
from pycheevos.models.rich_presence import RichPresence
from pycheevos.models.leaderboard import Leaderboard
from pycheevos.models.set import AchievementSet
from pycheevos.models.achievement import Achievement


import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from helpers import *
from helpers.achievements import *
from helpers.achievements.custom import *
from profiles.addresses import get_profile
from pathlib import Path
from typing import Union

mySet = AchievementSet(game_id=38001, title="Super Monkey Ball 651")
platform = "GameCube"

profile = get_profile("651")


story_progression = {
    0: ("World 1 Story",                "Clear World 1 in Story Mode",  5),
    1: ("World 2 Story",                "Clear World 2 in Story Mode",  5),
    2: ("World 3 Story",                "Clear World 3 in Story Mode",  10),
    3: ("World 4 Story",                "Clear World 4 in Story Mode",  10),
    4: ("World 5 Story",                "Clear World 5 in Story Mode",  10),
    5: ("Vaporwave Rave",                "Clear World 6 in Story Mode",  10),
    6: ("Arctic Expedition",                "Clear World 7 in Story Mode",  10),
    7: ("Squeaky Clean",                "Clear World 8 in Story Mode",  25),
    8: ("Molten Madness",                "Clear World 9 in Story Mode",  25),
    9: ("Serene Insanity",                "Clear World 10 in Story Mode", 50),

}

extras = {
    "999bananas": ("Plus 348",              "Collect 999 bananas in Story Mode", 10),
    "colourful":  ("RGB Monkey",            "Enter every green and red goal in a single session", 25)
}

ils = {
    "1-2":   ("1-2 IL",         "Clear \"1-2 Paper\" with a stage score of 12,000 points or more"                                                                      ,4 ),
    "1-3":   ("1-3 IL",         "Clear \"1-3 Meadow\" in 6 seconds or less"                                                                                            ,3 ),
    "1-5":   ("1-5 IL",         "Clear \"1-5 Screen Tearing\" with a stage score of 14,000 points or more"                                                             ,10 ),
    "1-6":   ("1-6 IL",         "Clear \"1-6 Restless\" with a stage score of 13,000 points or more"                                                                   ,5 ),
    "1-8":   ("1-8 IL",         "Clear \"1-8 Rerun\" in 10 seconds or less"                                                                                            ,5 ),
    "1-10":  ("1-10 IL",        "Clear \"1-10 Ring Attack\" with at least 29 bananas collected"                                                                        ,5 ),
    "2-1":  ("2-1  IL",        "Clear \"2-1 Jump Simulator\" with a stage score of 13,000 or more"                                                                    ,4 ),
    "2-2":  ("2-2  IL",        "Clear \"2-2 Capsule\" in 8 seconds or less"                                                                                           ,4 ),
    "2-4":  ("2-4  IL",        "Clear \"2-4 Silly Slalom\" with a stage score of 13,500 or more"                                                                      ,5 ),
    "2-5":  ("2-5  IL",        "Clear \"2-5 Stencil\" with a stage score of 14,000 points or more"                                                                    ,5 ),
    "2-7":  ("2-7  IL",        "Clear \"2-7 Fun House\" with at least 5 banana bunches collected"                                                                     ,10 ),
    "2-10":  ("2-10 IL",        "Clear \"2-10 Crystal Cave Museum\" by taking both thin paths"                                                                         ,4 ),
    "3-1":  ("3-1  IL",        "Clear \"3-1 Commitment\" with at least one banana bunch collected"                                                                    ,3 ),
    "3-3":  ("3-3  IL",        "Clear \"3-3 Corner Block\" with every banana collected"                                                                               ,5 ),
    "3-4":  ("3-4  IL",        "Clear \"3-4 Saw\" in 8 seconds or less"                                                                                               ,4 ),
    "3-5":  ("3-5  IL",        "Clear \"3-5 Stamps\" with all 3 banana bunches collected"                                                                             ,5 ),
    "3-6":  ("3-6  IL",        "Clear \"3-6 Slicer\" without going to the left side of the level and without pausing"                                                 ,10 ),
    "3-7":  ("3-7  IL",        "Clear \"3-7 Gyration\" with all 5 banana bunches collected"                                                                           ,5 ),
    "3-8":  ("3-8  IL",        "Clear \"3-8 Waves\" with a stage score of 36,000 points or more"                                                                      ,5 ),
    "3-10":  ("3-10 IL",        "Clear \"3-10 Descent\" in less than 10 seconds"                                                                                       ,5 ),
    "4-2":  ("4-2  IL",        "Clear \"4-2 Measuring Spoons\" in 6 seconds or less"                                                                                  ,4 ),
    "4-3":   ("4-3 IL",         "Enter the green goal in \"4-3 Launcher\" without pressing the switch"                                                                 ,5 ),
    "4-4":  ("4-4  IL",        "Clear \"4-4 Feedback Loop\" with all 5 banana bunches collected"                                                                      ,5 ),
    "4-6":  ("4-6  IL",        "Clear \"4-6 Collectathon\" by only pressing 2 switches"                                                                               ,4 ),
    "4-7":  ("4-7  IL",        "Clear \"4-7 Scoop\" while going over 100mph"                                                                                          ,5 ),
    "4-8":  ("4-8  IL",        "Clear \"4-8 Tail\" without pressing the pause switch"                                                                                 ,10 ),
    "4-9":   ("4-9 IL",         "Enter the red goal in \"4-9 Valves\" without pressing a switch"                                                                       ,10 ),
    "4-10": ("4-10 IL",        "Clear \"4-10 Waveform\" in 4 seconds or less"                                                                                         ,4 ),
    "5-2":   ("5-2 IL",         "Clear \"5-2 Railroad\" with a stage score of 14,500 points or more"                                                                   ,5 ),
    "5-3":   ("5-3 IL",         "Clear \"5-3 Raft\" with every banana collected"                                                                                       ,5 ),
    "5-4":   ("5-4 IL",         "Find the secret entrance to the cage and Clear \"5-4 Area\""                                                                          ,4 ),
    "5-5":   ("5-5 IL",         "Clear \"5-5 Custom Road\" by only pressing one switch"                                                                                ,4 ),
    "5-7":   ("5-7 IL",         "Clear \"5-7 Changeover\" with a stage score of 35,000 points or more"                                                                 ,10 ),
    "5-8":   ("5-8 IL",         "Clear \"5-8 Ribbon\" with every banana collected"                                                                                     ,4 ),
    "5-9":   ("5-9 IL",         "Clear \"5-9 Quadripartite\" with at least 80 bananas collected"                                                                       ,10 ),
    "5-10":  ("5-10 IL",        "Clear \"5-10 Tides\" in 7 seconds or less"                                                                                            ,5 ),
    "6-2":   ("6-2 IL",         "Clear \"6-2 Timing\" with all 4 banana bunches collected"                                                                             ,5 ),
    "6-3":   ("6-3 IL",         "Clear \"6-3 Mystery Box\" in 6.5 seconds or less"                                                                                     ,4 ),
    "6-5":   ("6-5 IL",         "Clear \"6-5 Steps\" with both banana bunches collected"                                                                               ,10 ),
    "6-8":   ("6-8 IL",         "Clear \"6-8 Antigravity\" while going over 200mph"                                                                                    ,5 ),
    "6-9":   ("6-9 IL",         "Clear \"6-9 Clothesline\" with every banana collected"                                                                                ,5 ),
    "6-10":  ("6-10 IL",        "Clear \"6-10 Architect\" without pressing any switches"                                                                               ,10 ),
    "7-2":   ("7-2 IL",         "Clear \"7-2 Valleys\" with every banana collected"                                                                                    ,5 ),
    "7-5":   ("7-5 IL",         "Clear \"7-5 Trap Doors\" with all 4 banana bunches collected"                                                                         ,10 ),
    "7-6":   ("7-6 IL",         "Clear \"7-6 Iced Hive\" in 4 seconds or less"                                                                                         ,5 ),
    "7-9":   ("7-9 IL",         "Clear \"7-9 Pull\" without collecting any bananas"                                                                                    ,3 ),
    "7-10":  ("7-10 IL",        "Clear \"7-10 Mini Map Assist\" by only using a fully zoomed out mini map"                                                             ,4 ),
    "8-1":   ("8-1 IL",         "Clear \"8-1 Axis Maze\" with a stage score of 10,500 points or more"                                                                  ,10 ),
    "8-2":   ("8-2 IL",         "Clear \"8-2 Warp Pipes\" with every banana collected"                                                                                 ,5 ),
    "8-4":   ("8-4 IL",         "Enter one of the goals in a corner in \"8-4 Overcorrection\""                                                                         ,10 ),
    "8-6":   ("8-6 IL",         "Clear \"8-6 Jumpscare\" after taking the top path"                                                                                    ,5 ),
    "8-8":   ("8-8 IL",         "Clear \"8-8 I-Beams\" with all 18 banana bunches collected and without pausing"                                                       ,25 ),
    "8-9":   ("8-9 IL",         "Clear \"8-9 Warp Heights\" without entering a wormhole more than twice"                                                               ,4 ),
    "8-10":  ("8-10 IL",        "Clear \"8-10 Checker Roll\" in 8 seconds or less"                                                                                     ,10 ),
    "9-2":   ("9-2 IL",         "Clear \"9-2 Distortion\" in 12 seconds or less"                                                                                       ,5 ),
    "9-3":   ("9-3 IL",         "Clear \"9-3 Picture Frames\" with all 5 banana bunches collected"                                                                     ,5 ),
    "9-4":   ("9-4 IL",         "Clear \"9-4 Network\" with every banana collected and without pausing"                                                                ,25 ),
    "9-5":   ("9-5 IL",         "Clear \"9-5 Lava River\" in 8 seconds or less"                                                                                        ,10 ),
    "9-7":   ("9-7 IL",         "Clear \"9-7 Ladder\" with every banana collected and without pausing"                                                                 ,10 ),
    "9-9":   ("9-9 IL",         "Clear \"9-9 Platformer\" in 21 seconds or less"                                                                                       ,10 ),
    "10-1":  ("10-1 IL",        "Clear \"10-1 Sleekhopper HD\" before the announcer says \"Hurry Up!\" without pausing"                                                ,10 ),
    "10-2":  ("10-2 IL",        "Clear \"10-2 Smile\" with at least 25 banana bunches collected and without pausing"                                                   ,25 ),
    "10-4":  ("10-4 IL",        "Balance atop the center bird while its wings are folded inwards and Clear \"10-4 Birds\" without pausing"                             ,25 ),
    "10-6":  ("10-6 IL",        "Clear \"10-6 Frame Windows\" without skipping around the wall"                                                                        ,10 ),
    "10-7":  ("10-7 IL",        "Clear \"10-7 Desync\" by pressing every switch"                                                                                       ,5 ),
    "10-8":  ("10-8 IL",        "Clear \"10-8 Exam-651\" without riding the lower wire between the second and the fourth yellow platform and without pausing"          ,10 ),
    "10-10": ("10-10 IL",       "Clear \"10-10 Antlers\" in 20 seconds or less without pausing"                                                                        ,25 ),
}

profile.LEVEL_TABLE = {
    (1,  1):  (0x0C9, "1-1 NEST", 60),
    (1,  2):  (0x0CA, "1-2 PAPER", 60),
    (1,  3):  (0x0CB, "1-3 MEADOW", 60),
    (1,  4):  (0x0CC, "1-4 CONTAINER", 60),
    (1,  5):  (0x001, "1-5 SCREEN TEARING", 60),
    (1,  6):  (0x002, "1-6 RESTLESS", 60),
    (1,  7):  (0x003, "1-7 CHILLS", 60),
    (1,  8):  (0x004, "1-8 RERUN", 60),
    (1,  9):  (0x005, "1-9 KNOT", 60),
    (1, 10):  (0x006, "1-10 RING ATTACK", 60),
    (2,  1):  (0x007, "2-1 JUMP SIMULATIOR", 60),
    (2,  2):  (0x008, "2-2 CAPSULE", 60),
    (2,  3):  (0x009, "2-3 BUNKERS", 60),
    (2,  4):  (0x00A, "2-4 SILLY SLALOM", 60),
    (2,  5):  (0x00B, "2-5 STENCIL", 60),
    (2,  6):  (0x00C, "2-6 DOME", 60),
    (2,  7):  (0x00D, "2-7 FUN HOUSE", 60),
    (2,  8):  (0x00E, "2-8 BEADS", 60),
    (2,  9):  (0xFFF, "2-9 PEAKING", 60),
    (2, 10):  (0x010, "2-10 CRYSTAL CAVE MUSEUM", 60),
    (3,  1):  (0x0E7, "3-1 COMMITMENT", 60),
    (3,  2):  (0x0E8, "3-2 BLEACHERS", 60),
    (3,  3):  (0x0E9, "3-3 CORNER BLOCK", 60),
    (3,  4):  (0x0EA, "3-4 SAW", 60),
    (3,  5):  (0x0EB, "3-5 STAMPS", 60),
    (3,  6):  (0x0EC, "3-6 SLICER", 60),
    (3,  7):  (0x0ED, "3-7 GYRATION", 60),
    (3,  8):  (0x0EE, "3-8 WAVES", 60),
    (3,  9):  (0x0EF, "3-9 HIDDEN ROOM", 60),
    (3, 10):  (0x011, "3-10 DESCENT", 60),
    (4,  1):  (0x012, "4-1 CROSSHAIR", 60),
    (4,  2):  (0x013, "4-2 MEASURING SPOONS", 60),
    (4,  3):  (0x014, "4-3 LAUNCHER", 60),
    (4,  4):  (0x015, "4-4 FEEDBACK LOOP", 60),
    (4,  5):  (0x016, "4-5 TRYPOPHOBIA", 60),
    (4,  6):  (0x017, "4-6 COLLECTATHON", 60),
    (4,  7):  (0x018, "4-7 SCOOP", 60),
    (4,  8):  (0x019, "4-8 TAIL", 60),
    (4,  9):  (0x01A, "4-9 VALVES", 60),
    (4, 10):  (0x01B, "4-10 WAVEFORM", 60),
    (5,  1):  (0x01C, "5-1 STAIRCASE", 60),
    (5,  2):  (0x01D, "5-2 RAILROAD", 60),
    (5,  3):  (0x01E, "5-3 RAFT", 30),
    (5,  4):  (0x01F, "5-4 AREA", 60),
    (5,  5):  (0x020, "5-5 CUSTOM ROAD", 60),
    (5,  6):  (0x021, "5-6 REPELLENT", 60),
    (5,  7):  (0x022, "5-7 CHANGEOVER", 60),
    (5,  8):  (0x023, "5-8 RIBBON", 60),
    (5,  9):  (0x024, "5-9 QUADRIPARTITE", 60),
    (5, 10):  (0x025, "5-10 TIDES", 60),
    (6,  1):  (0x026, "6-1 WORMHOLE PRACTICE", 60),
    (6,  2):  (0x027, "6-2 TIMING", 60),
    (6,  3):  (0x028, "6-3 MYSTERY BOX", 60),
    (6,  4):  (0x029, "6-4 RETURN", 60),
    (6,  5):  (0x02A, "6-5 STEPS", 60),
    (6,  6):  (0x02B, "6-6 DROP IN", 60),
    (6,  7):  (0x02C, "6-7 VOLTE-FACE", 60),
    (6,  8):  (0x02D, "6-8 ANTIGRAVITY", 60),
    (6,  9):  (0x02E, "6-9 CLOTHESLINE", 60),
    (6, 10):  (0x02F, "6-10 ARCHITECT", 60),
    (7,  1):  (0x119, "7-1 CARDS", 60),
    (7,  2):  (0x11A, "7-2 VALLEYS", 60),
    (7,  3):  (0x11B, "7-3 GRAVITY JUMPER", 60),
    (7,  4):  (0x11C, "7-4 REFLECTION", 60),
    (7,  5):  (0x11D, "7-5 TRAP DOORS", 60),
    (7,  6):  (0x11E, "7-6 ICED HIVE", 60),
    (7,  7):  (0x11F, "7-7 DEVICE", 60),
    (7,  8):  (0x120, "7-8 POUR", 60),
    (7,  9):  (0x121, "7-9 PULL", 60),
    (7, 10):  (0x030, "7-10 MINI MAP ASSIST", 60),
    (8,  1):  (0x031, "8-1 AXIS MAZE", 60),
    (8,  2):  (0x032, "8-2 WARP PIPES", 60),
    (8,  3):  (0x033, "8-3 TURN", 60),
    (8,  4):  (0xFFF, "8-4 OVERCORRECTION", 60),
    (8,  5):  (0x035, "8-5 SEWING", 60),
    (8,  6):  (0x036, "8-6 JUMPSCARE", 60),
    (8,  7):  (0x037, "8-7 OSCILLATING OVERPASS", 60),
    (8,  8):  (0x038, "8-8 I-BEAMS", 60),
    (8,  9):  (0x039, "8-9 WARP HEIGHTS", 60),
    (8, 10):  (0x03A, "8-10 CHECKER ROLL", 60),
    (9,  1):  (0x03B, "9-1 ELEVATORS", 60),
    (9,  2):  (0x03C, "9-2 DISTORTION", 60),
    (9,  3):  (0x03D, "9-3 PICTURE FRAMES", 60),
    (9,  4):  (0x03E, "9-4 NETWORK", 60),
    (9,  5):  (0x03F, "9-5 LAVA RIVER", 60),
    (9,  6):  (0x040, "9-6 STREAM", 60),
    (9,  7):  (0x041, "9-7 LADDER", 60),
    (9,  8):  (0x042, "9-8 PACING", 60),
    (9,  9):  (0x043, "9-9 PLATFORMER", 60),
    (9, 10):  (0x044, "9-10 TECHNIQUE", 60),
    (10,  1): (0x155, "10-1 SLEEKHOPPER HD", 60),
    (10,  2): (0x156, "10-2 SMILE", 60),
    (10,  3): (0x157, "10-3 CRANK", 60),
    (10,  4): (0x158, "10-4 BIRDS", 60),
    (10,  5): (0x159, "10-5 UNLOCK", 60),
    (10,  6): (0x15A, "10-6 FRAME WINDOWS", 60),
    (10,  7): (0x15B, "10-7 DESYNC", 60),
    (10,  8): (0xFFF, "10-8 EXAM-651", 60),
    (10,  9): (0x15D, "10-9 STRESS TEST", 60),
    (10, 10): (0x15E, "10-10 ANTLERS", 60),
    ("StaffRoll", 1): (0xC5, "Staff Roll", 60)
}


# Story Mode
for world, (title, description, points) in story_progression.items():
    ach = Achievement(title, description, points)
    ach.add_core(story_world_clear(profile, world))
    mySet.add_achievement(ach)

# Extras
for x, (title, description, points) in extras.items():
    ach = Achievement(title, description, points)
    match x:
        case "999bananas":
            ach.add_core(collect_x_bananas_story(profile, 999))
        case "colourful":
            logic = [
                *mode_check(profile, "non-challenge"),
                clear_level_type(profile, 2, 7, "GREEN"),
                clear_level_type(profile, 3, 1, "GREEN"),
                clear_level_type(profile, 3, 7, "GREEN"),
                clear_level_type(profile, 3, 8, "GREEN"),
                clear_level_type(profile, 4, 3, "GREEN"),
                clear_level_type(profile, 4, 4, "GREEN"),
                clear_level_type(profile, 4, 9, "RED"),
                clear_level_type(profile, 5, 5, "GREEN"),
                clear_level_type(profile, 5, 5, "RED"),
                clear_level_type(profile, 5, 7, "GREEN"),
                clear_level_type(profile, 6, 1, "GREEN"),
                clear_level_type(profile, 6, 3, "GREEN"),
                clear_level_type(profile, 6, 6, "GREEN"),
                clear_level_type(profile, 6, 9, "GREEN"),
                clear_level_type(profile, 8, 2, "GREEN"),
                clear_level_type(profile, 8, 9, "GREEN"),
                clear_level_type(profile, 8, 9, "RED"),
                clear_level_type(profile, 9, 6, "RED"),
                measured(value(0x00) == value(0x01)).with_hits(18)
            ]

# ILs

for x, (title, description, points) in ils.items():
    ach = Achievement(title, description, points)
    match x:
        case "1-2":                         # Clear 1-2 Paper with a stage score of 12,000 points or more
            ach.add_core(score_clear(profile, "non-challenge", 1, 2, 12000))
        case "1-3":                         # Clear 1-3 Meadow in 6 seconds or less
            ach.add_core(timed(profile, "non-challenge", 1, 3, 60, 6))
        case "1-5":                         # Clear 1-5 Screen Tearing with a stage score of 14,000 points or more
            pass
        case "1-6":                         # Clear 1-6 Restless with a stage score of 13,000 points or more
            pass
        case "1-8":                         # Clear 1-8 Rerun in 10 seconds or less
            pass
        case "1-10":                        # Clear 1-10 Ring Attack with at least 29 bananas collected
            pass
        case "2-1":                         # Clear 2-1 Jump Simulator with a stage score of 13,000 or more
            pass
        case "2-2":                         # Clear 2-2 Capsule in 8 seconds or less
            pass
        case "2-4":                         # Clear 2-4 Silly Slalom with a stage score of 13,500 or more
            pass
        case "2-5":                         # Clear 2-5 Stencil with a stage score of 14,000 points or more
            pass
        case "2-7":                         # Clear 2-7 Fun House with at least 5 banana bunches collected
            pass
        case "2-10":                        # Clear 2-10 Crystal Cave Museum by taking both thin paths
            pass
        case "3-1":                         # Clear 3-1 Commitment with at least one banana bunch collected
            pass
        case "3-3":                         # Clear 3-3 Corner Block with every banana collected
            pass
        case "3-4":                         # Clear 3-4 Saw in 8 seconds or less
            pass
        case "3-5":                         # Clear 3-5 Stamps with all 3 banana bunches collected
            pass
        case "3-6":                         # Clear 3-6 Slicer without going to the left side of the level and without pausing
            pass
        case "3-7":                         # Clear 3-7 Gyration with all 5 banana bunches collected
            pass
        case "3-8":                         # Clear 3-8 Waves with a stage score of 36,000 points or more
            pass
        case "3-10":                        # Clear 3-10 Descent in less than 10 seconds
            pass
        case "4-2":                         # Clear 4-2 Measuring Spoons in 6 seconds or less
            pass
        case "4-3":                         # Enter the green goal in 4-3 Launcher without pressing the switch
            pass
        case "4-4":                         # Clear 4-4 Feedback Loop with all 5 banana bunches collected
            pass
        case "4-6":                         # Clear 4-6 Collectathon by only pressing 2 switches
            pass
        case "4-7":                         # Clear 4-7 Scoop while going over 100mph
            pass
        case "4-8":                         # Clear 4-8 Tail without pressing the pause switch
            pass
        case "4-9":                         # Enter the red goal in 4-9 Valves without pressing a switch
            pass
        case "4-10":                        # Clear 4-10 Waveform in 4 seconds or less
            pass
        case "5-2":                         # Clear 5-2 Railroad with a stage score of 14,500 points or more
            pass
        case "5-3":                         # Clear 5-3 Raft with every banana collected
            pass
        case "5-4":                         # Find the secret entrance to the cage and clear 5-4 Area
            pass
        case "5-5":                         # Clear 5-5 Custom Road by only pressing one switch
            pass
        case "5-7":                         # Clear 5-7 Changeover with a stage score of 35,000 points or more
            pass
        case "5-8":                         # Clear 5-8 Ribbon with every banana collected
            pass
        case "5-9":                         # Clear 5-9 Quadripartite with at least 80 bananas collected
            pass
        case "5-10":                        # Clear 5-10 Tides in 7 seconds or less
            pass
        case "6-2":                         # Clear 6-2 Timing with all 4 banana bunches collected
            pass
        case "6-3":                         # Clear 6-3 Mystery Box in 6.5 seconds or less
            pass
        case "6-5":                         # Clear 6-5 Steps with both banana bunches collected
            pass
        case "6-8":                         # Clear 6-8 Antigravity while going over 200mph
            pass
        case "6-9":                         # Clear 6-9 Clothesline with every banana collected
            pass
        case "6-10":                        # Clear 6-10 Architect without pressing any switches
            pass
        case "7-2":                         # Clear 7-2 Valleys with every banana collected
            pass
        case "7-5":                         # Clear 7-5 Trap Doors with all 4 banana bunches collected
            pass
        case "7-6":                         # Clear 7-6 Iced Hive in 4 seconds or less
            pass
        case "7-9":                         # Clear 7-9 Pull without collecting any bananas
            pass
        case "7-10":                        # Clear 7-10 Mini Map Assist by only using a fully zoomed out mini map
            pass
        case "8-1":                         # Clear 8-1 Axis Maze with a stage score of 10,500 points or more
            pass
        case "8-2":                         # Clear 8-2 Warp Pipes with every banana collected
            pass
        case "8-4":                         # Enter one of the goals in a corner in 8-4 Overcorrection
            pass
        case "8-6":                         # Clear 8-6 Jumpscare after taking the top path
            pass
        case "8-8":                         # Clear 8-8 I-Beams with all 18 banana bunches collected and without pausing
            pass
        case "8-9":                         # Clear 8-9 Warp Heights without entering a wormhole more than twice
            pass
        case "8-10":                        # Clear 8-10 Checker Roll in 8 seconds or less
            pass
        case "9-2":                         # Clear 9-2 Distortion in 12 seconds or less
            pass
        case "9-3":                         # Clear 9-3 Picture Frames with all 5 banana bunches collected
            pass
        case "9-4":                         # Clear 9-4 Network with every banana collected and without pausing
            pass
        case "9-5":                         # Clear 9-5 Lava River in 8 seconds or less
            pass
        case "9-7":                         # Clear 9-7 Ladder with every banana collected and without pausing
            pass
        case "9-9":                         # Clear 9-9 Platformer in 21 seconds or less
            pass
        case "10-1":                        # Clear 10-1 Sleekhopper HD before the announcer says "Hurry Up!" without pausing
            pass
        case "10-2":                        # Clear 10-2 Smile with at least 25 banana bunches collected and without pausing
            pass
        case "10-4":                        # Balance atop the center bird while its wings are folded inwards and clear 10-4 Birds without pausing
            pass
        case "10-6":                        # Clear 10-6 Frame Windows without skipping around the wall
            pass
        case "10-7":                        # Clear 10-7 Desync by pressing every switch
            pass
        case "10-8":                        # Clear 10-8 Exam-651 without riding the lower wire between the second and the fourth yellow platform and without pausing
            pass
        case "10-10":                       # Clear 10-10 Antlers in 20 seconds or less without pausing
            pass

    mySet.add_achievement(ach)

# Specific to my PC for saving the set - change locally

dolphinPath = Path("E:\\Dolphin-x64\\RACache\\Data")
laptopPath = Path("D:\\RetroAchievements\\RALibretro\\RACache\\Data")
pcPath = Path("D:\\Games\\Emulation\\RetroAchievements\\RALibretro\\RACache\\Data")
    
match platform:
    case "Wii" | "GameCube":
        if dolphinPath.exists():
            mySet.save(dolphinPath)
    case default:
        if laptopPath.exists():
            mySet.save(laptopPath)
        elif pcPath.exists():
            mySet.save(pcPath)
        else:
            mySet.save()