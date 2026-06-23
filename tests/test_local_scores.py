from local_scores import merge_sort_scores, _merge

class TestLocalScores:
    def test_merge_sort_empty_returns_empty_array(self):
        arr = []
        assert merge_sort_scores(arr) == []

    def test_merge_sort_empty_returns_sorted_array(self):
        arr = [{"username": "a", "score": 999},
               {"username": "b", "score": 12},
               {"username": "c", "score": 213},
               {"username": "d", "score": 9999},
               {"username": "e", "score": 1111},
               {"username": "f", "score": 0}]

        sorted_arr = [{"username": "d", "score": 9999},
               {"username": "e", "score": 1111},
               {"username": "a", "score": 999},
               {"username": "c", "score": 213},
               {"username": "b", "score": 12},
               {"username": "f", "score": 0}]

        assert merge_sort_scores(arr) == sorted_arr

    def test_merge_sort_returns_same_array_if_already_sorted(self):
        sorted_arr = [{"username": "d", "score": 9999},
               {"username": "e", "score": 1111},
               {"username": "a", "score": 999},
               {"username": "c", "score": 213},
               {"username": "b", "score": 12},
               {"username": "f", "score": 0}]
        assert merge_sort_scores(sorted_arr) == sorted_arr

    def test_merge_function_returns_merged(self):
        left = [{"username": "test", "score":99}]
        right = [{"username": "test", "score": 100}]

        expected = [{"username":"test", "score":100}, {"username": "test", "score":99}]
        assert _merge(left, right) == expected


