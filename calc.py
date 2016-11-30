import csv
from collections import OrderedDict
from decimal import Decimal
import datetime

import matplotlib
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

output_filename = 'output/combined.csv'
trendline_both_output_filename = 'output/trendline_both.png'
trendline_north_output_filename = 'output/trendline_north.png'
trendline_south_output_filename = 'output/trendline_south.png'
input_north_filename = 'data/NH_seaice_extent_final_v2.csv'
input_north_2016_filename = 'data/NH_seaice_extent_nrt_v2.csv'
input_south_filename = 'data/SH_seaice_extent_final_v2.csv'
input_south_2016_filename = 'data/SH_seaice_extent_nrt_v2.csv'

data = {}
list_of_years = []

# Pull data from 1978-2015
with open(input_north_filename) as csvfile:
	north_reader = csv.DictReader(csvfile, skipinitialspace=True)
	for row in north_reader:
		# Skip the example formatting line
		if row['Year'] == 'YYYY':
			continue

		date = (row['Year'], row['Month'], row['Day'])
		extent = row['Extent']

		if date not in data:
			data[date] = {}

		data[date]['north'] = extent

		if row['Year'] not in list_of_years:
			list_of_years.append(row['Year'])

# Pull data from 2016
with open(input_north_2016_filename) as csvfile:
	north_reader = csv.DictReader(csvfile, skipinitialspace=True)
	for row in north_reader:
		# Skip the example formatting line
		if row['Year'] == 'YYYY':
			continue

		date = (row['Year'], row['Month'], row['Day'])
		extent = row['Extent']

		if date not in data:
			data[date] = {}

		data[date]['north'] = extent

		if row['Year'] not in list_of_years:
			list_of_years.append(row['Year'])

# Pull data from 1978-2015
with open(input_south_filename) as csvfile:
	south_reader = csv.DictReader(csvfile, skipinitialspace=True)
	for row in south_reader:
		# Skip the example formatting line
		if row['Year'] == 'YYYY':
			continue

		date = (row['Year'], row['Month'], row['Day'])
		extent = row['Extent']

		if date not in data:
			data[date] = {}

		data[date]['south'] = extent

		if row['Year'] not in list_of_years:
			list_of_years.append(row['Year'])

# Pull data from 2016
with open(input_south_2016_filename) as csvfile:
	south_reader = csv.DictReader(csvfile, skipinitialspace=True)
	for row in south_reader:
		# Skip the example formatting line
		if row['Year'] == 'YYYY':
			continue

		date = (row['Year'], row['Month'], row['Day'])
		extent = row['Extent']

		if date not in data:
			data[date] = {}

		data[date]['south'] = extent

		if row['Year'] not in list_of_years:
			list_of_years.append(row['Year'])

for date in data.keys():
	north_extent = data[date]['north'] if 'north' in data[date] else 0
	south_extent = data[date]['south'] if 'south' in data[date] else 0
	total = Decimal(north_extent) + Decimal(south_extent)
	data[date]['total'] = str(total)

ordered = OrderedDict(sorted(data.items(), key=lambda t: t[0]))

'''
with open(output_filename, 'w') as outfile:
	header = "Year,Month,Day,NorthExtent,SouthExtent,TotalExtent\n"
	outfile.write(header)
	for date, info_dict in ordered.items():
		row = ','.join([date[0], date[1], date[2], info_dict['north'], info_dict['south'], info_dict['total']])
		outfile.write(row)
		outfile.write("\n")
'''

# Setup the trendline data in the structure we need for plotting
trendline_data = {}
for y in list_of_years:
	trendline_data[y] = {'date': [], 'total_extent': [], 'north_extent': [], 'south_extent': []}
for date, data in ordered.items():
	year = date[0]
	trendline_data[year]['date'].append(date)
	trendline_data[year]['total_extent'].append(data['total'])
	trendline_data[year]['north_extent'].append(data['north'])
	trendline_data[year]['south_extent'].append(data['south'])

# Setup the formatting for the axes
months = mdates.MonthLocator()  # every month
monthsFmt = mdates.DateFormatter('%m')

# Generate the combined ice coverage plot
fig, ax = plt.subplots()

ax.set_title('Global (North && South) Ice Extent')

