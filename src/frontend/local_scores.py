import json
from .constants import LOCAL_SCORES

def _get_scores(file: str) -> list[dict]:
    try:
        with open(file, 'r') as f:
            scores = json.load(f)
        return scores
    except FileNotFoundError:
        return [{}]

def _merge(left: list[dict], right: list[dict]) -> list[dict]:
    result = []
    i = j = 0

    # compare score values from both lists, add smaller element and shift pointer by one
    while i < len(left) and j < len(right):
        if left[i]["score"] > right[j]["score"]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    # add remaining chunk of elements straight away, as it is already sorted
    result.extend(left[i:])
    result.extend(right[j:])
    return result

def merge_sort_scores(arr:list[dict]) -> list[dict]:
    # base case: list has only one element (cannot be broken down further)
    if len(arr) <= 1:
        return arr

    # step 1: find middle element, left half, right half
    mid = len(arr) // 2
    left = arr[:mid]
    right = arr[mid:]

    # step 2: use recursion to keep diving and merging
    left = merge_sort_scores(left)
    right = merge_sort_scores(right)

    # step 3: merge halves
    return _merge(left, right)

def get_top_score() -> list[dict]:
    scores = _get_scores(LOCAL_SCORES)
    sorted_scores = merge_sort_scores(scores)
    return sorted_scores[:1]
