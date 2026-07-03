from pycheevos.core.helpers import *
from profiles import GameProfile
from helpers.common import *

# //
# Info: This file holds all of the IL challenge functions. 
# /progression.py holds all of the mode completion functions.
# These include completing a world, completing a Challenge difficulty, 
# as well as various challenge functions for doing x conditions across the whole run.
# //

# //
# Time Related Functions
# //

def timed(ctx: GameProfile, mode: str, world, level, starting_time, within_time):
    """
    Clear a level within a time limit.
    
    Parameters
    ----------
    ctx: GameProfile
        The game's memory profile
    mode: str
        Mode restriction, e.g. "story", "non-challenge"
    world: int | str
        World number or letter e.g. 1, 3, 5, "MX", "B"
    level: int
        Level number
    starting_time: int | float
        Level starting time. Should be treat as a float to allow for frame conversion, but accepts both ints and floats
    within_time: int | float
        How fast should the user complete the level in. Should be treat as a float to allow for frame conversion, but accepts both ints and floats
    """

    if starting_time == int:
        float(starting_time)
    if within_time == int:
        float(within_time)

    logic = [
        *mode_check(mode),
        reset_level_check(world, level),
        time_checkpoint(ctx, starting_time),
        reset_if(ctx.stage_time == ((starting_time - within_time) * 60)),
        trigger(ctx.stage_complete_delta),
        trigger(ctx.stage_complete),
        reset_if(ctx.stage_time == 0)
    ]

    return logic

# //
# Speed Related Functions
# //
    
def over_speed(ctx: GameProfile, mode: str, world, level, required_speed: int):
    """
    Clear a level with a specific speed.
    
    Parameters
    ----------
    ctx: GameProfile
        The game's memory profile
    mode: str
        Mode restriction, e.g. "story", "non-challenge"
    world: int | str
        World number or letter e.g. 1, 3, 5, "MX", "B"
    level: int
        Level number
    required_speed: int
        Required speed to hit while clearing the goal e.g Clear 1-2 at over 300mph.
    """
    
    logic = [
        *mode_check*(mode),
        level_check(world, level),
        over_speed_check(ctx, required_speed),
        trigger(ctx.stage_complete_delta),
        trigger(ctx.stage_complete),
        ctx.stage_time != 0x00
    ]

    return logic

def under_speed(ctx: GameProfile, mode: str, world, level, required_speed: int):
    """
    Clear a level with a specific speed.
    
    Parameters
    ----------
    ctx: GameProfile
        The game's memory profile
    mode: str
        Mode restriction, e.g. "story", "non-challenge"
    world: int | str
        World number or letter e.g. 1, 3, 5, "MX", "B"
    level: int
        Level number
    required_speed: int
        Required speed to stay under while clearing the goal e.g Clear 1-2 at under 300mph.
    """
    
    logic = [
        *mode_check*(mode),
        level_check(world, level),
        under_speed_check(ctx, required_speed),
        trigger(ctx.stage_complete_delta),
        trigger(ctx.stage_complete),
        ctx.stage_time != 0x00
    ]

    return logic

def miminum_speed_hit(ctx: GameProfile, mode: str, world, level, starting_time, required_speed: int):
    """
    Clear a level with a specific speed.
    
    Parameters
    ----------
    ctx: GameProfile
        The game's memory profile
    mode: str
        Mode restriction, e.g. "story", "non-challenge"
    world: int | str
        World number or letter e.g. 1, 3, 5, "MX", "B"
    level: int
        Level number
    required_speed: int
        Required speed to hit at any point in the stage.
    """
    
    logic = [
        *mode_check*(mode),
        reset_level_check(world, level),
        time_checkpoint(ctx, starting_time),
        over_speed_at_any_point_check(ctx, required_speed),
        trigger(ctx.stage_complete_delta),
        trigger(ctx.stage_complete),
        reset_if(ctx.stage_time != 0x00)
    ]

    return logic

# TODO: maximum_speed_hit()

# //
# Banana Related Functions
# //

