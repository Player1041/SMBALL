from profiles.smb2 import default_smb2_profile
from profiles import GameProfile

_REGISTRY: dict[str, object] = {
    "Gaiden":   default_smb2_profile,
    "349":      default_smb2_profile,
    "651":      default_smb2_profile
}

def get_profile(game: str) -> GameProfile:
    if game not in _REGISTRY:
        raise KeyError(f"[ERROR] No profile registered for {game}. Known games: {list(_REGISTRY.keys())}")
    return _REGISTRY[game]