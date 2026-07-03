from pycheevos.core.helpers import *
from profiles import GameProfile

mask = value(0x1fffffff)

template_smb2_profile = GameProfile(
    character_selected          = None,
    main_mode_option            = None,
    main_game_option            = None,
    in_game                     = None,
    paused                      = None,

    LEVEL_TABLE                 = {},
    world                       = None,
    level                       = None,

    stage_time                  = None,
    speed_pointer               = None,
    lives                       = None,
    deaths                      = None,
    continues_used              = None,

    goal_state                  = None, # remember: keep as hex, don't put into mem expr
    goal_type                   = None,

    bananas_remaining           = None,
    bananas_collected           = None,

    score_global                = None,
    score_level                 = None,

    x_coord                     = None,
    y_coord                     = None,
    z_coord                     = None,

    switch_pressed              = None,
    wormhole_entered            = None,
    wormhole_entered_delta      = None,
    wormhole_entered_prior      = None
)

default_smb2_profile = GameProfile(
    character_selected          = byte(0x54df78),
    main_mode_option            = byte(0x54df20),
    main_game_option            = byte(0x54df27),
    in_game                     = dword_be(0x5bc484),
    paused                      = bit3(0x5bc477),

    LEVEL_TABLE                 = {},
    world                       = byte(0x54dbbd),
    level                       = dword_be(0x473118),

    stage_time                  = word_be(0x553974),
    speed_pointer               = (dword_be(0x5ed1c4) & mask),
    lives                       = byte(0x5bc9a2),
    deaths                      = dword_be(0x969c80),
    continues_used              = word_be(0x55399a),

    goal_state                  = 0x553973,
    goal_type                   = byte(0x5539a8),

    bananas_remaining           = dword_be(0x553994),
    bananas_collected           = dword_be(0x5bca18),

    score_global                = dword_be(0x5bca1c),
    score_level                 = (dword_be(0x5be7d0) & mask) >> dword_be(0x10),

    x_coord                     = float32_be(0x5bc9a4),
    y_coord                     = float32_be(0x5bc9a8),
    z_coord                     = float32_be(0x5bc9ac),

    switch_pressed              = bit2(0x56e36a),
    wormhole_entered            = (dword_be(0x61ba90) & mask) >> byte(0xd8),
    wormhole_entered_delta      = (dword_be(0x61ba90) & mask) >> byte(0xd8).delta(),
    wormhole_entered_prior      = (dword_be(0x61ba90) & mask) >> byte(0xd8).prior(),
)