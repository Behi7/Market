def n_numbers(num):
  result = ""
  for i in range(1, num + 1):
    result += str(i) * i
  return result

n= int(input('введите число: '))
print(n_numbers(n))

    