def all_bananas_collected(ctx: GameProfile, mode: str, world, level, starting_time):
    """
    Collect every banana in a level, then complete the level
    
    Parameters
    ----------
    ctx: GameProfile
        The game's memory profile
    mode: str
        Mode restriction, e.g. "story", "non-challenge"
    world: int | str
        World number or letter e.g. 1, 3, 5, "MX", "B"
    level: int
        Level number
    starting_time: int | float
        Level starting time. Should be treat as a float to allow for frame conversion, but accepts both ints and floats
    """

    logic = [
        *mode_check(mode),
        reset_level_check(world, level),
        time_checkpoint(ctx, starting_time),
        (ctx.bananas_remaining != 0x00).with_hits(1),
        trigger(ctx.bananas_remaining),
        trigger(ctx.stage_complete_prior),
        trigger(ctx.stage_complete),
        reset_if(ctx.stage_time == 0x00)
    ]

    return logic

def banana_bunches_collected(ctx: GameProfile, mode: str, world, level, total_collected):
    """Collect total_collected amount of banana bunches, not singles, in a level.
    Parameters    
    ----------    
    ctx: GameProfile    
        The game's memory profile    
    mode: str
        Mode restriction, e.g. "story", "non-challenge"
    world: int | str
        World number or letter e.g. 1, 3, 5, "MX", "B"
    level: int
        Level number
    total_collected:  int
        Total amount of banana bunches to collect before finishing
    """

    logic = [
        *mode_check(mode),
        reset_level_check(world, level),
        add_source(value(1000)),
        trigger((ctx.score_global.delta() == ctx.score_global).with_hits(total_collected)),
        trigger(ctx.stage_complete_prior),
        trigger(ctx.stage_complete),
        reset_if(ctx.stage_time == 0x00)
    ]
    return logic

def minimum_bananas_collected(ctx: GameProfile, mode: str, world, level, starting_time, total_collected):
    """Collect total_collected amount of bananas in a level.
    Parameters    
    ----------    
    ctx: GameProfile    
        The game's memory profile    
    mode: str
        Mode restriction, e.g. "story", "non-challenge"
    world: int | str
        World number or letter e.g. 1, 3, 5, "MX", "B"
    level: int
        Level number
    starting_time: int | float
        Level starting time. Should be treat as a float to allow for frame conversion, but accepts both ints and floats
    total_collected:  int
        Total amount of bananas to collect before finishing
    """

    logic = [
        *mode_check(mode),
        reset_level_check(world, level),
        time_checkpoint(ctx, starting_time)
    ]

    for x in range(0, 9):
        logic.append(sub_source(ctx.bananas_collected.delta()))
        logic.append(add_hits(ctx.bananas_collected == value(0x0a)))

    logic.extend([
        measured(ctx.bananas_collected > ctx.bananas_collected.delta()).with_hits(total_collected),
        trigger(ctx.stage_complete_delta),
        trigger(ctx.stage_complete),
        reset_if(ctx.stage_time == 0x00)
    ])

    return logic

def maximum_bananas_collected(ctx: GameProfile, mode: str, world, level, starting_time, max_bananas):
    """Collect at most max_bananas bananas over the stage
    Parameters
    ----------    
    ctx: GameProfile    
        The game's memory profile    
    mode: str
        Mode restriction, e.g. "story", "non-challenge"
    world: int | str
        World number or letter e.g. 1, 3, 5, "MX", "B"
    level: int
        Level number
    starting_time: int | float
        Level starting time. Should be treat as a float to allow for frame conversion, but accepts both ints and floats
    max_bananas:  int
        Maximum amount of bananas allowed to collect
    """

    if max_bananas != 0:
        max_bananas += 1

    logic = [
        *mode_check(mode),
        reset_level_check(world, level),
        time_checkpoint(ctx, starting_time),
        reset_if(ctx.bananas_remaining < ctx.bananas_remaining.delta()).with_hits(max_bananas),
        trigger(ctx.stage_complete_delta),
        trigger(ctx.stage_complete),
        reset_if(ctx.stage_time == 0x00)
    ]

    return logic

def bananaless(ctx: GameProfile, mode: str, world, level, starting_time):
    """Complete a level without collecting any bananas.
    Parameters
    ----------    
    ctx: GameProfile    
        The game's memory profile    
    mode: str
        Mode restriction, e.g. "story", "non-challenge"
    world: int | str
        World number or letter e.g. 1, 3, 5, "MX", "B"
    level: int
        Level number
    starting_time: int | float
        Level starting time. Should be treat as a float to allow for frame conversion, but accepts both ints and floats
    """

    logic = [
        *mode_check(mode),
        reset_level_check(world, level),
        time_checkpoint(ctx, starting_time),
        reset_if(ctx.bananas_remaining < ctx.bananas_remaining.delta()),
        trigger(ctx.stage_complete_delta),
        trigger(ctx.stage_complete),
        reset_if(ctx.stage_time == 0x00)
    ]

    return logic

