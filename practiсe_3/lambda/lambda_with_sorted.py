#1
pairs = [(1, 'one'), (2, 'two'), (3, 'three'), (4, 'four')]
pairs.sort(key=lambda pair: pair[1])
print(pairs)

#2
ids = ['id1', 'id20', 'id3', 'id10']
sorted_ids = sorted(ids, key=lambda x: int(x[2:]))
print(sorted_ids)

#3
data = [{"name": "Max", "age": 20}, {"name": "Bob", "age": 15}]
sorted_data = sorted(data, key=lambda x: x["age"])
print(sorted_data)

#4
words = ["apple", "Kiwi", "banana", "Orange"]
print(sorted(words, key=lambda x: x.lower()))

#5
points = [(1, 2), (3, 1), (5, 0)]
print(sorted(points, key=lambda p: p[1]))