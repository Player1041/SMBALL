from pycheevos.core.helpers import *
from profiles import GameProfile
from helpers.common import *

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