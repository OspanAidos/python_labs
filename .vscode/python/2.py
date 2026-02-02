a=int(input())
b=list(map(int, input().split()))
b.sort(reverse=True)
for i in b:
    print(i, end=" ")