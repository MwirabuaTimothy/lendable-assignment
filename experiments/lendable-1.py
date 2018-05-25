import sys
import csv
import time
import operator
import heapq
import pprint

filename = sys.argv[1]
numberOfClients = sys.argv[2]
pp = pprint.PrettyPrinter(indent=1,depth=2,compact=True)

with open(filename, 'r') as csvfile:

	# skip first line, headers
	next(csvfile)
	reader = csv.reader(csvfile)

	# 1. sort csv by date, ignore row 1
	dateColumn = 2
	filteredRows = filter(lambda x: len(x) > dateColumn, reader)
	# sortedRows = sorted(filteredRows, key=lambda row: time.strptime(row[2].strip(), "%m/%d/%y %H:%M:%S"), reverse=False)
	sortedRows = sorted(filteredRows, key=lambda row: time.strptime(row[2].strip(), "%Y-%m-%d %H:%M:%S"), reverse=False)
	# pp.pprint(sortedRows)

	# save streaks
	streaks = {}
	previousAccount = ''
	for i, row in enumerate(sortedRows):
		account = row[0]
		if account in streaks:
			if previousAccount == account: # consecutive
				streaks[account][-1] +=1 # increment last streak
			else:
				streaks[account].append(1) # broke streak or no streak
		else:
			streaks[account] = [1]
		previousAccount = account
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
