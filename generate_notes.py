from profiles.addresses import get_profile
from pycheevos.core.value import MemoryExpression
import dataclasses
import re

game = input("Input your game: ")
profile = get_profile(game)

SKIP_SUFFIXES = ("_delta", "_prior")
SKIP_FIELDS = ("LEVEL_TABLE",)

FIELD_NOTES = {
    "character_selected":   "[8-bit] Selected Character\r\n0x00 - AiAi\r\n0x01 - MeeMee\r\n0x02 - Baby\r\n0x03 - GonGon",
    "main_mode_option":     "[8-bit] Main Mode Select\r\n0x00 - Main Game\r\n0x01 - Party Mode\r\n0x02 - Options",
    "main_game_option":     "[8-bit] Main Game Select\r\n0x00 - Story Mode\r\n0x01 - Challenge Mode\r\n0x02 - Practice Mode",
    "in_game":              "[32-bit BE] In game check\r\n0x00 - Not in game\r\n0x01 - In game",
    "paused":               "[8-bit] Pause Check\r\nbit3 - Paused",
    "world":                "[8-bit] [Story Mode] World ID",
    "level":                "[32-bit BE] Level ID | specify levels in the ctx.LEVEL_TABLE in the script file.",
    "stage_time":           "[16-bit BE] Timer",
    "speed_pointer":        "[32-bit BE] Pointer to HUD - Stored as ASCII\r\n+0x720: [8-bit] MPH Hundreds\r\n+0x721: [8-bit] MPH Tens\r\n+0x722: [8-bit] MPH Ones",
    "lives":                "[8-bit] Lives | +1 from display",
    "deaths":               "[32-bit BE] Death Counter for Challenge Mode | Used in hacks with no life counter i.e Gaiden",
    "continues_used":       "[16-bit BE] Total Continues used",
    "goal_state":           "[8-bit bitflags] Goal State",
    "goal_type":            "[8-bit] Goal Type\r\n0x00 - Blue Goal\r\n0x01 - Green Goal\r\n0x02 - Red Goal",
    "bananas_remaining":    "[32-bit BE] Bananas remaining in stage",
    "bananas_collected":    "[32-bit BE] Bananas collected",
    "score_global":         "[32-bit BE] Score across every level",
    "score_level":          "[32-bit BE] Level Score Pointer\r\n+0x10 - [32-bit BE] Level Score - doesn't get set until replay / bit4 gets set, displays 0xff until.",
    "x_coord":              "[Float BE] X coordinate",
    "y_coord":              "[Float BE] Y coordinate",
    "z_coord":              "[Float BE] Z coordinate",
    "switch_pressed":       "[8-bit] Switch pressed - seems reused and is tied to nearest box? Should be paired with a coordinate box\r\nbit2 - Pressed | 0 - No, 1 - Yes",
    "wormhole_entered":     "[32-bit BE Pointer] Wormhole Pointer\r\n+0xd8: [8-bit] Wormhole\r\n.0x01 - Wormhole has been entered",
}

lines = []
expr_counter = 0

for field in dataclasses.fields(profile):
    name = field.name

    if name in SKIP_FIELDS:
        continue
    if any(name.endswith(s) for s in SKIP_SUFFIXES):
        continue

    value = getattr(profile, field.name)
    if value is None:
        continue

    if isinstance(value, MemoryExpression):
        addr_str = f'0x{expr_counter:02X}'
        lines.append(f'N0:{addr_str}:"[8-bit] [{field.name}] CHANGE THIS - UN-NOTED VARIABLE FOUND"')
        expr_counter += 1
    else:
        value_str = re.sub(r'0x[^0-9a-fA-F]', lambda m: '0x', str(value))
        note = FIELD_NOTES.get(name, f"[{name}] TODO")
        lines.append(f'N0:{value_str}:"{note}"')

output = "\n".join(lines)
print(output)

with open("notes_output.txt", "w") as f:
    f.write(output.replace("\r\n", r"\r\n") + "\n")

print("\nWritten to notes_output.txt")