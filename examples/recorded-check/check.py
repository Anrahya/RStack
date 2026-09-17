from app import sorted_unique

original = [3, 1, 3, 2]
assert sorted_unique(original) == [1, 2, 3]
assert original == [3, 1, 3, 2]
assert sorted_unique([]) == []
print('Public sorting and non-mutation assertions passed.')
