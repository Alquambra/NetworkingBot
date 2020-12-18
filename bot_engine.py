# -*- coding: utf-8 -*-
# Python 3.8.6

from collections import defaultdict
import random


def create_pairs(dict_with_previous_meetings, taking_part_users):
    current_pairs = defaultdict(list)
    partner = None
    iters = []

    for user in taking_part_users:
        if user in iters:
            continue
        for_choice = list(set(taking_part_users) - {user} - set(dict_with_previous_meetings[str(user)]))

        if for_choice:
            partner = random.choice(for_choice)
            dict_with_previous_meetings[str(user)].append(partner)
            dict_with_previous_meetings[str(partner)].append(str(user))
            current_pairs[str(user)].append(partner)
            current_pairs[str(partner)].append(str(user))
        else:
            dict_with_previous_meetings[str(user)].append(None)
            current_pairs[str(user)].append(None)
        taking_part_users = list(set(taking_part_users) - {partner} - {user})
        iters.append(user and partner)
    return current_pairs
