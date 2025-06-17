def find_ideal_direction(latitude):
    if latitude > 5:
        return 180  # True South
    elif latitude < -5:
        return 0  # True North
    else:
        return 90


print(find_ideal_direction(-82))