# //
# Score Related Functions
# //

def score_clear(ctx: GameProfile, mode: str, world, level, score_required):
    """Have this score at the end of the level.
    Parameters
    ----------    
    ctx: GameProfile    
        The game's memory profile    
    mode: str
        Mode restriction, e.g. "story", "non-challenge"
    world: int | str
        World number or letter e.g. 1, 3, 5, "MX", "B"
    level: int
        Level number
    score_required: int
        Total score needed at end of level
    """
    logic = [
        *mode_check(mode),
        level_check(world, level),
        and_next(ctx.score_level != 0xffffffff),
        trigger(ctx.level_score >= score_required),
        trigger(ctx.replay_playing_delta),
        trigger(ctx.replay_playing),
        trigger(ctx.stage_complete),
        ctx.stage_time != 0x00
    ]

    return logic

# //
# Switch Related Functions
# //

def global_switchless(ctx: GameProfile, mode: str, world, level, starting_time):
    """Complete a level without ever pressing a switch.
    Parameters
    ----------
    ctx: GameProfile    
        The game's memory profile    
    mode: str
        Mode restriction, e.g. "story", "non-challenge"
    world: int | str
        World number or letter e.g. 1, 3, 5, "MX", "B"
    level: int
        Level number
    starting_time: int | float
        Level starting time. Should be treat as a float to allow for frame conversion, but accepts both ints and floats
    """
    logic = [
        *mode_check(mode),
        reset_level_check(world, level),
        time_checkpoint(ctx, starting_time),
        and_next(ctx.switch_pressed.delta() == 0x00),
        reset_if(ctx.switch_pressed == 0x01),
        trigger(ctx.stage_complete_delta),
        trigger(ctx.stage_complete),
        reset_if(ctx.stage_time == 0x00)
    ]

    return logic

def all_switches(ctx: GameProfile, mode: str, world, level, starting_time, boxes):
    """Complete a level with every single switch pressed.
    Parameters
    ----------
    ctx: GameProfile    
        The game's memory profile    
    mode: str
        Mode restriction, e.g. "story", "non-challenge"
    world: int | str
        World number or letter e.g. 1, 3, 5, "MX", "B"
    level: int
        Level number
    starting_time: int | float
        Level starting time. Should be treat as a float to allow for frame conversion, but accepts both ints and floats
    boxes: List(bounding, inverted_bounding)
        A list of bounding boxes using the bounding() and/or inverted_bounding().
    """
    logic = [
        *mode_check(mode),
        reset_level_check(world, level),
        time_checkpoint(ctx, starting_time)
    ]

    for box in boxes:
        logic.extend(box)
        logic.extend([
            and_next(ctx.switch_pressed.delta() == 0x00),
            (ctx.switch_pressed == 0x01).with_hits(1)
        ])

    logic.extend([
        trigger(ctx.stage_complete_delta),
        trigger(ctx.stage_complete),
        reset_if(ctx.stage_time == 0x00)
    ])

    return logic

def miss_specific_switch(ctx: GameProfile, mode: str, world, level, starting_time, boxes):
    """Complete a level without pressing a specific switch.
    Parameters
    ----------
    ctx: GameProfile    
        The game's memory profile    
    mode: str
        Mode restriction, e.g. "story", "non-challenge"
    world: int | str
        World number or letter e.g. 1, 3, 5, "MX", "B"
    level: int
        Level number
    starting_time: int | float
        Level starting time. Should be treat as a float to allow for frame conversion, but accepts both ints and floats
    boxes: List(bounding, inverted_bounding)
        A list of bounding boxes using the bounding() and/or inverted_bounding().
    """

    logic = [
        *mode_check(mode),
        reset_level_check(world, level),
        time_checkpoint(ctx, starting_time)
    ]

    for box in boxes:
        logic.extend(box)
        logic.extend([
            and_next(ctx.switch_pressed.delta() == 0x00),
            reset_if(ctx.switch_pressed == 0x01)
        ])
    
    logic.extend([
        trigger(ctx.stage_complete_delta),
        trigger(ctx.stage_complete),
        reset_if(ctx.stage_time == 0x00)
    ])
    return logic

