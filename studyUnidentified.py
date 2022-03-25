import json

def ReadFinancialBook():
    with open('data/financialBook/finBook.json', 'r') as filehandle:
        # book{:} = json.load(filehandle)
        data = json.load(filehandle)
    return data

def SaveFinancialBook(book):
    with open('data/financialBook/finBook.json', 'w') as filehandle:
        json.dump(book, filehandle)

def StudyUnindentified(book):

	nIdentified = 0
	for item in book.values():
		if item["identified"] == False:
			nIdentified += 1
			print(item)
	return nIdentified

if __name__ == "__main__":
	book = ReadFinancialBook()
	nUnindentified = StudyUnindentified(book)
	print(nUnindentified)