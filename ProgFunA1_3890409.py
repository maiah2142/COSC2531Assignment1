import sys

debug = True

#template for displaying error messages
#ideally the user never sees this
#used to debug and make sure the program doesn't always hard crash
def printError(desc:str, e:str)->str:
    sys.stdout.write("An error has occured with " + str(desc) + ", " + str(e) + ".\n")

#formats price to be 2 decimal places and rounds pricing
def formatPrice(price:float)->float:
    return "{:.2f}".format(round(price, 2))

#formats a neat print for lists
def neatPrintList(neatList:list):
    if neatList:
        #range is used instead of "in list" to utilise index
        for i in range(len(neatList)):
            sys.stdout.write(neatList[i])
            #separates items in list with commas
            if not i == len(neatList) - 1:
                sys.stdout.write(", ")
            #if last item use full stop instead
            else:
                sys.stdout.write(".")

#for loop that takes in a variable number of booleans
#and checks if they are all True
#it's basically an And gate
def bulkValidation(*validBools:bool)->bool:
    for check in validBools:
        if not check:
            return False    #return False if a single False is detected
    return True             #return True if all True

#Checks if name is all alpha characters
def nameValid(name:str, errMsg:str = None)->bool:
    #checks every character individually in the input string
    for ch in name:
        if not (ch.isalpha() or ch.isspace()):
            if errMsg: sys.stdout.write(errMsg)
            return False    #return False if invalid
    return True             #return True if valid

#Checks if product's name contains any spaces
def prodNameValid(prod:str, errMsg:str = None)->bool:
    #checks every character individually in the input string
    for ch in prod:
        if ch.isspace():
            if errMsg: sys.stdout.write(errMsg)
            return False    #return False if invalid
    return True             #return True if valid

#Checks if item exists in the list
def existValid(item, checkList:list, errMsg:str = None)->bool:
    if not item in checkList:
        if errMsg: sys.stdout.write(errMsg)
        return False
    return True

#Checks if the number is within the mathematical set N (natural integers)
def naturalNumValid(num:int, errMsg:str = None)->bool:
    if not num.isdecimal() or num == 0:
        if errMsg: sys.stdout.write(errMsg)
        return False
    return True

#Checks if an integer, index, is within the bounds of a list's size
def indexValid(index:int, checkList:list, errMsg:str = None)->bool:
    if index < 0 or index > len(checkList) - 1:
        if errMsg: sys.stdout.write(errMsg)
        return False
    return True

#Checks for if the item is null (None)
def nullValid(item, errMsg:str = None)->bool:
    if item == None:
        if errMsg: sys.stdout.write(errMsg)
        return False
    return True

#TODO redo without dictionary
def stockUpdateValidation(product:str, quantity:int, stocks:dict, errMsg:str = None)->bool:
    if quantity > stocks[product]:
        if errMsg: sys.stdout.write(errMsg)
        return False
    return True

"""
Originally I used while(True) to keep a loop going on constantly asking for input until
broken out of the loop.
Currently a boolean declared "loop" initiated as "True" is used which I can later
change inside the while loop to the value of "False".
"""
#get name input from user
def getName()->str:
    loop = True
    while loop:
        #get input
        sys.stdout.write("Please enter the name of the customer: ")
        custName = input()
        if bulkValidation(\
                nameValid(custName,\
                    "The name must only contain alphabet characters or spaces.\n")
        ):
            loop = False
    #finally return name
    return custName

#get product input from user
def getProduct(listProducts:list)->str:
    loop = True
    while loop:
        #get input
        sys.stdout.write("Please enter the name of a product: ")
        productName = input()
        if bulkValidation(\
                prodNameValid(productName,\
                    "The product's name must not contain any spaces."),\
                existValid(productName, listProducts,\
                    "That product does not exist.\n")\
        ):
            loop = False
    #finally return product
    return productName

#get product quantity input from user
def getQuantity()->int:
    loop = True
    while loop:
        #get input
        sys.stdout.write("Please enter quantity you wish to order: ")
        quantity = input()
        if bulkValidation(\
                naturalNumValid(quantity,\
                    "Please enter a positive whole number.\n")
        ):
            loop = False
    #finally return quantity
    return int(quantity)

