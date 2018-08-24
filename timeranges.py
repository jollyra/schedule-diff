#!/usr/bin/env python3


from datetime import time


inf = float('inf')


def is_time_within(time_range, time):
    return time_range[0] <= time <= time_range[1]


def invert_schedule(schedule):
    if len(schedule) == 0:
        return [(0, inf)]

    inverted_schedule = []

    s, e = schedule[0]
    if s > 0:
        inverted_schedule.append((0, s))

    i = 0
    while i < len(schedule) - 1:
        a0, a1 = schedule[i]
        b0, b1 = schedule[i + 1]
        inverted_schedule.append((a1, b0))
        i += 1

    inverted_schedule.append((schedule[-1][1], inf))

    return inverted_schedule


def range_union(a, b):
    a0, a1 = a
    b0, b1 = b
    if a == b:
        # a0----a1
        # b0----b1
        return a
    elif is_time_within(b, a0) and is_time_within(b, a1):
        #    a0----a1
        # b0----------b1
        return a
    elif a1 <= b0 or a0 >= b1:
        # a0----a1
        #            b0----b1
        return None
    elif is_time_within(a, b0) and a1 <= b1 and a1 != b0:
        # a0--------a1
        #      b0---------b1
        return (b0, a1)
    elif is_time_within(a, b1) and b0 <= a0 and a0 != b1:
        #      a0--------a1
        # b0---------b1
        return (a0, b1)
    elif is_time_within(a, b0) and is_time_within(a, b1):
        # a0------------a1
        #     b0----b1
        return b
    else:
        print('error: cannot union ranges', a, b)


def schedule_union(A, B):
    C = []
    for a in A:
        for b in B:
            union = range_union(a, b)
            if union:
                C.append(union)
    return C


def schedule_subtract(A, B):
    inverse_B = invert_schedule(B)
    return schedule_union(A, inverse_B)


if __name__ == '__main__':
    assert invert_schedule([(0, 1), (2, 3), (9, 11)]) == [(1, 2), (3, 9), (11, inf)]
    assert invert_schedule([(2, 3), (9, 11)]) == [(0, 2), (3, 9), (11, inf)]
    assert invert_schedule([(3, 5)]) == [(0, 3), (5, inf)]
    assert invert_schedule([]) == [(0, inf)]
    print('invert_schedule: pass')
    assert is_time_within((2, 4), 2) is True
    assert is_time_within((2, 4), 4) is True
    assert is_time_within((2, 4), 3) is True
    assert is_time_within((2, 4), 5) is False
    print('is_time_within: pass')
    assert range_union((0, 2), (0, 2)) == (0, 2)
    assert range_union((0, 2), (0, 3)) == (0, 2)
    assert range_union((2, 4), (0, 3)) == (2, 3)
    assert range_union((2, 4), (3, 5)) == (3, 4)
    assert range_union((0, 2), (0, 1)) == (0, 1)
    assert range_union((0, 2), (1, 2)) == (1, 2)
    assert range_union((2, 4), (1, 5)) == (2, 4)
    assert range_union((0, 3), (1, 2)) == (1, 2)
    assert range_union((0, 2), (2, 4)) is None
    assert range_union((0, 2), (3, 4)) is None
    assert range_union((2, 4), (0, 1)) is None
    assert range_union((2, 4), (0, 2)) is None
    print('range_union: pass')
    assert schedule_subtract([(0, 2)], [(3, 5)]) == [(0, 2)]
    assert schedule_subtract([(0, 2)], [(0, 2)]) == []
    assert schedule_subtract([(2, 4)], [(0, 3)]) == [(3, 4)]
    assert schedule_subtract([(2, 4)], [(3, 5)]) == [(2, 3)]
    assert schedule_subtract([(0, 2)], [(0, 1)]) == [(1, 2)]
    assert schedule_subtract([(0, 2)], [(1, 2)]) == [(0, 1)]
    assert schedule_subtract([(2, 4)], [(1, 5)]) == []
    assert schedule_subtract([(0, 3)], [(1, 2)]) == [(0, 1), (2, 3)]
    assert schedule_subtract([(9, 10)], [(9, 10)]) == []
    assert schedule_subtract([(0, 2), (4, 6)], [(1, 5)]) == [(0, 1), (5, 6)]
    assert schedule_subtract([(0, 4)], [(0, 1), (2, 5)]) == [(1, 2)]
    assert schedule_subtract([(0, 4)], [(0, 1), (2, 3)]) == [(1, 2), (3, 4)]
    assert schedule_subtract([(0, 4), (7, 10)], [(0, 1), (2, 3), (9, 11)]) == [(1, 2), (3, 4), (7, 9)]
    print('pass')
