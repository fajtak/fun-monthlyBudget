import tabula
from PyPDF2 import PdfFileWriter, PdfFileReader
import json
import argparse

debug = False
# debug = True

def GetTheLastPage(numPages,fileName):
	for pageID in range(numPages,0,-1):
		if args.air:
			dataFrame = tabula.read_pdf(fileName,pages=pageID,area=[5.0,0.0,9.,100.],relative_area=True)
		else:
			dataFrame = tabula.read_pdf(fileName,pages=pageID,area=[17.0,0.0,20.,100.],relative_area=True)
		if debug:
			print("Debug - DataFrame: ",pageID)
			print(dataFrame)
			if len(dataFrame) != 0:
				print(dataFrame[0].shape)
		if args.air:
			if (len(dataFrame) != 0 and dataFrame[0].shape[1] == 6):
				return pageID
		else:
			if (len(dataFrame) != 0 and dataFrame[0].shape[1] > 6):
				return pageID

def ExtractValues(dataFrame,items):
	if debug:
		print(dataFrame)
	addedItems = 0
	for index in range(dataFrame.shape[0]):
		if type(dataFrame.iloc[index][0]) != type(""):
			continue
		# print(dataFrame.iloc[index][0])
		titleList = dataFrame.iloc[index][0].split(" ")
		name = " ".join(titleList[1:])
		# print(titleList)
		if titleList[0].count(".") == 2 and len(titleList[0]) < 8:
		# if type(dataFrame.loc[index]["Valuta"]) ==  type(""):
			ammount = float((dataFrame.iloc[index][-2]).replace(",",".").replace(" ",""))
			# ammount = float((dataFrame.iloc[index][-2]))
			paymentType = "out" if ammount < 0 else "in"
			month = titleList[0].split(".")[1]
			day = titleList[0].split(".")[0]
			items.append({"year":args.Year,"month":month,"day":day,"name":name,"accountName":dataFrame.iloc[index][1],"account":dataFrame.iloc[index+1][0],"vs":dataFrame.iloc[index+1][1],"value":ammount,"identified":False,"paymentType":paymentType})
			addedItems += 1
			if "kartou" in items[-1]["name"]:
				items[-1]["place"] = dataFrame.iloc[index+2][0]
			if debug:
				print(items[-1])
	return addedItems

def ExtractValuesAirBank(dataFrame,items):
	if debug:
		print(dataFrame)
	addedItems = 0
	for index in range(dataFrame.shape[0]):
		if debug:
			print(dataFrame.iloc[index])
		date = dataFrame.iloc[index][0].split("\r")[-1]
		transactionType = dataFrame.iloc[index][1].split("\r")[0]
		transactionID = dataFrame.iloc[index][1].split("\r")[-1]
		# print(dataFrame.iloc[index][2].split("\r"))
		accountName = dataFrame.iloc[index][2].split("\r")[0]
		# print(accountName)
		account = dataFrame.iloc[index][2].split("\r")[-1]
		# print(account)
		if type(dataFrame.iloc[index][3]) == type(0.0):
			vs = -1
			place = ""
		else:
			if len(dataFrame.iloc[index][3]) == 1:
				place = dataFrame.iloc[index][3].split("\r")[0]
				vs = -1
			else:
				place = dataFrame.iloc[index][3].split("\r")[0]
				vs = dataFrame.iloc[index][3].split("\r")[-1]
		ammount = float((dataFrame.iloc[index][-2]).replace(",",".").replace(" ",""))
		paymentType = "out" if ammount < 0 else "in"
		year = date.split(".")[2]
		month = date.split(".")[1]
		day = date.split(".")[0]

		# print(place)
		items.append({"year":year,"month":month,"day":day,"transactionType":transactionType,"transactionID":transactionID,"accountName":accountName,"account":account,"vs":vs,"value":ammount,"identified":False,"paymentType":paymentType,"place":place})
		addedItems += 1
		# 	if debug:
		# 		print(items[-1])
	return addedItems

def FixEightColumns(dataFrame):
	# print(dataFrame)
	# print(dataFrame.iloc[:,0])
	dataFrame[dataFrame.keys()[0]+dataFrame.keys()[1]] = dataFrame.iloc[:,0].fillna("") + " " + dataFrame.iloc[:,1]
	dataFrame.pop("Datum")
	dataFrame.pop("Označení platby")
	column = dataFrame.pop("DatumOznačení platby")
	dataFrame.insert(0, "DatumOznačení platby", column)
	# print(dataFrame)


