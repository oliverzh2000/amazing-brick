def do_lines_intersect(((ax1, ay1), (ax2, ay2)), ((bx1, by1), (bx2, by2))):
    """
    This function assumes line a to be vertical or horizontal,
    and that line b is diagonal (has slope 1 or -1)
    """
    # line a is vertical
    m = 1 if float(by1 - by2)/(bx1 - bx2) > 0 else -1 # m is slope of line b
    if ax1 == ax2:
        intx, inty = ax1, m * ax1 + by1 - m * bx1
        if (min(by1, by2) <= inty <= max(ay1, ay2) and min(ay1, ay2) <= inty <= max(by1, by2)
            and min(bx1, bx2) <= intx <= max(bx1, bx2)):
            return True
    # line a is horizontal
    else:
        intx, inty = (ay1 - by1 + m * bx1) / m, ay1
        print intx, inty
        if (min(bx1, bx2) <= intx <= max(ax1, ax2) and min(ax1, ax2) <= intx <= max(bx1, bx2)
                and min(by1, by2) <= inty <= max(by1, by2)):
            return True
    return False

print do_lines_intersect(((800, 281), (447, 281)), ((535, 280), (515, 300)))