def miss_every_switch_bar_one(ctx: GameProfile, mode: str, world, level, starting_time, boxes, identifier = None):
    """Complete a level without pressing any switch except for one.
    Parameters
    ----------
    ctx: GameProfile    
        The game's memory profile    
    mode: str
        Mode restriction, e.g. "story", "non-challenge"
    world: int | str
        World number or letter e.g. 1, 3, 5, "MX", "B"
    level: int
        Level number
    starting_time: int | float
        Level starting time. Should be treat as a float to allow for frame conversion, but accepts both ints and floats
    boxes: List(bounding, inverted_bounding)
        A list of bounding boxes using the bounding() and/or inverted_bounding(); likely needs to use inverted_bounding()
    identifier: str
        Legacy: added specifically for BX8 for 349 since it has a row of switches, including a mandatory switch, so it should only reset if two pause switches are pressed, excluding this button
    """

    logic = [
        *mode_check(mode),
        reset_level_check(world, level),
        time_checkpoint(ctx, starting_time)
    ]

    match identifier.lower():
        case "two_box": # this was specificly made for BX8 for 349, but is included as legacy code - feel free to override this and add more cases if needed.
            for box in boxes:
                logic.extend(box)
            logic.extend([
                and_next(ctx.switch_pressed.delta() == 0x00),
                reset_if(ctx.switch_pressed == 0x01),
                and_next(ctx.switch_pressed.delta() == 0x00),
                (ctx.switch_pressed == 0x01).with_hits(2)
            ])
        case _:
            for box in boxes:
                logic.extend(box)
                logic.extend([
                    and_next(ctx.switch_pressed.delta() == 0x00),
                    reset_if(ctx.switch_pressed == 0x01)
                ])

    logic.extend([
        trigger(ctx.stage_complete_delta),
        trigger(ctx.stage_complete),
        reset_if(ctx.stage_time == 0x00)
    ])
    
    return logic

# TODO: limited_switch_presses()

# //
# Miscellaneous Functions
# //

def limited_wormhole_entries(ctx: GameProfile, mode: str, world, level, starting_time, max_wormhole_entries):
    """Complete a level with a limited amount of wormhole entries.
    Parameters
    ----------
    ctx: GameProfile    
        The game's memory profile    
    mode: str
        Mode restriction, e.g. "story", "non-challenge"
    world: int | str
        World number or letter e.g. 1, 3, 5, "MX", "B"
    level: int
        Level number
    starting_time: int | float
        Level starting time. Should be treat as a float to allow for frame conversion, but accepts both ints and floats
    max_entries: int
        Maximum amount of wormhole entries allowed to complete the level
    """

    if max_wormhole_entries != 0:
        max_wormhole_entries += 1
    
    logic = [
        *mode_check(mode),
        reset_level_check(world, level),
        # do add address(wormhole_entered) if still buggy
        time_checkpoint(ctx, starting_time),
        reset_if(ctx.wormhole_entries > ctx.wormhole_entries.delta()).with_hits(max_wormhole_entries),
        trigger(ctx.stage_complete_delta),
        trigger(ctx.stage_complete),
        reset_if(ctx.stage_time == 0x00)
    ]

    return logic

