def chunks(lst, n):
  for i in range(0, len(lst),n):
    yield lst[i:i + n]

def portfolio_input():
  portfolio_size = input('Enter the size of your portfolio: ')

  try:
    val = float(portfolio_size)
    return val
  except:
    print('That is not a number')
    portfolio_input()