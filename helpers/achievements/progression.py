from pycheevos.core.helpers import *
from profiles import GameProfile
from helpers.common import *

# //
# Story Mode
# //

def story_world_clear(ctx: GameProfile, world: int):
    """Complete a world in Story Mode
    Parameters
    ----------
    ctx: GameProfile
        The game's memory profile
    world: int
        World number e.g. 1, 3, 5
    """
    logic = [
        *mode_check("story"),
    ]
    match world:
        case 10:
            logic.extend([
                ctx.world.delta() == 9,
                level_check("StaffRoll", "1")
            ])
        case _:
            logic.extend([
                ctx.world.delta() == world,
                ctx.world == world + 1
            ])
    
    return logic

def collect_x_bananas_story(ctx: GameProfile, banana_count: int):
    """Collect a specific amount of bananas in Story Mode.
    Parameters
    ----------
    ctx: GameProfile
        The game's memory profile
    banana_count: int
        Total amount of bananas to collect, typically 999
    """

    logic = [
        *mode_check("story"),
        ctx.bananas_collected.delta() < banana_count,
        ctx.bananas_collected >= banana_count
    ]
    
    return logic

def bananaless_story(ctx: GameProfile):
    logic = [
        *mode_check("story"),
        ctx.bananas_collected == 0x00,
        get_level("StaffRoll", 1)
    ]

    return logic

# //
# Challenge Mode
# //

def challenge_mode_complete(ctx: GameProfile, difficulty: str, total_levels: int):
    """Complete Challenge Mode.
    Parameters
    ----------
    ctx: GameProfile
        The game's memory profile
    difficulty: str
        Which difficulty of Challenge Mode should be checked - "Beginner", "Advanced", "Expert", "Master"
    total_levels: int
        Total levels in the challenge
    """

    logic = [
        *mode_check("challenge"),
    ]

    match difficulty.lower():
        case "beginner":
            logic.append(and_next(level_check("B", total_levels)))
        case "advanced":
            logic.append(and_next(level_check("A", total_levels)))
        case "expert":
            logic.append(and_next(level_check("E", total_levels)))
        case "master":
            logic.append(and_next(level_check("M", total_levels)))
        case "beginner extra":
            logic.append(and_next(level_check("BX", total_levels)))
        case "advanced extra":
            logic.append(and_next(level_check("AX", total_levels)))
        case "expert extra":
            logic.append(and_next(level_check("EX", total_levels)))
        case "master extra":
            logic.append(and_next(level_check("MX", total_levels)))
    
    logic.extend([
        ctx.stage_complete_delta,
        ctx.stage_complete
    ])

def challenge_and_extra_deathless(ctx: GameProfile, difficulty: str, stage_1_starting_time, final_level_of_extra):
    """Complete any Challenge Mode difficulty and its extra levels without dying.
    Parameters
    ----------
    ctx: GameProfile
        The game's memory profile
    difficulty: str
        Which difficulty of Challenge Mode should be checked - "Beginner", "Advanced", "Expert", "Master"
    stage_1_starting_time: int | float
        Level starting time. Should be treat as a float to allow for frame conversion, but accepts both ints and floats
    final_level_of_extra: level_check()
        What is the final level that the player should play before earning the achievement
    """

    logic = [
        *mode_check("challenge")
    ]

    match difficulty.lower():
        case "beginner":
            logic.append(and_next(level_check("B", 1)))
        case "advanced":
            logic.append(and_next(level_check("A", 1)))
        case "expert":
            logic.append(and_next(level_check("E", 1)))
        case "master":
            logic.append(and_next(level_check("M", 1)))

    logic.append(ctx.stage_time == stage_1_starting_time * 60).with_hits(1)

    match difficulty.lower():
        case "beginner":
            logic.append(and_next(level_check("BX", 10)))
        case "advanced":
            logic.append(and_next(level_check("AX", 10)))
        case "expert":
            logic.append(and_next(level_check("EX", 10)))
        case "master":
            logic.append(and_next(level_check("MX", 10)))
    
    logic.extend([
        and_next(ctx.stage_complete_delta),
        trigger(ctx.stage_complete),
        pause_if(ctx.lives < ctx.lives.delta())
    ])

    resetAltLogic = [
        reset_if(ctx.in_game == 0x00) # reset if out of game
    ]
    
    return logic, resetAltLogic

