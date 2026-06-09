from dataclasses import dataclass, field
from typing import Any

@dataclass
class GameProfile:
    # Options
    character_selected:          Any = None                 # [8-bit] Selected Character
                                                            # 0x00=AiAi
                                                            # 0x01=MeeMee
                                                            # 0x02=Baby
                                                            # 0x03=GonGon

    main_mode_option:            Any = None                 # [8-bit] Main Mode Select
                                                            # 0x00 - Main Game
                                                            # 0x01 - Party Mode
                                                            # 0x02 - Options

    main_game_option:            Any = None                 # [8-bit] Main Game Select
                                                            # 0x00 = Story Mode
                                                            # 0x01 = Challenge Mode
                                                            # 0x02 = Practice Mode

    in_game:                     Any = None                 # [32-bit BE] In game check
                                                            # 0x00 - Not in game
                                                            # 0x01 - In game

    paused:                      Any = None                 # [8-bit] Pause Check
                                                            # bit3 - Paused

    # Level                 
    LEVEL_TABLE:                 Any = None                 # Specified in the script file. 
                                                            # LEVEL_TABLE: dict[tuple[Union[int, str], int], tuple[int, str, int]] = { 
                                                            # # World, Level, Level ID, Level Name, Starting Timer
                                                            # (1,  1): (0xc9,  "1-1 Ease", 60),
                                                            # (1,  2): (0xca,  "1-2 Interceptor", 60),
                                                            # (1,  3): (0xcb,  "1-3 Cornercraft", 60),
                                                            # }

    world:                       Any = None                 # [8-bit] [Story Mode] World ID
    level:                       Any = None                 # [32-bit BE] Level ID | specify levels in the ctx.LEVEL_TABLE in the script file.

    # HUD               
    stage_time:                  Any = None                 # [16-bit BE] Timer

    speed:                       Any = None                 # [32-bit BE] Pointer to HUD - Stored as ASCII
                                                            # +0x720: [8-bit] MPH Hundreds
                                                            # +0x721: [8-bit] MPH Tens
                                                            # +0x722: [8-bit] MPH Ones

    lives:                       Any = None                 # [8-bit] Lives | +1 from display
    deaths:                      Any = None                 # [32-bit BE] Death Counter for Challenge Mode | Used in hacks with no life counter i.e Gaiden
 
    # Goal State 
    goal_state:                  Any = None                 # [8-bit bitflags] Goal State
 
    goal_hit:                    bit0(goal_state)           # bit0 - Goal!
    goal_hit_delta:              bit0(goal_state.delta())
    goal_hit_prior:              bit0(goal_state.prior())

    time_out:                    bit1(goal_state)           # bit1 - Out of Time
    time_out_delta:              bit1(goal_state.delta())
    time_out_prior:              bit1(goal_state.prior())
 
    fall_out:                    bit2(goal_state)           # bit2 - Fall out
    fall_out_delta:              bit2(goal_state.delta())
    fall_out_prior:              bit2(goal_state.prior())
 
    time_paused:                 bit3(goal_state)           # bit3 - Time Paused
    time_paused_delta:           bit3(goal_state.delta())
    time_paused_prior:           bit3(goal_state.prior())
 
    replay_playing:              bit4(goal_state)           # bit4 - Replay
    replay_playing_delta:        bit4(goal_state.delta())
    replay_playing_prior:        bit4(goal_state.prior())
 
    stage_complete:              bit5(goal_state)           # bit5 - Completed Stage
    stage_complete_delta:        bit5(goal_state.delta())
    stage_complete_prior:        bit5(goal_state.prior())
 
    goal_type:                   Any = None                 # [8-bit] Goal Type
                                                            # 0x00 - Blue Goal
                                                            # 0x01 - Green Goal
                                                            # 0x02 - Red Goal
 
    # Bananas 
    bananas_remaining:           Any = None                 # [32-bit BE] Bananas remaining in stage
    bananas_collected:           Any = None                 # [32-bit BE] Bananas collected
 
    # Score 
    score_global:                Any = None                 # [32-bit BE] Score across every level
    score_level:                 Any = None                 # [32-bit BE] Level Score Pointer
                                                            # +0x10 - [32-bit BE] Level Score - doesn't get set until replay / bit4 gets set, displays 0xff until.
 
    # Coordinates 
    x_coord:                     Any = None                 # [Float BE] X coordinate
    y_coord:                     Any = None                 # [Float BE] Y coordinate
    z_coord:                     Any = None                 # [Float BE] Z coordinate
 
    # Misc 
    switch_pressed:              Any = None                 # [8-bit] Switch pressed - seems reused and is tied to nearest box? Should be paired with a coordinate box
                                                            # bit2 - Pressed | 0 - No, 1 - Yes

    wormhole_entered:            Any = None                 # [32-bit BE Pointer] Wormhole Pointer
    wormhole_entered_delta:      Any = None                 # +0xd8: [8-bit] Wormhole
    wormhole_entered_prior:      Any = None                 # .0x01 - Wormhole has been entered
