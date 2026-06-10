from profiles.addresses import get_profile

ctx = get_profile("Gaide")

print(ctx.bananas_remaining)

print(ctx.world)