def special_path(ctx: GameProfile, mode: str, world, level, starting_time, start_reset, start_checkpoint, end_checkpoint):
    """Complete a level having taken a specific path.
    Parameters
    ----------
    ctx: GameProfile    
        The game's memory profile    
    mode: str
        Mode restriction, e.g. "story", "non-challenge"
    world: int | str
        World number or letter e.g. 1, 3, 5, "MX", "B"
    level: int
        Level number
    starting_time: int | float
        Level starting time. Should be treat as a float to allow for frame conversion, but accepts both ints and floats
    start_reset: bounding(), inverted_bounding()
        A bounding box that serves as the only place the player can swap off of the path, signalling a failure of the challenge and a hit reset
    start_checkpoint: bounding(), inverted_bounding()
        A bounding box that serves as the first spot along the path which can be considered a checkpoint; ideally, this is some place just after the reset and is impossible to get from here to an easier path without going through the start_reset
    end_checkpoint: bounding(), inverted_bounding()
        A bounding box that serves as the last spot along the path which can be considered a checkpoint; ideally, this is some place just before the end of the path and is impossible to get from here to an easier path without going through the start_reset
    """

    logic = [
        *mode_check(mode),
        reset_level_check(world, level),
        time_checkpoint(ctx, starting_time),
        *start_reset,
        reset_next_if(value(0x00) == value(0x00)) # resets if the player has entered the box
        *start_checkpoint,
        value(0x00) == value(0x00).with_hits(1), # incurs a hit if the player is inside the box
        *end_checkpoint,
        trigger(value(0x00) == value(0x00).with_hits(1)), # incurs a hit if the player is inside the box, trigger makes it clear to see if the challenge is active or not
        trigger(ctx.stage_complete_delta),
        trigger(ctx.stage_complete),
        reset_if(ctx.stage_time == 0x00)
    ]

    return logic

def multiple_special_paths(ctx: GameProfile, mode: str, world, level, starting_time, paths):
    """special_path() adapted for multiple path choices.
    Parameters
    ----------
    ctx: GameProfile    
        The game's memory profile    
    mode: str
        Mode restriction, e.g. "story", "non-challenge"
    world: int | str
        World number or letter e.g. 1, 3, 5, "MX", "B"
    level: int
        Level number
    starting_time: int | float
        Level starting time. Should be treat as a float to allow for frame conversion, but accepts both ints and floats
    paths: List()
        paths should contain:
            start_reset: bounding(), inverted_bounding()
                A bounding box that serves as the only place the player can swap off of the path, signalling a failure of the challenge and a hit reset
            start_checkpoint: bounding(), inverted_bounding()
                A bounding box that serves as the first spot along the path which can be considered a checkpoint; ideally, this is some place just after the reset and is impossible to get from here to an easier path without going through the start_reset
            end_checkpoint: bounding(), inverted_bounding()
                A bounding box that serves as the last spot along the path which can be considered a checkpoint; ideally, this is some place just before the end of the path and is impossible to get from here to an easier path without going through the start_reset
    """

    logic = [
        *mode_check(mode),
        reset_level_check(world, level),
        time_checkpoint(ctx, starting_time),
    ]

    for path in paths:
        start_reset, start_checkpoint, end_checkpoint = path[0], path[1], path[2]
        logic.extend([
            *start_reset,
            reset_next_if(value(0x00) == value(0x00)),
            *start_checkpoint,
            value(0x00) == value(0x00).with_hits(1),
            *end_checkpoint,
            trigger(value(0x00) == value(0x00).with_hits(1))
        ])

    logic.extend([
        trigger(ctx.stage_complete_delta),
        trigger(ctx.stage_complete),
        reset_if(ctx.stage_time == 0x00)
    ])
    return logic



def multiple_goals_within_x_time(ctx: GameProfile, mode: str, world, level, starting_time, within_time, goals):
    """Complete a level with multiple goals within a time limit.
    Parameters
    ----------
    ctx: GameProfile    
        The game's memory profile    
    mode: str
        Mode restriction, e.g. "story", "non-challenge"
    world: int | str
        World number or letter e.g. 1, 3, 5, "MX", "B"
    level: int
        Level number
    starting_time: int | float
        Level starting time. Should be treat as a float to allow for frame conversion, but accepts both ints and floats
    within_time: int | float
        How fast should the user complete the level in. Should be treat as a float to allow for frame conversion, but accepts both ints and floats
    goals: List[function]
        A list of functions that represent the goals to be completed within the time limit
    """

    if starting_time == int:
        float(starting_time)
    if within_time == int:
        float(within_time)

    logic = [
        *mode_check(mode),
        reset_level_check(world, level),
        time_checkpoint_multiple_sessions(ctx, starting_time),
        (ctx.stage_time.prior() == starting_time * 60).with_hits(1)
    ]

    for goal in goals:
        logic.extend(goal)

    logic.extend([
        trigger(ctx.stage_complete_delta),
        trigger(ctx.stage_complete),
        reset_if(ctx.stage_time == 0x00)
    ])

    return logic
