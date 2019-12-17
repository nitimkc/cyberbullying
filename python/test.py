r = requests.get("https://api.coindesk.com/v1/bpi/historical/close.json?start=2012-01-01&end=2018-09-05")
x = r.json()['bpi'].keys()
y = r.json()['bpi'].values()
# print(x)
# print(y)
x = list(x)
y = list(y)

plt.plot(x, y)