#calculate the price of single product with discount
def calcUnitPrice(existingCustomer, productName, listProducts, listPrices):
    #get product index
    index = listProducts.index(productName)

    if not indexValid(index, listPrices):
        return
    else:
        price = listPrices[index]

    #if existing customer apply 10% discount
    if existingCustomer:
        price *= 0.9
    return price

#mulitplies price by quantity
def calcTotalPrice(price:float, quantity:int)->float:
    try:
        return price * quantity
    except Exception as e:
        printError("calculating total pricing", str(e))
        return

#prints output as directed in part 1 of assignment
def printReceipt(custName, productName, price, quantity):
    sys.stdout.write(\
            custName + " purchased " + str(quantity) + " x " + productName + "\n" +\
            "Unit price:  $" + str(formatPrice(price)) + "\n" +\
            "Total price: $" + str(formatPrice(calcTotalPrice(price, quantity)))\
            + "\n"\
    )

def updateProdStock(product:str, quantity:int, dictStock:dict):
    dictStock[product] = dictStock[product] - quantity

def updateTotalSpend(dictTotalSpend:dict, name:str, price:float):
    if not dictTotalSpend.get(name):
        dictTotalSpend[name] = price
    else:
        dictTotalSpend[name] = dictTotalSpend.get(name) + price

def getMostValued(dictTotalSpend:dict, listCustomers:list)->list:
    listNames = []
    highest = 0
    for names in listCustomers:
        amount = dictTotalSpend.get(names)
        if amount:
            if amount == highest:
                listNames.append(names)
            elif amount > highest:
                listNames.clear()
                listNames.append(names)
                highest = amount
    return listNames

def printMostValued(dictTotalSpend:dict, listCustomers:list):
    cust = getMostValued(dictTotalSpend, listCustomers)
    if not cust:
        sys.stdout.write("No customer has made a purchase.")
    else:
        sys.stdout.write("The most valuable customer")
        if len(cust) == 1:
            sys.stdout.write(" is: ")
        else:
            sys.stdout.write("s are: ")
        neatPrintList(cust)
    sys.stdout.write("\n\n")

def updateOrderHistory(dictOrderHistory:dict, name:str, prod:str, quantity:int):
    if not dictOrderHistory.get(name):
        dictTempVal = {prod: quantity}
        dictOrderHistory[name] = dictTempVal 
    elif not dictOrderHistory.get(name).get(prod):
        dictOrderHistory[name][prod] = quantity
    else:
        oldVal = dictOrderHistory.get(name).get(prod)
        dictOrderHistory[name][prod] = oldVal + quantity

def getOrderHistory(dictOrderHistory:dict, prod:str, name:str)->int:
    if not dictOrderHistory.get(name):
        return 0
    elif not dictOrderHistory.get(name).get(prod):
        return 0
    else:
        return dictOrderHistory.get(name).get(prod)
    return

#TODO data validation
def printOrderHistory(listCustomers:list, listProducts:list, dictOrderHistory:dict):
    padName = 15
    padProd = 8
    formName = "{:<" + str(padName) + "}"
    formProd = "{:>" + str(padProd) + "}"

    #print product header
    sys.stdout.write(formName.format("") + " ")
    for prod in listProducts:
        sys.stdout.write(" " + formProd.format(prod)[:padProd])
    sys.stdout.write("\n")

    #print name header and purchase quantities
    for name in listCustomers:
        sys.stdout.write(formName.format(name) + " ")
        for prod in listProducts:
            sys.stdout.write(" " + formProd.format(getOrderHistory(dictOrderHistory, prod, name)))
        sys.stdout.write("\n")
    sys.stdout.write("\n")


