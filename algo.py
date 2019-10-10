import pandas as pd

# two solutions to the max profit with k transactions
# the first solution is mine with pandas (not as elegant but makes more sense to me, easier to understand)
# second solution is from algoexpert.io ... wow super clean code



# beginning of my solution in pandas
# get the begin/end trade on same row
# value_grp = group rows together that could be lumped into 1 trade
# group by value_grp
# sort by best trade and return sum of top n rows

def label_slope(row):
  if (row['index1']==0): return -1
  if (row['price2']>=row['price']): return 1
  else: return 0

def label_profit(row): return row['price2'] - row['price']

def max_profit(prices, k):
  prices.insert(0,0)
  df = pd.DataFrame(prices,columns =['price'])
  df['price2'] = df['price']
  df.price2 = df.price.shift(-1)
  df['index1'] = df.index
  df['theslope'] = df.apply (lambda row: label_slope(row), axis=1)
  df = df.iloc[1:,]
  df = df.iloc[:-1,]
  df['value_grp'] = (df.theslope.diff(1) != 0).astype('int').cumsum()
  #print(df)

  gk = pd.DataFrame({'price' : df.groupby(['value_grp', 'theslope']).price.first(),
                'price2' : df.groupby(['value_grp', 'theslope']).price2.last(),
                'Consecutive' : df.groupby(['value_grp', 'theslope']).size()}).reset_index(drop=True)

  gk['theprofit'] = gk.apply (lambda row: label_profit(row), axis=1)
  #print('.')
  #print(gk)
  gk = gk.nlargest(k, 'theprofit')
  return gk['theprofit'].sum()


theanswer = max_profit([5,11,3,50,10,90], 3)
#theanswer = max_profit([5,11,3,50,60,90], 2)
print(theanswer)


exit()

# very elegant and fast!  (algoexpert.io)
def maxprofit(prices, k):
  if not len(prices): return 0
  fn_profits = [[0 for d in prices] for t in range(k+1)]
  fn_maxthusfar1 = [[0 for d in prices] for t in range(k+1)]
  for t in range(1, k+1): #2 trades (t) going from 1..3
    #maxthusfar = float("-inf")
    br_maxthusfar = -100000

    for d in range(1, len(prices)):
      br_profits_other_trade = fn_profits[t-1][d-1]
      br_profits_this_trade = fn_profits[t][d-1]
      br_prices_yesterday = prices[d-1]
      br_prices_today = prices[d]

      br_maxthusfar = max(br_maxthusfar, br_profits_other_trade - br_prices_yesterday)
      fn_profits[t][d] = max(br_profits_this_trade, br_maxthusfar + br_prices_today)
      fn_maxthusfar1[t][d] = br_maxthusfar
  for a in fn_profits: print(a)
  return fn_profits[k][-1]

abc = maxprofit([5,11,3,50,10,90], 3)
#abc = maxprofit([90, 80, 70, 60], 2)
print(abc)

# think of maxthusfar as the cheapest buy in adjusted for profits accrued

"""
a = {list} <class 'list'>: [0, 6, 6, 53, 53, 133]
br_maxthusfar = {int} 43
br_prices_today = {int} 90
br_prices_yesterday = {int} 10
br_profits_other_trade = {int} 53
br_profits_this_trade = {int} 53
d = {int} 5
fn_maxthusfar1 = {list} <class 'list'>: [[0, 0, 0, 0, 0, 0], [0, -5, -5, -3, -3, -3], [0, -5, -5, 3, 3, 37], [0, -5, -5, 3, 3, 43]]
fn_profits = {list} <class 'list'>: [[0, 0, 0, 0, 0, 0], [0, 6, 6, 47, 47, 87], [0, 6, 6, 53, 53, 127], [0, 6, 6, 53, 53, 133]]
k = {int} 3
prices = {list} <class 'list'>: [5, 11, 3, 50, 10, 90]
t = {int} 3
"""
