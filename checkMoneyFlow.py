import json
import argparse
import pandas as pd
pd.options.mode.chained_assignment = None
from matplotlib import pyplot
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go

def ReadFinancialBook():
	if args.air:
	    with open('data/financialBook/finBook_AirBank.json', 'r') as filehandle:
	        # book{:} = json.load(filehandle)
	        data = json.load(filehandle)
	else:
		with open('data/financialBook/finBook.json', 'r') as filehandle:
		    # book{:} = json.load(filehandle)
		    data = json.load(filehandle)
	return data

def SaveFinancialBook(book):
    with open('data/financialBook/finBook.json', 'w') as filehandle:
        json.dump(book, filehandle)

def PlotSummary(book):
	dataIn = {}
	dataOut = {}
	dataSum = {}
	for item in book.values():
		key = str(item["year"])+"-"+item["month"]
		if item["paymentType"] == "out":
			if key in dataOut:
				dataOut[key] += item["value"]
			else:
				dataOut[key] = item["value"]
		if item["paymentType"] == "in":
			if key in dataIn:
				dataIn[key] += item["value"]
			else:
				dataIn[key] = item["value"]
		if key in dataSum:
			dataSum[key] += item["value"]
		else:
			dataSum[key] = item["value"]
	seriesOut = pd.Series(data=dataOut)
	seriesOut.sort_index(axis=0,inplace=True)
	seriesOut.plot()
	seriesIn = pd.Series(data=dataIn)
	seriesIn.sort_index(axis=0,inplace=True)
	seriesIn.plot()
	seriesSum = pd.Series(data=dataSum)
	seriesSum.sort_index(axis=0,inplace=True)
	seriesSum.plot()
	pyplot.show()

def PrintOut(book):
	for item in book.values():
		if item["paymentType"] == "out" and item["year"] == 2020 and item["month"] == "09":
		# if item["paymentType"] == "out":
			print(item)

def PrintType(book):
	type = input("Enter type: ")
	for item in book.values():
		if item["identified"] and item["type"] == type:
		# if item["paymentType"] == "out":
			print(item)

def PlotPie(book):
	data = {}
	for item in book.values():
		if item["paymentType"] == "in":
			continue
		key = item["type"] if item["identified"] else "Unidentified"
		if key in data:
			data[key] += -item["value"]
		else:
			data[key] = -item["value"]
	# Pie chart, where the slices will be ordered and plotted counter-clockwise:
	labels = data.keys()
	sizes = data.values()
	# explode = (0, 0.3, 0, 0)  # only "explode" the 2nd slice (i.e. 'Hogs')
	fig1, ax1 = pyplot.subplots()
	ax1.pie(sizes, labels=labels, autopct='%1.1f%%',
	        shadow=True, startangle=90)
	ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

	pyplot.show()

def PrintItems(newDf):
	# print(newDf.loc[(df["date"] == "2020-11") & (df["type"] == "plat")])
	# print(newDf[["date","name","value","who","type","subType"]].loc[(df["date"] == "2021-04") & (df["type"] == "investice")])
	print(newDf[["date","name","value","who","type","subType","place"]].loc[(df["date"] == "2020-04") & (df["type"] == "jidlo")])
	# print(newDf[["date","name","value","who","type","subType"]].loc[(df["type"] == "plat")])

def PlotItems(newDf,df):
	fig = px.pie(newDf, values='value', names='type', title='Population of European continent')
	fig.show()

	fig = px.histogram(df, x="date", y="value")
	fig.show()

	fig = px.histogram(df, x="date", y="value", color="paymentType")
	fig.show()

	fig = px.histogram(newDf, x="date", y="value", color="type")
	fig.show()

	onlyOutFiltered = df.query("type != 'investice' and type != 'vyjimecne' and type != 'splatky' and subType != 'pronajem'")

	# fig = px.bar(onlyOutFiltered, x="date", y="value",color="paymentType")
	# fig = px.histogram(onlyOutFiltered, x="date", y="value")
	fig = px.histogram(onlyOutFiltered, x="date", y="value", color="paymentType")
	# fig = px.histogram(onlyOutFiltered, x="date", y="value")
	fig.show()

def PlotPies(newDf):
	# labels = ["US", "China", "European Union", "Russian Federation", "Brazil", "India",
	          # "Rest of World"]

	# Create subplots: use 'domain' type for Pie subplot
	# fig = make_subplots(rows=4, cols=3, specs=[[{'type':'domain'}, {'type':'domain'}]])
	fig = make_subplots(rows=3, cols=4,specs=[[{'type':'domain'}]*4]*3)
	for monthID in range(1,13):
	# fig.add_trace(go.Pie(labels=["a","b","c","d","e","f"], values=[16, 15, 12, 6, 5, 4, 42]),1,1)
		tempDF = newDf.query("year == 2020 and month == '%02d'" % monthID)
		fig.add_trace(go.Pie(values=tempDF["value"],labels=tempDF["type"]),(monthID-1)//4+1,(monthID-1)%4+1)
	# for x in range(1,13):
		# fig.add_trace(px.pie(newDf, values='value', names='type'),1, x)

	# Use `hole` to create a donut-like pie chart
	# fig.update_traces(hole=.4, hoverinfo="label+percent+name")

	fig.update_layout(
	    title_text="Mesicni procentualni zastoupeni vydaju v jednotlivych mesicich v roce 2020",)
	    # Add annotations in the center of the donut pies.
	    # annotations=[dict(text='GHG', x=0.18, y=0.5, font_size=20, showarrow=False),
	                 # dict(text='CO2', x=0.82, y=0.5, font_size=20, showarrow=False)])
	fig.show()

# Create the parser
my_parser = argparse.ArgumentParser(description='Plots basic money flow graphs')

my_parser.add_argument('-a',
                       '--air',
                       action='store_true',
                       help='read AirBank statement format')

# Execute the parse_args() method
args = my_parser.parse_args()

if __name__ == "__main__":
	book = ReadFinancialBook()
	# PlotSummary(book)
	# PrintOut(book)
	# PlotPie(book)
	# PrintType(book)
	df = pd.DataFrame.from_dict(book, orient='index')
	df["date"] = df["year"].astype(str) + "-" + df["month"]
	newDf = df.query("paymentType == 'out'")
	newDf["value"] = -1*newDf["value"]

	PrintItems(newDf)
	PlotItems(newDf,df)
	PlotPies(newDf)

