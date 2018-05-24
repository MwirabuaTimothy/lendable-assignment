import sys, csv, time, heapq, pprint

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

		# save streaks
		dateGroups = {}
		streaks = {}
		previousAccount = ''
		for i, row in enumerate(sortedRows):
				account = row[0]
				date = row[2].strip().split(' ')[0]
				if account in dateGroups:
						if previousAccount == account: # consecutive
								dateGroups[account][-1].append(date) # increment last streak
						else:
								dateGroups[account].append([date]) # broke streak or no streak
				else:
						dateGroups[account] = [[date]]
						streaks[account] = []
				
				previousAccount = account
		# pp.pprint(dateGroups)
		# pp.pprint(streaks)
		
		# filter payments of same date
		for account in dateGroups:
				for dateGroup in dateGroups[account]:
						filteredDates = list(set(dateGroup))
						streaks[account].append(len(filteredDates))
		# pp.pprint(dateGroups)
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