#ask for input to make order
def makeOrder(listCustomers:list, listProducts:list, listPrices:list,\
        dictStock:dict, dictTotalSpend:dict, dictOrderHistory:dict):
    loop = True
    sys.stdout.write("\n")

    #get input from customer
    custName = getName()
    existCust = custName in listCustomers
    while loop:
        productName = getProduct(listProducts)
        unitPrice = calcUnitPrice(existCust, productName, listProducts, listPrices)
        try:
            if unitPrice == None:
                sys.stdout.write("That product does not have a price.\n")
            elif unitPrice < 0:
                sys.stdout.write("The product's price is invalid.\n")
            elif unitPrice == 0 and not existCust:
                sys.stdout.write("Free products are not available to new customers.\n")
            else:
                loop = False
        except Exception as e:
            printError("making an order", str(e))

    loop = True
    while loop:
        quantity = getQuantity()
        if stockUpdateValidation(productName, quantity, dictStock,\
                "Unfortunately we only have " + str(dictStock.get(productName)) +\
                " in stock.\nWould you like to cancel the current order?\n"):
            updateProdStock(productName, quantity, dictStock)
            loop = False

    sys.stdout.write("\n")
    #print receipt output
    printReceipt(custName, productName, unitPrice, quantity)
    #add customer to customer list if they are new
    if not existCust:
        listCustomers.append(custName)
    updateTotalSpend(dictTotalSpend, custName, calcTotalPrice(unitPrice, quantity))
    updateOrderHistory(dictOrderHistory, custName, productName, quantity)
    sys.stdout.write("\n")

#figure out later how to do this without classes
#or maybe ask if classes are allowed to be used?
"""
Originally I used globals to call the lists outside of the main function's scope.
I later found calling the list with .clear and .append worked too which is the current
implementation.
Perhaps using a set/dictionary could be good as well since that'll force uniqueness
but that'll also be weird with ordering.
"""
#TODO Empty input validation
def newProductList():
    loop = True

    while loop:
        #flags to check for errors
        #flags reset every loop
        flagUnique = False
        flagAlpNum = False
        flagNull = False

        #get input
        sys.stdout.write("Please enter a new list of products separated by spaces:\n")
        try:
            productInput = input().split()
            #checks if user input is unique
            #converts list into set, sets being unique
            #if the length of the set is the same as the list
            #then the list only has unique elements
            if not len(set(productInput)) == len(productInput): 
                flagUnique = True
            #checks each item in the list to see if they are alphanumeric
            for item in productInput:
                if not item.isalnum():
                    flagAlpNum = False
                    break
        except Exception as e:
            printError("entering a new product list", str(e))

        #print relevant error messages to user
        if flagUnique:
            sys.stdout.write("Please have every product be unqiue.\n")
        if flagAlpNum:
            sys.stdout.write("Please have every product be one word and " +\
                    "contain only alphabet or numeric characters.\n")
        sys.stdout.write("\n")
        #break out of loop if no errors were detected or flags raised
        #this makes it so user cannot reenter input once valid input is entered
        if not flagUnique and not flagAlpNum:
            loop = False

    #set new list
    try:
        listProducts.clear()
        #if a new product list is made it makes sense to force a price list as well
        for item in productInput:
            listProducts.append(str(item))
        sys.stdout.write("New product list successfully set.\n\n")
    except Exception as e:
        printError("creating a new product list", str(e))

#Done? Maybe.
def newPriceList():
    loop = True
    while loop:
        flagDecimal = False
        flagNull = False

        #get input
        sys.stdout.write("Please enter a new list of prices separated by a space and " +\
                "without the $ symbol: ")

        try:
            priceInput = input().split()
            #loops through every item in user's input
            for item in priceInput:
                #checks if item is a decimal number
                #removes a single decimal point and checks if
                #string is all integers, if all integers it means
                #only 1 or 0 decimals were inputted,
                #negative sign was added to validation as part 3.1 implies negative
                #values are valid input, but processed invalidly in different areas
                if not item.replace(".", "", 1).replace("-", "", 1).isdecimal():
                    flagDecimal = True
                if item == "":
                    flagNull = True
        except Exception as e:
            printError("entering a new price list", str(e))

        #print relevant error messages to user
        if flagDecimal:
            sys.stdout.write("Please use numbers or decimal numbers without a $ symbol.\n")
        if flagNull:
            sys.stdout.write("Please do not have any null inputs.\n")

        #get out of loop if no error detected
        if not flagDecimal and not flagNull:
            loop = False

    #set new list
    try:
        listPrices.clear()
        for item in priceInput:
            listPrices.append(float(item))
        sys.stdout.write("New price list successfully set.\n\n")
    except Exception as e:
        printError("creating a new price list", str(e))

