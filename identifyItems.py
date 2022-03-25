import json
import argparse
import hashlib

def PrintItems(items):
    for item in items:
        PrintItem(item)

def PrintItem(item):
    print(str(item["year"])+"-"+item["month"]+"-"+item["day"],item["transactionType"],item["accountName"],item["account"],item["vs"],item["value"],item.get("place",""),sep="|")

def PrintRule(rule):
    print(rule["ruleType"],rule["ruleValue"],rule["who"],rule["type"],rule["subType"])

def PrintIdentifiedItems(items):
    print("Identified items: ")
    for item in items:
        if item["identified"]:
            PrintItem(item)

def PrintUnidentifiedItems(items):
    print("Unidentified items: ")
    for item in items:
        if not item["identified"]:
            PrintItem(item)

def PrintRules(rules):
    for rule in rules:
        print(rule["ruleType"],rule["ruleValue"],rule["who"],rule["type"],rule["subType"])

def ReadItems(items):
    try:
        fileName = ""
        if args.air:
            fileName = 'data/extractedPayments/items_' + str(args.Year) + "_" + str(args.Month) + "_AirBank.json"
        else:
            fileName = 'data/extractedPayments/items_' + str(args.Year) + "_" + str(args.Month) + ".json"

        with open(fileName, 'r') as filehandle:
            items[:] = json.load(filehandle)
        items.sort(key = lambda i: i['value'])
    except:
        print("No file: " + fileName + " found!")
        exit(1)
    # PrintItems(items)

def ReadRules(rules):
    try:
        with open('configs/rules.json', 'r') as filehandle:
            rules[:] = json.load(filehandle)
    except:
        with open('configs/rules.json', 'w') as filehandle:
            rules[:] = []

def ReadFinancialBook():
    fileName = ""
    if args.air:
        fileName = 'data/financialBook/finBook_AirBank.json'
    else:
        fileName = 'data/financialBook/finBook.json'
    try:
        with open(fileName, 'r') as filehandle:
            # book{:} = json.load(filehandle)
            data = json.load(filehandle)
    except:
        data = {}
        with open(fileName, 'w') as filehandle:
            json.dump(book, filehandle)
    return data

def SaveFinancialBook(book):
    fileName = ""
    if args.air:
        fileName = 'data/financialBook/finBook_AirBank.json'
    else:
        fileName = 'data/financialBook/finBook.json'
    with open(fileName, 'w') as filehandle:
        json.dump(book, filehandle)

def CheckItem(item,rule):
    if item.get(rule["ruleType"]) == None or type(item.get(rule["ruleType"])) != type(""):
        return False
    # PrintItem(item)
    # PrintRule(rule)
    if rule["ruleValue"].lower() in item.get(rule["ruleType"]).lower():
        # print("Item identified")
        # print(item)
        item["identified"] = True
        item["who"] = rule["who"]
        item["type"] = rule["type"]
        item["subType"] = rule["subType"]
        return True

def IdentifyItems(items,rules):
    for item in items:
        item["type"] = "unidentified"
        for rule in rules:
            if CheckItem(item,rule):
                break

def GenerateHash(item):
    # PrintItem(item)
    print(str(item["year"]),str(item["month"]),str(item["day"]),str(item["transactionType"]),str(item["transactionID"]),str(item["accountName"]),str(item["account"]),str(item["vs"]),str(item["value"]),item.get("place",""))
    hashInput = str(item["year"]) + str(item["month"]) + str(item["day"]) + str(item["transactionType"]) + str(item["transactionID"]) + str(item["accountName"]) + str(item["account"]) + str(item["vs"]) + str(item["value"]) + item.get("place","")
    m = hashlib.md5()
    m.update(hashInput.encode('utf-8'))
    return str(int(m.hexdigest(), 16))[0:12]

def AddToBook(items,book):
    for item in items:
        hash = GenerateHash(item)
        if hash in book:
            if book[hash]["identified"] == False and item["identified"] == True:
                book[hash]["type"] = item["type"]
                book[hash]["who"] = item["who"]
                book[hash]["subType"] = item["subType"]
                book[hash]["identified"] = True
            continue
        else:
            book[hash] = item

# Create the parser
my_parser = argparse.ArgumentParser(description='Tries to identify extracted payments based on the identification rules')

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
    items = []
    rules = []
    book = {}
    ReadItems(items)
    # PrintItems(items)
    ReadRules(rules)
    # PrintRules(rules)
    book = ReadFinancialBook()
    IdentifyItems(items,rules)
    AddToBook(items,book)
    SaveFinancialBook(book)
    PrintIdentifiedItems(items)
    PrintUnidentifiedItems(items)
