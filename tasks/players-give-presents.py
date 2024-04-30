from random import choice


def players_give_presents(players: list[str]) -> list[tuple[str, str]]:
    result_pairs: list[tuple[str, str]] = []

    possible_givers, possible_getters = set(players), set(players)

    for player in players:
        if len(possible_givers) == 1 and possible_getters == possible_givers:
            return players_give_presents(players)

        if player in possible_givers:
            possible_givers.remove(player)

            while (getter := choice(list(possible_getters))) == player:
                pass
            possible_getters.remove(getter)

            result_pairs.append((player, getter))
        if player in possible_getters:
            possible_getters.remove(player)

            while (giver := choice(list(possible_givers))) == player:
                pass
            possible_givers.remove(giver)
            result_pairs.append((giver, player))

    return result_pairs


print(players_give_presents(["Ivan", "Tom", "Sam", "Mark", "Antony", "Samuel"]))
