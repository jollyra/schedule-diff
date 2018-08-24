#!/usr/bin/env python3


from datetime import time


inf = float('inf')


def is_time_within(time_range, time):
    return time_range[0] <= time <= time_range[1]


def invert_schedule(schedule, type='int'):
    if type == 'int':
        range_min = 0
        range_max = inf
    elif type == 'time':
        range_min = time(0)
        range_max = time.max

    if len(schedule) == 0:
        return [(range_min, range_max)]

    inverted_schedule = []

    s, e = schedule[0]
    if s > range_min:
        inverted_schedule.append((range_min, s))

    i = 0
    while i < len(schedule) - 1:
        a0, a1 = schedule[i]
        b0, b1 = schedule[i + 1]
        inverted_schedule.append((a1, b0))
        i += 1

    inverted_schedule.append((schedule[-1][1], range_max))

    return inverted_schedule


def range_intersect(a, b):
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
        raise ValueError('cannot intersect ranges', a, b)


def schedule_intersect(A, B):
    C = []
    for a in A:
        for b in B:
            intersect = range_intersect(a, b)
            if intersect:
                C.append(intersect)
    return C


def schedule_subtract(A, B, type='int'):
    inverse_B = invert_schedule(B, type)
    return schedule_intersect(A, inverse_B)


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

    assert range_intersect((0, 2), (0, 2)) == (0, 2)
    assert range_intersect((0, 2), (0, 3)) == (0, 2)
    assert range_intersect((2, 4), (0, 3)) == (2, 3)
    assert range_intersect((2, 4), (3, 5)) == (3, 4)
    assert range_intersect((0, 2), (0, 1)) == (0, 1)
    assert range_intersect((0, 2), (1, 2)) == (1, 2)
    assert range_intersect((2, 4), (1, 5)) == (2, 4)
    assert range_intersect((0, 3), (1, 2)) == (1, 2)
    assert range_intersect((0, 2), (2, 4)) is None
    assert range_intersect((0, 2), (3, 4)) is None
    assert range_intersect((2, 4), (0, 1)) is None
    assert range_intersect((2, 4), (0, 2)) is None
    print('range_intersect: pass')

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

    print('\ntesting schedules of time objects')
    print(schedule_subtract([(time(9), time(10))], [(time(9), time(9, 30))], type='time'))
    print(schedule_subtract([(time(9), time(10))], [(time(9), time(10))], type='time'))
    print(schedule_subtract([(time(9), time(9, 30))], [(time(9, 30), time(15))], type='time'))
    print(schedule_subtract([(time(9), time(9, 30)), (time(10), time(10, 30))], [(time(9, 15), time(10, 15))], type='time'))
    print(schedule_subtract([(time(9), time(11)), (time(13), time(15))], [(time(9), time(9, 15)), (time(10), time(10, 15)), (time(12, 30), time(16))], type='time'))