for y in list_of_years:
	# Pull the aggregate data for the current year
	year_data = trendline_data[y]

	# We finagle the year for the date of each datapoint so that we can get them to all display overlaid on top of each other
	dates_list = [datetime.date(2016, int(x[1]), int(x[2])) for x in year_data['date']]

	# We want to plot the total extent data here
	total_extent_list = year_data['total_extent']

	# Set the line color
	if y == '2016':
		line_color = 'red'
		legend_label = y
	elif y == '2015':
		line_color = 'green'
		legend_label = y
	elif y == '2014':
		line_color = 'black'
		legend_label = 'All Other Years'
	else:
		line_color = 'black'
		legend_label = ''

	# Plot the datapoints for the current year
	ax.plot_date(dates_list, total_extent_list, color=line_color, label=legend_label)

# Format the ticks
ax.xaxis.set_major_locator(months)
ax.xaxis.set_major_formatter(monthsFmt)

datemin = datetime.date(2016, 1, 1)
datemax = datetime.date(2016 + 1, 1, 1)
ax.set_xlim(datemin, datemax)

# Format the coords message box
def area(x):
	return '{}'.format(x)
ax.format_xdata = mdates.DateFormatter('%b')
ax.format_ydata = area
ax.grid(True)

# Rotates and right aligns the x labels, and moves the bottom of the
# axes up to make room for them
fig.autofmt_xdate()

# Add a legend for the trendlines
ax.legend(loc='best')

# Save the plot
plt.savefig(trendline_both_output_filename)


# Generate the north ice coverage plot
fig, ax = plt.subplots()

ax.set_title('North Ice Extent')

for y in list_of_years:
	# Pull the aggregate data for the current year
	year_data = trendline_data[y]

	# We finagle the year for the date of each datapoint so that we can get them to all display overlaid on top of each other
	dates_list = [datetime.date(2016, int(x[1]), int(x[2])) for x in year_data['date']]

	# We want to plot the total extent data here
	north_extent_list = year_data['north_extent']

	# Set the line color
	if y == '2016':
		line_color = 'red'
		legend_label = y
	elif y == '2015':
		line_color = 'green'
		legend_label = y
	elif y == '2014':
		line_color = 'black'
		legend_label = 'All Other Years'
	else:
		line_color = 'black'
		legend_label = ''

	# Plot the datapoints for the current year
	ax.plot_date(dates_list, north_extent_list, color=line_color, label=legend_label)

# Format the ticks
ax.xaxis.set_major_locator(months)
ax.xaxis.set_major_formatter(monthsFmt)

datemin = datetime.date(2016, 1, 1)
datemax = datetime.date(2016 + 1, 1, 1)
ax.set_xlim(datemin, datemax)

# Format the coords message box
def area(x):
	return '{}'.format(x)
ax.format_xdata = mdates.DateFormatter('%b')
ax.format_ydata = area
ax.grid(True)

# Rotates and right aligns the x labels, and moves the bottom of the
# axes up to make room for them
fig.autofmt_xdate()

# Add a legend for the trendlines
ax.legend(loc='best')

# Save the plot
plt.savefig(trendline_north_output_filename)


# Generate the south ice coverage plot
fig, ax = plt.subplots()

ax.set_title('South Ice Extent')

for y in list_of_years:
	# Pull the aggregate data for the current year
	year_data = trendline_data[y]

	# We finagle the year for the date of each datapoint so that we can get them to all display overlaid on top of each other
	dates_list = [datetime.date(2016, int(x[1]), int(x[2])) for x in year_data['date']]

	# We want to plot the total extent data here
	south_extent_list = year_data['south_extent']

	# Set the line color
	if y == '2016':
		line_color = 'red'
		legend_label = y
	elif y == '2015':
		line_color = 'green'
		legend_label = y
	elif y == '2014':
		line_color = 'black'
		legend_label = 'All Other Years'
	else:
		line_color = 'black'
		legend_label = ''

	# Plot the datapoints for the current year
	ax.plot_date(dates_list, south_extent_list, color=line_color, label=legend_label)

# Format the ticks
ax.xaxis.set_major_locator(months)
ax.xaxis.set_major_formatter(monthsFmt)

datemin = datetime.date(2016, 1, 1)
datemax = datetime.date(2016 + 1, 1, 1)
ax.set_xlim(datemin, datemax)

# Format the coords message box
def area(x):
	return '{}'.format(x)
ax.format_xdata = mdates.DateFormatter('%b')
ax.format_ydata = area
ax.grid(True)

# Rotates and right aligns the x labels, and moves the bottom of the
# axes up to make room for them
fig.autofmt_xdate()

# Add a legend for the trendlines
ax.legend(loc='best')

# Save the plot
plt.savefig(trendline_south_output_filename)