def challenge_and_extra_continueless(ctx: GameProfile, difficulty: str, stage_1_starting_time, final_level_of_extra):
    """Complete any Challenge Mode difficulty and its extra levels without using a continue.
    Parameters
    ----------
    ctx: GameProfile
        The game's memory profile
    difficulty: str
        Which difficulty of Challenge Mode should be checked - "Beginner", "Advanced", "Expert", "Master"
    stage_1_starting_time: int | float
        Level starting time. Should be treat as a float to allow for frame conversion, but accepts both ints and floats
    final_level_of_extra: level_check()
        What is the final level that the player should play before earning the achievement
    """

    logic = [
        *mode_check("challenge")
    ]

    match difficulty.lower():
        case "beginner":
            logic.append(and_next(level_check("B", 1)))
        case "advanced":
            logic.append(and_next(level_check("A", 1)))
        case "expert":
            logic.append(and_next(level_check("E", 1)))
        case "master":
            logic.append(and_next(level_check("M", 1)))

    logic.append(ctx.stage_time == stage_1_starting_time * 60).with_hits(1)

    match difficulty.lower():
        case "beginner":
            logic.append(and_next(level_check("BX", 10)))
        case "advanced":
            logic.append(and_next(level_check("AX", 10)))
        case "expert":
            logic.append(and_next(level_check("EX", 10)))
        case "master":
            logic.append(and_next(level_check("MX", 10)))
    
    logic.extend([
        and_next(ctx.stage_complete_delta),
        trigger(ctx.stage_complete),
        pause_if(ctx.continues_used > ctx.continues_used.delta())
    ])

    resetAltLogic = [
        reset_if(ctx.in_game == 0x00) # reset if out of game
    ]
    
    return logic, resetAltLogic

def challenge_and_extra_warpless(ctx: GameProfile, difficulty: str, stage_1_starting_time, final_level_of_extra):
    """Complete any Challenge Mode difficulty and it's extra levels without using a continue.
    Parameters
    ----------
    ctx: GameProfile
        The game's memory profile
    difficulty: str
        Which difficulty of Challenge Mode should be checked - "Beginner", "Advanced", "Expert", "Master"
    stage_1_starting_time: int | float
        Level starting time. Should be treat as a float to allow for frame conversion, but accepts both ints and floats
    final_level_of_extra: level_check()
        What is the final level that the player should play before earning the achievement
    """

    logic = [
        *mode_check("challenge")
    ]

    match difficulty.lower():
        case "beginner":
            logic.append(and_next(level_check("B", 1)))
        case "advanced":
            logic.append(and_next(level_check("A", 1)))
        case "expert":
            logic.append(and_next(level_check("E", 1)))
        case "master":
            logic.append(and_next(level_check("M", 1)))

    logic.append(ctx.stage_time == stage_1_starting_time * 60).with_hits(1)

    match difficulty.lower():
        case "beginner":
            logic.append(and_next(level_check("BX", 10)))
        case "advanced":
            logic.append(and_next(level_check("AX", 10)))
        case "expert":
            logic.append(and_next(level_check("EX", 10)))
        case "master":
            logic.append(and_next(level_check("MX", 10)))
    
    logic.extend([
        and_next(ctx.stage_complete_delta),
        trigger(ctx.stage_complete)
    ])

    resetAltLogic = [
        reset_if(ctx.in_game == 0x00) # reset if out of game
    ]
    
    return logic, resetAltLogic

def challenge_and_extra_warpless_deathless(ctx: GameProfile, difficulty: str, stage_1_starting_time, final_level_of_extra):
    """Complete any Challenge Mode difficulty and its extra levels without dying and without entering warp goals.
    Parameters
    ----------
    ctx: GameProfile
        The game's memory profile
    difficulty: str
        Which difficulty of Challenge Mode should be checked - "Beginner", "Advanced", "Expert", "Master"
    stage_1_starting_time: int | float
        Level starting time. Should be treat as a float to allow for frame conversion, but accepts both ints and floats
    final_level_of_extra: level_check()
        What is the final level that the player should play before earning the achievement
    """

    logic = [
        *mode_check("challenge")
    ]

    match difficulty.lower():
        case "beginner":
            logic.append(and_next(level_check("B", 1)))
        case "advanced":
            logic.append(and_next(level_check("A", 1)))
        case "expert":
            logic.append(and_next(level_check("E", 1)))
        case "master":
            logic.append(and_next(level_check("M", 1)))

    logic.append(ctx.stage_time == stage_1_starting_time * 60).with_hits(1)

    match difficulty.lower():
        case "beginner":
            logic.append(and_next(level_check("BX", 10)))
        case "advanced":
            logic.append(and_next(level_check("AX", 10)))
        case "expert":
            logic.append(and_next(level_check("EX", 10)))
        case "master":
            logic.append(and_next(level_check("MX", 10)))
    
    logic.extend([
        and_next(ctx.stage_complete_delta),
        trigger(ctx.stage_complete),
        pause_if(ctx.lives < ctx.lives.delta())
    ])

    logic.append(reset_if(ctx.goal_type != 0x00))

    resetAltLogic = [
        reset_if(ctx.in_game == 0x00) # reset if out of game
    ]
    
    return logic, resetAltLogic

