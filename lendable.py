import sys, csv, time, heapq, pprint
from datetime import datetime, timedelta

filename = sys.argv[1]
numberOfClients = sys.argv[2]
pp = pprint.PrettyPrinter(indent=1,depth=3,compact=True)

with open(filename, 'r') as csvfile:

		# skip first line - headers
		next(csvfile)
		reader = csv.reader(csvfile)

		# sort csv by dateTime
		sortedRows = sorted(reader, key=lambda row: time.strptime(row[2].strip(), "%Y-%m-%d %H:%M:%S"), reverse=False)
		# pp.pprint(sortedRows)

		# analyze frequency / streaks
		streaks = {}
		dates = {}
		for i, row in enumerate(sortedRows):
				account = row[0]
				dateString = row[2].strip().split(' ')[0]
				date = datetime.strptime(dateString, "%Y-%m-%d")
				aDayAgo = (date - timedelta(days=1)).strftime('%Y-%m-%d')
				if account in streaks:
						previousDate = dates[account][-1]
						# print(previousDate, account)
						if previousDate == dateString:
								continue # skip same-day deposits from same user 
						if previousDate == aDayAgo:
								streaks[account][-1] += 1 # increment streak
						else:
								streaks[account].append(1) # start new streak
						dates[account].append(dateString)
				else:
						streaks[account] = [1]
						dates[account] = [dateString]
				# print(dates[account])
		# pp.pprint(streaks)
		
		rank = {}
		for account, streak in streaks.items():
				streak = streaks[account]
				rank[account] = max(streak)
		# print(rank)

		# sort rank by values and sort ties alphabetically
		topN = heapq.nsmallest(int(numberOfClients), rank.items(), key=lambda kv: (-kv[1], kv[0]))
		# print(topN)

		# return the keys
		ids = list(dict(topN).keys())
		print(ids)