#prints product list
def printProducts(listProducts:list, listPrices:list, dictStock:dict):
    #neatPrintList(listProducts, "products")
    padProd = "{:<15}"
    padPrice = "{:>9}"
    padStock = "{:>6}"
    formatting = padProd + padPrice + padStock + "\n"

    if not listProducts:
        sys.stdout.write("There are currently no products.") 
    else:
        try:
            sys.stdout.write(formatting.format("Products", "Price", "Stock"))
            for i in range(len(listProducts)):
                if i > len(listPrices) - 1 or listPrices[i] < 0:
                    price = "No Price"
                else:
                    price = formatPrice(listPrices[i])
                prod = listProducts[i]
                stock = dictStock[prod]
                sys.stdout.write(formatting.format(prod, price, stock))
        except Exception as e:
            printError("printing product list", str(e))
    sys.stdout.write("\n")


#prints all existing customers
def printCustomers(listCustomers:list):
    if not listCustomers:
        sys.stdout.write("There are currently no existing customers.")
    else:
        sys.stdout.write("Existing customers:")
        neatPrintList(listCustomers)
    sys.stdout.write("\n\n")

def getReplenish()->int:
    loop = True
    while loop:
        sys.stdout.write("Please enter the  quantity you wish each product be stocked to: ")
        quantity = input()
        if not quantity.isdecimal():
            sys.stdout.write("Please enter a whole number greater than or equal to 0.\n")
        else:
            loop = False
    try:
        return int(quantity)
    except Exception as e:
        printError("getting input for replenishing", str(e))
    return

def replenish(dictStock:dict, listProducts:list):
    quantity = getReplenish()
    if quantity == None:
        printError("replenishing stock", "")
    else:
        dictStock.clear()
        for prod in listProducts:
            dictStock[prod] = quantity
        sys.stdout.write("All products successfully replenished.\n\n")

#print the menu options
def printMenu():
    sys.stdout.write(\
            "Please enter an option:\n" +\
            "1. Make a new purchase\n" +\
            "2. Replace product list\n" +\
            "3. Replace product prices\n" +\
            "4. Display all existing customers\n" +\
            "5. Display all products and prices\n" +\
            "6. Replenish stock\n" +\
            "7. Display most valuable customer(s)\n" +\
            "8. Display previous order information\n" +\
            "\n" +\
            "0. Exit\n\n" +\
            "> "\
    )

#main init
if __name__ == '__main__':
    #temporary customer list
    listCustomers =[]
    #temporary product list
    listProducts = []
    #temporary product list
    listPrices = []
    #temporary stock dictionary
    dictStock = {}
    
    dictOrderHistory = {}
    #dictionary to keep track of amount spent by each customer
    dictTotalSpend = {}

    if debug:
        listCustomers = ["John Smith", "Jane Doe"]
        listProducts = ["shortblack", "cappuccino", "latte"]
        listPrices = [1, 12.5555, 2.01]
        print(listProducts)
        for prod in listProducts:
            dictStock[prod] = 10

    while True:
        printMenu()
        option = input()
        if   option == "1":
            makeOrder(listCustomers, listProducts, listPrices, dictStock, dictTotalSpend, dictOrderHistory)
        elif option == "2":
            newProductList()
        elif option == "3":
            newPriceList()
        elif option == "4":
            printCustomers(listCustomers)
        elif option == "5":
            printProducts(listProducts, listPrices, dictStock)
        elif option == "6":
            replenish(dictStock, listProducts)
        elif option == "7":
            printMostValued(dictTotalSpend, listCustomers)
        elif option == "8":
            printOrderHistory(listCustomers, listProducts, dictOrderHistory)
        elif option == "0":
            sys.stdout.write("Goodbye.\n")
            quit()
