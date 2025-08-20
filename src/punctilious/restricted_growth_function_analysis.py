# import math
import sympy.functions.combinatorial.numbers


def generate_erratic_dyck_path_sequence(max_steps, max_value, retrieve_sequence=True, retrieve_combinations=False):
    """Computes the combinations of sequences of n natural numbers such that:
    - n_1 = 1
    - 1 <= n_i < max(union(n_k, k=1, n-1))

    A constraint parameter `max_value` can be defined such that:
    - n_i <= max_value

    Without the max_value constraint, the number of combinations is equal to the Bell numbers.

    With the max_value constraint:
    - The number of combinations that are made impossible because of the constraint is (per max_value):
        (0, 1, 4, 14, 51, 202, 876, 4139, 21146, 115974, 678569),
        (0, 0, 1, 7, 36, 171, 813, 4012, 20891, 115463, 677546),
        (0, 0, 0, 1, 11, 81, 512, 3046, 17866, 106133, 649045),
        (0, 0, 0, 0, 1, 16, 162, 1345, 10096, 72028, 503295),
        (0, 0, 0, 0, 0, 1, 22, 295, 3145, 29503, 256565),
        (0, 0, 0, 0, 0, 0, 1, 29, 499, 6676, 77078),
        (0, 0, 0, 0, 0, 0, 0, 1, 37, 796, 13091),
        (0, 0, 0, 0, 0, 0, 0, 0, 1, 46, 1211),
        (0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 56),
        (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1),
        (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)




    :param max_steps:
    :param max_value:
    :param retrieve_sequence:
    :param retrieve_combinations:
    :return:
    """

    def take_step(precedent_path, max_steps, max_value: int | None = None,
                  combinations: dict[int, set[tuple[int]]] | None = None,
                  counters: list[int] | None = None):
        precedent_length = len(precedent_path)
        precedent_max_index = max(precedent_path)
        current_length = precedent_length + 1
        while counters is not None and len(counters) < current_length:
            counters.append(0)
        if combinations is not None and current_length not in combinations.keys():
            combinations[current_length] = set()
        current_max_index = precedent_max_index + 1
        if max_value is not None:
            current_max_index = min(current_max_index, max_value)
        for x in range(1, current_max_index + 1):
            new_path = precedent_path + (x,)
            if combinations is not None:
                combinations[current_length] = combinations[current_length] | {new_path}
            if counters is not None:
                counters[current_length - 1] = counters[current_length - 1] + 1
            if len(precedent_path) < max_steps:
                take_step(new_path, max_steps, max_value, combinations=combinations, counters=counters)

    path = (1,)
    counters = [1, ] if retrieve_sequence else None
    combinations = dict() if retrieve_combinations else None
    take_step(path, max_steps=max_steps, max_value=max_value, combinations=combinations, counters=counters)
    # These are the Bell numbers
    return counters, combinations


def test_1():
    b_n = tuple(sympy.functions.combinatorial.numbers.bell(n) for n in range(1, 12))
    minus = list()

    for max_value in range(1, 12):
        counters, combinations = generate_erratic_dyck_path_sequence(
            max_steps=11,
            max_value=max_value,
            retrieve_sequence=True,
            retrieve_combinations=False)
        # print(combinations)
        print(f"algo result with max_value:{max_value} : {counters}")
        minus.append(tuple(x - y for x, y in zip(b_n, counters)))

    print(str(minus).replace("[", "\n").replace("]", ""))


# test_1()

def test_2():
    counters, combinations = generate_erratic_dyck_path_sequence(
        max_steps=12,
        max_value=4,
        retrieve_sequence=True,
        retrieve_combinations=False)
    print(counters)


test_2()
