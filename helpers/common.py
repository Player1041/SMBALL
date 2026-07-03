from pycheevos.core.helpers import *
from profiles import GameProfile

def bounding(ctx: GameProfile,
                x1: float,
                x2: float,
                y1: float,
                y2: float,
                z1: float,
                z2: float,
                include_y: bool = True):
    """
    Bounding box. x1 >= x <= x2
    """

    match include_y:
        case True:
            return [
                and_next(ctx.x_coord >= x1),
                and_next(ctx.x_coord <= x2),
                and_next(ctx.y_coord >= y1),
                and_next(ctx.y_coord <= y2),
                and_next(ctx.z_coord >= z1),
                and_next(ctx.z_coord <= z2)
            ]
        case False:
            return [
                and_next(ctx.x_coord >= x1),
                and_next(ctx.x_coord <= x2),
                and_next(ctx.z_coord >= z1),
                and_next(ctx.z_coord <= z2)
            ]

def inverted_bounding(ctx: GameProfile,
                x1: float,
                x2: float,
                y1: float,
                y2: float,
                z1: float,
                z2: float,
                include_y: bool = True):
    """
    Inverted bounding box. x1 <= x >= x2
    """

    match include_y:
        case True:
            return [
                 or_next(ctx.x_coord >= x1),
                and_next(ctx.x_coord <= x2),
                 or_next(ctx.y_coord >= y1),
                and_next(ctx.y_coord <= y2),
                 or_next(ctx.z_coord >= z1),
                and_next(ctx.z_coord <= z2)
            ]
        case False:
            return [
                 or_next(ctx.x_coord >= x1),
                and_next(ctx.x_coord <= x2),
                 or_next(ctx.z_coord >= z1),
                and_next(ctx.z_coord <= z2)
            ]
        
def get_level(ctx: GameProfile, world: int | str, level: int) -> tuple[int, str, int]:
    if (world, level) not in ctx.LEVEL_TABLE:
        raise ValueError(f"No entry for World {world}-{level}")
    return ctx.LEVEL_TABLE[(world, level)]

def level_check(ctx: GameProfile, world, level):
    """Search the level table to retrieve its hex code."""

    hex_code, _, _ = story_level(world, level)
    return ctx.level_id == hex_code

def reset_level_check(ctx: GameProfile, world, level):
    """Search the level table to retrieve the hex code, and reset hits if not in that level"""
    hex_code, _, _ = story_level(world, level)
    return reset_if(ctx.level_id == hex_code)

def mode_check(ctx: GameProfile, mode):
    """Check which mode you want the player to play in."""
    match mode.lower():
        case "story":
            return [ctx.main_mode_option == 0x00,
                    ctx.main_game_option == 0x00]
        case "challenge":
            return [ctx.main_mode_option == 0x00,
                    ctx.main_game_option == 0x01]
        case "practice":
            return [ctx.main_mode_option == 0x00,
                    ctx.main_game_option == 0x02]
        case "non-challenge":
            return [ctx.main_mode_option == 0x00,
                    or_next(ctx.main_game_option == 0x00),
                    ctx.main_game_option == 0x02]
        case "non-story":
            return [ctx.main_mode_option == 0x00,
                    or_next(ctx.main_game_option == 0x01),
                    ctx.main_game_option == 0x02]
        case "non-practice": # not sure why you'd ban practice but ok
            return [ctx.main_mode_option == 0x00,
                    or_next(ctx.main_game_option == 0x00),
                    ctx.main_game_option == 0x01]
        
def time_checkpoint(ctx: GameProfile, starting_time):
    """Reset any hits on level checkpoint - also functions as a checkpoint, so you have to restart the level to retry challenges."""
    return [
        reset_if(ctx.stage_time == starting_time * 60),
        (ctx.stage_time.prior() == starting_time * 60).with_hits(1)
    ]

def time_checkpoint_multiple_sessions(ctx: GameProfile, starting_time):
    """Reset any hits on level checkpoint - also functions as a checkpoint, so you have to restart the level to retry challenges."""
    return [
        reset_next_if(ctx.stage_time == starting_time * 60),
        pause_if(ctx.stage_time.prior() == starting_time * 60).with_hits(1)
    ]

def over_speed_check(ctx: GameProfile, required_speed):
    """Complete the stage while at/over this speed."""
    return [
        add_source(ctx.speed_pointer >> ctx.speed_hundreds),
        add_source(ctx.speed_pointer >> ctx.speed_tens),
        ctx.speed_pointer >> ctx.speed_ones >= value(required_speed)
    ]

def under_speed_check(ctx: GameProfile, required_speed):
    """Complete the stage while at/over this speed."""
    return [
        add_source(ctx.speed_pointer >> ctx.speed_hundreds),
        add_source(ctx.speed_pointer >> ctx.speed_tens),
        ctx.speed_pointer >> ctx.speed_ones <= value(required_speed)
    ]

def over_speed_at_any_point_check(ctx: GameProfile, required_speed):
    """Hit this speed at any point while in the level."""
    return [
        add_source(ctx.speed_pointer >> ctx.speed_hundreds),
        add_source(ctx.speed_pointer >> ctx.speed_tens),
        ctx.speed_pointer >> ctx.speed_ones >= value(required_speed).with_hits(1)
    ]

def stay_above_speed_check(ctx: GameProfile, minimum_speed):
    """Hit a specific speed and do not go under it at any point in the level until you finish."""
    return [
        add_source(ctx.speed_pointer >> ctx.speed_hundreds),
        add_source(ctx.speed_pointer >> ctx.speed_tens),
        and_next(ctx.speed_pointer >> ctx.speed_ones >= value(minimum_speed)).with_hits(1),
        add_source(ctx.speed_pointer >> ctx.speed_hundreds),
        add_source(ctx.speed_pointer >> ctx.speed_tens),
        reset_if(ctx.speed_pointer >> ctx.speed_ones < value(minimum_speed))
    ]

def pause(ctx: GameProfile):
    """Add a pauseless condition to an achievement."""
    return reset_if(ctx.paused == 0x01)