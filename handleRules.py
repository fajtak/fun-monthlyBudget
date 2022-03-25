import json

rules = []
who = []
types = {}

def PrintRules():
    for rule in rules:
        print(rule["ruleType"],rule["ruleValue"],rule["who"],rule["type"],rule["subType"])

def ReadRules():
	try:
		with open('configs/rules.json', 'r') as filehandle:
		    rules[:] = json.load(filehandle)
	except:
		pass

def ReadWhoTags():
	try:
		with open('configs/whoTags.json', 'r') as filehandle:
		    who[:] = json.load(filehandle)
	except:
		pass

def ReadTypeTags():
	try:
		with open('configs/typeTags.json', 'r') as filehandle:
		    # types{} = json.load(filehandle)
		     types = json.load(filehandle)
	except:
		pass
	return types

def SaveRules():
	with open('configs/rules.json', 'w') as filehandle:
	    json.dump(rules, filehandle)

def SaveWhoTags():
	with open('configs/whoTags.json', 'w') as filehandle:
	    json.dump(who,filehandle)

def SaveTypeTags():
	with open('configs/typeTags.json', 'w') as filehandle:
	    json.dump(types,filehandle)

def GetRuleType():
	print("Pick rule type:\n\t1 - transactionType\n\t2 - accountName\n\t3 - account\n\t4 - vs\n\t5 - place\n")
	ruleTypeInput = int(input())
	ruleType = ""
	if ruleTypeInput == 1:
		ruleType = "transactionType"
	elif ruleTypeInput == 2:
		ruleType = "accountName"
	elif ruleTypeInput == 3:
		ruleType = "account"
	elif ruleTypeInput == 4:
		ruleType = "vs"
	elif ruleTypeInput == 5:
		ruleType = "place"
	else:
		return "exit"
	return ruleType

def AddRule():
	ruleType = GetRuleType()
	if ruleType == "exit":
		exit(1)
	ruleValue = input("Enter rule value: ")
	while True:
		print(who)
		whoTag = input("Enter who tag: ")
		if whoTag in who:
		    break
	while True:
		print(types.keys())
		typeTag = input("Enter type tag: ")
		if typeTag in types:
		    break
	while True:
		print(types[typeTag])
		subTypeTag = input("Enter subType tag: ")
		if subTypeTag in types[typeTag]:
		    break
	rules.append({"ruleType":ruleType,"ruleValue":ruleValue,"who":whoTag,"type":typeTag,"subType":subTypeTag})
	return 0

def AddWhoTag():
	newWhoTag = input("Enter new WhoTag: ")
	if (newWhoTag.isnumeric()):
		return -1
	who.append(newWhoTag)
	return 0

def AddTypeTag():
	print(types)
	newTypeTag = input("Enter new TypeTag: ")
	if (newTypeTag.isnumeric()):
		return -1
	newSubtypeTags = []
	while True:
		newSubtypeTag = input("Enter new SubTypeTag: ")
		if (newSubtypeTag.isnumeric()):
			if len(newSubtypeTags) != 0:
				if newTypeTag in types:
					types[newTypeTag].append(newSubtypeTags)
				else:
					types[newTypeTag] = newSubtypeTags
			break
		newSubtypeTags.append(newSubtypeTag)
	return 0

if __name__ == "__main__":
	ReadRules()
	# print(rules)
	ReadWhoTags()
	# print(who)
	types = ReadTypeTags()
	# print(types)
	# PrintRules()
	# print(who)
	while (True):
		if 	AddRule() != 0:
		# if 	AddWhoTag() != 0:
		# if 	AddTypeTag() != 0:
			break
		SaveRules()
	PrintRules()
	SaveWhoTags()
	SaveTypeTags()