def ProcessFirstPageCSOB(fileName,items):
	dataFrame = tabula.read_pdf(fileName,pages=1,area=[48.5,0.0,92.,100.],relative_area=True)[0]
	# print(dataFrame)
	if (dataFrame.shape[1] != 7):
		print("Wrong Settings!!!")
		exit(1)
	if debug:
		print(dataFrame.shape)
		print(dataFrame)
	addedItems = ExtractValues(dataFrame,items)
	dataFrame = tabula.read_pdf(fileName,pages=1,area=[38.0,0.0,45,100.],relative_area=True)[0]
	# print(dataFrame)
	official_incomes = float((dataFrame.iloc[0][3]).replace(",",".").replace(" ",""))
	official_expenses = float((dataFrame.iloc[1][3]).replace(",",".").replace(" ",""))
	official_n_items = int((dataFrame.iloc[0][1])) + int((dataFrame.iloc[1][1]))
	return (addedItems,official_incomes,official_expenses,official_n_items)

def ProcessFirstPageAirBank(fileName,items):
	dataFrame = tabula.read_pdf(fileName,pages=1,area=[53.5,8.0,88.0,92.],relative_area=True)[0]
	if (dataFrame.shape[1] != 6):
		print("Wrong Settings!!!")
		exit(1)
	if debug:
		print(dataFrame.shape)
		print(dataFrame)
	addedItems = ExtractValuesAirBank(dataFrame,items)
	dataFrame = tabula.read_pdf(fileName,pages=1,area=[40.0,0.0,52,100.],relative_area=True)[0]
	# print(dataFrame)
	# print(dataFrame.iloc[0][2])
	official_incomes = float((dataFrame.iloc[0][2]).replace(",",".").replace(" ",""))
	official_expenses = float((dataFrame.iloc[1][2]).replace(",",".").replace(" ",""))
	official_n_items = 0
	return (addedItems,official_incomes,official_expenses,official_n_items)

def ProcessFirstPage(fileName,items):

	if args.air:
		return ProcessFirstPageAirBank(fileName,items)
	else:
		return ProcessFirstPageCSOB(fileName,items)

def ProcessMidPageCSOB(fileName,pageID,items):
	if debug:
		print("Page: " + str(pageID))
	dataFrame = tabula.read_pdf(fileName,pages=pageID,area=[17.0,0.0,95.,100.],relative_area=True)[0]
	if(dataFrame.shape[1] == 8):
			FixEightColumns(dataFrame)
	addedItems = ExtractValues(dataFrame,items)
	return addedItems

def ProcessMidPageAirBank(fileName,pageID,items):
	if debug:
		print("Page: " + str(pageID))
	dataFrame = tabula.read_pdf(fileName,pages=pageID,area=[5.0,8.0,95.,92.],relative_area=True)[0]
	# if(dataFrame.shape[1] == 8):
			# FixEightColumns(dataFrame)
	addedItems = ExtractValuesAirBank(dataFrame,items)
	return addedItems


def ProcessMidPage(fileName,pageID,items):
	if args.air:
		return ProcessMidPageAirBank(fileName,pageID,items)
	else:
		return ProcessMidPageCSOB(fileName,pageID,items)

def ProcessLastPageCSOB(fileName,pageID,items):
	if debug:
		print("LastPage")
	for bottomLimit in range(95,15,-1):
		dataFrame = tabula.read_pdf(fileName,pages=pageID,area=[17.0,0.0,bottomLimit,100.],relative_area=True)[0]
		# print(bottomLimit)
		# print(dataFrame)
		# print(dataFrame[0].shape[1] == 8)
		if(dataFrame.shape[1] == 8):
			FixEightColumns(dataFrame)
		# print(dataFrame)
		# print(dataFrame.shape[1])
		if(dataFrame.shape[1] == 7):
			addedItems = ExtractValues(dataFrame,items)
			# print(addedItems)
			return addedItems

def ProcessLastPageAirBank(fileName,pageID,items):
	if debug:
		print("LastPage")
	for bottomLimit in range(95,15,-1):
		dataFrame = tabula.read_pdf(fileName,pages=pageID,area=[5.0,8.0,bottomLimit,92.],relative_area=True)[0]
		# print(bottomLimit)
		# print(dataFrame)
		if(dataFrame.shape[1] == 6):
			addedItems = ExtractValuesAirBank(dataFrame,items)
			# print(addedItems)
			return addedItems

def ProcessLastPage(fileName,pageID,items):
	if args.air:
		return ProcessLastPageAirBank(fileName,pageID,items)
	else:
		return ProcessLastPageCSOB(fileName,pageID,items)

