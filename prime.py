def generate_numbers(limit):
    numbers = []
    for n in range(1, limit + 1):
        if n % 6 == 1 or n % 6 == 5:
            numbers.append(n)
    return numbers

limit = 100
result = generate_numbers(limit)
print(result)
