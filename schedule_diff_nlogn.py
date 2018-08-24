#!/usr/bin/env python3


from collections import defaultdict
from datetime import time


inf = float('inf')


def chunks(xs, n):
    chunks = []
    for i in range(0, len(xs), n):
        chunks.append(xs[i:i + n])
    return chunks


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


def add_markers(marker_timeline, A):
    for a in A:
        s, e = a
        marker_timeline[s] += 1
        marker_timeline[e] -= 1


def create_marker_timeline(A, B):
    marker_timeline = defaultdict(int)
    add_markers(marker_timeline, A)
    add_markers(marker_timeline, B)
    timeline = [(k, v) for k, v in marker_timeline.items()]
    return sorted(timeline, key=lambda x: x[0])


def schedule_intersect(A, B):
    marker_timeline = create_marker_timeline(A, B)
    schedule = []
    acc = 0
    for time, marker in marker_timeline:
        if acc == 2:
            schedule.append(time)
        acc += marker
        if acc == 2:
            schedule.append(time)
    schedule = [tuple(chunk) for chunk in chunks(schedule, 2)]
    return schedule


def schedule_subtract(A, B):
    inverted_B = invert_schedule(B)
    return schedule_intersect(A, inverted_B)


if __name__ == '__main__':
    assert schedule_subtract([], [(3, 5)]) == []
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
