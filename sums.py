import sys
import itertools
import argparse


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


parser = argparse.ArgumentParser(
    description=f"{bcolors.WARNING}Sudoku sum combinations{bcolors.ENDC}")
parser.add_argument(
    "-f", type=str, help=f"{bcolors.OKBLUE}Filter sums including ['inc'] or excluding ['exc]. Default 'none'{bcolors.ENDC}", default="none")
parser.add_argument("-fnums", type=int, nargs='+',
                    help=f"{bcolors.OKCYAN}list of numbers to include in filter{bcolors.ENDC}")
parser.add_argument("sum", type=int, help=f"{bcolors.OKCYAN}Sum{bcolors.ENDC}")
parser.add_argument("-d", type=int,
                    default=-1, help=f"{bcolors.OKGREEN}Number of digits in sum{bcolors.ENDC}")


def get_all_combos(s, d, f_type='none', f_nums=None):
    # initialize f_nums if default
    if f_nums is None:
        f_nums = []
    poss_nums = []

    # add possible numbers to array
    # handles excluding filter condition upfront
    for i in range(1, 10):
        if f_type == 'exc' and i not in f_nums:
            poss_nums.append(i)
        elif f_type != 'exc':
            poss_nums.append(i)

    # creates all combinations
    # if d == -1 (any combination allowed), run through all iterations
    # if d != -1 (only d length combinations allowed), only run when i == d
    mostly_final = set()
    for i in range(1, 10):
        if d != -1 and i != d:
            continue

        c = list(itertools.combinations(poss_nums, i))
        all_combos = set(c)

        for combo in all_combos:
            if sum(combo) == s:
                mostly_final.add(combo)

    # if inclusive filter active, make sure each combo has at least one of the included filter numbers
    num_set = set(f_nums)
    final = set()
    if f_type == 'inc':
        for fin in mostly_final:
            fin_set = set(fin)
            if len(fin_set) != len(fin_set-num_set):
                final.add(fin)
    else:
        final = mostly_final

    return final


if __name__ == "__main__":
    # parse args
    args = parser.parse_args()

    # run get_all_combos
    ret = get_all_combos(args.sum, args.d, args.f, args.fnums)

    # print results
    filter_msg = f" and include {args.fnums}" if args.f == 'inc' else f"and exclude {args.fnums}"
    digits_msg = f" that consist of {args.d} digits."
    print(f"{bcolors.OKGREEN}All combinations of numbers that{bcolors.ENDC} {bcolors.OKBLUE}sum to {args.sum}{bcolors.ENDC}{bcolors.WARNING}{filter_msg if args.f != 'none' else ''}{bcolors.ENDC}{bcolors.HEADER}{digits_msg if args.d != -1 else ''}{bcolors.ENDC}")
    print(f"{bcolors.OKCYAN}{ret}{bcolors.ENDC}")