def CalculateSum(items,nItems):
	expenses = 0
	incomes = 0

	for index in range(nItems,len(items)):
		if items[index]["value"] < 0:
			expenses -= items[index]["value"]
		else:
			incomes += items[index]["value"]

	# print("Expenses: ",expenses)
	# print("Incomes: ", incomes)
	return (incomes,expenses)

def PrintItems(items):
	for item in items:
		print(str(item["year"])+"-"+item["month"]+"-"+item["day"],item["name"],item["accountName"],item["account"],item["vs"],item["value"],item.get("place",""))

def ProcessFile(fileName,items,nItems):
	print("Processing file:",fileName)
	try:
		pdfread = PdfFileReader(fileName)
	except:
		print("No file: " + fileName + " found!")
		return 0
	numPages = pdfread.getNumPages()
	lastPage = GetTheLastPage(numPages,fileName);
	if debug:
		print("Debug - NumPages: ",numPages," lastPage: ",lastPage)
	official_incomes = 0
	official_expenses = 0
	official_n_items = 0
	extracted_n_items = 0
	extracted_n_items,official_incomes,official_expenses,official_n_items = ProcessFirstPage(fileName,items)
	# print(items)
	for pageID in range(2,lastPage):
		extracted_n_items += ProcessMidPage(fileName,pageID,items)
		# print(items)
	extracted_n_items += ProcessLastPage(fileName,lastPage,items)
	# print(items)
	# print("Extracted items: " + str(extracted_n_items))
	extracted_incomes,extracted_expenses = CalculateSum(items,nItems)
	print("\tOfficial expenses: " + str(official_expenses) + " vs. Extracted expenses: " + str(extracted_expenses))
	print("\tOfficial incomes: " + str(official_incomes) + " vs. Extracted incomes: " + str(extracted_incomes))
	print("\tOfficial No. items: " + str(official_n_items) + " vs. Extracted No. items: " + str(extracted_n_items))
	if abs(extracted_incomes - official_incomes) > 1 or abs(official_expenses - extracted_expenses) > 1:
		print("File was not processed properly:")
		exit(1)
	return extracted_n_items

def ProcessFiles():
	if args.air:
		if args.Month != -1:
			items = []
			nItems = 0
			nItems = ProcessFile("data/vypisy/" + str(args.Year) + "/" + str(args.Month) + "a.pdf",items,nItems)
			SaveItems(items,str(args.Month))
		else:
			for monthID in range(1,13):
				items = []
				nItems = 0
				nItems = ProcessFile("data/vypisy/" + str(args.Year) + "/" + str(monthID) + "a.pdf",items,nItems)
				SaveItems(items,str(monthID))
	else:
		if args.Month != -1:
			items = []
			nItems = 0
			nItems = ProcessFile("data/vypisy/" + str(args.Year) + "/" + str(args.Month) + ".pdf",items,nItems)
			nItems = ProcessFile("data/vypisy/" + str(args.Year) + "/" + str(args.Month) + "m.pdf",items,nItems)
			SaveItems(items,str(args.Month))
		else:
			for monthID in range(1,13):
				items = []
				nItems = 0
				nItems = ProcessFile("data/vypisy/" + str(args.Year) + "/" + str(monthID) + ".pdf",items,nItems)
				nItems = ProcessFile("data/vypisy/" + str(args.Year) + "/" + str(monthID) + "m.pdf",items,nItems)
				SaveItems(items,str(monthID))

def SaveItems(items,monthID):
	if args.air:
		with open('data/extractedPayments/items_' + str(args.Year) + "_" + monthID + "_AirBank.json", 'w') as filehandle:
		    json.dump(items, filehandle)
	else:
		with open('data/extractedPayments/items_' + str(args.Year) + "_" + monthID + ".json", 'w') as filehandle:
		    json.dump(items, filehandle)

# Create the parser
my_parser = argparse.ArgumentParser(description='Reads PDF account statements and transforms them to the python format')

# Add the arguments
my_parser.add_argument('Year',
                       metavar='year',
                       type=int,
                       help='year of the statement')

# Add the arguments
my_parser.add_argument('Month',
                       metavar='month',
                       type=int,
                       help='month of the statement')

my_parser.add_argument('-a',
                       '--air',
                       action='store_true',
                       help='read AirBank statement format')

# Execute the parse_args() method
args = my_parser.parse_args()

if __name__ == "__main__":
	ProcessFiles()