def challenge_and_extra_warpless_continueless(ctx: GameProfile, difficulty: str, stage_1_starting_time, final_level_of_extra):
    """Complete any Challenge Mode difficulty and its extra levels without using a continue and without entering warp goals.
    Parameters
    ----------
    ctx: GameProfile
        The game's memory profile
    difficulty: str
        Which difficulty of Challenge Mode should be checked - "Beginner", "Advanced", "Expert", "Master"
    stage_1_starting_time: int | float
        Level starting time. Should be treat as a float to allow for frame conversion, but accepts both ints and floats
    final_level_of_extra: level_check()
        What is the final level that the player should play before earning the achievement
    """

    logic = [
        *mode_check("challenge")
    ]

    match difficulty.lower():
        case "beginner":
            logic.append(and_next(level_check("B", 1)))
        case "advanced":
            logic.append(and_next(level_check("A", 1)))
        case "expert":
            logic.append(and_next(level_check("E", 1)))
        case "master":
            logic.append(and_next(level_check("M", 1)))

    logic.append(ctx.stage_time == stage_1_starting_time * 60).with_hits(1)

    match difficulty.lower():
        case "beginner":
            logic.append(and_next(level_check("BX", 10)))
        case "advanced":
            logic.append(and_next(level_check("AX", 10)))
        case "expert":
            logic.append(and_next(level_check("EX", 10)))
        case "master":
            logic.append(and_next(level_check("MX", 10)))
    
    logic.extend([
        and_next(ctx.stage_complete_delta),
        trigger(ctx.stage_complete),
        pause_if(ctx.continues_used > ctx.continues_used.delta())
    ])

    logic.append(reset_if(ctx.goal_type != 0x00))

    resetAltLogic = [
        reset_if(ctx.in_game == 0x00) # reset if out of game
    ]
    
    return logic, resetAltLogic

def custom_clear_route(ctx: GameProfile, level_order: List() = []):
    """Define a custom route for the player to clear, useful for shortest routes.
    Parameters
    ----------
    ctx: GameProfile
        The game's memory profile
    level_order: List(clear_level_type_no_hits)
        List of levels to clear with specific goals for more unique routes
    """

    logic = [
        *mode_check("challenge")
    ]

    for level in level_order:
        logic.extend(level)
    
    resetAltLogic = [
        reset_in(ctx.in_game == 0x00) # reset if not in game
    ]

    return logic, resetAltLogic

# //
# Any Mode
# //

def clear_level_type(ctx: GameProfile, world, level: int, goal_type: str):
    """Check if a level has been completed via a specific goal"""
    hex_code, _, _, = get_level(ctx, world, level)
    match goal_type.lower():
        case "blue":
            hex_goal == 0x00
        case "green":
            hex_goal == 0x01
        case "red":
            hex_goal == 0x02
    
    return [
        and_next(ctx.level == hex_code),
        and_next(ctx.stage_complete_delta),
        and_next(ctx.stage_complete),
        add_hits(ctx.goal_type == hex_goal).with_hits(1)
    ]

def clear_level_type_no_hits(ctx: GameProfile, world, level: int, goal_type: str):
    """Check if a level has been completed via a specific goal"""
    hex_code, _, _, = get_level(ctx, world, level)
    match goal_type.lower():
        case "blue":
            hex_goal == 0x00
        case "green":
            hex_goal == 0x01
        case "red":
            hex_goal == 0x02
    
    return [
        and_next(ctx.level == hex_code),
        and_next(ctx.stage_complete_delta),
        and_next(ctx.stage_complete),
        (ctx.goal_type == hex_goal).with_hits(1)
    ]

def all_coloured_goals(ctx: GameProfile, mode: str, goal_list):
    """Complete every Red and Green goal in a single session.
    Parameters
    ----------
    ctx: GameProfile
        The game's memory profile
    mode: str
        Mode restriction, e.g. "story", "non-challenge"
    goal_list: List(clear_level_type)
        A list of levels and their goal type clears.
    """
    logic = [
        *mode_check(mode),
    ]

    for goal in goal_list:
        logic.extend(goal)
    logic.append(measured(value(0x00) == value(0x01)).with_hits(len(goal_list)))

    return logic