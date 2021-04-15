import sys

debug = True

#template for displaying error messages
#ideally the user never sees this
#used to debug and make sure the program doesn't always hard crash
def printError(desc:str, e:str = None)->str:
    sys.stdout.write("An error has occured with " + str(desc))
    if e:
        sys.stdout.write(", " + str(e))
    sys.stdout.write(".\n")

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

"""
The validation functions below
return true is valid, false if invalid
"""
#Loop that takes in a variable number of booleans
#and checks if they are all True
#it's basically an And gate
def bulkValidation(*validBools:bool)->bool:
    for check in validBools:
        if not check:
            return False
    return True

#Checks if name is all alpha characters
def nameValid(name:str, errMsg:str = None)->bool:
    #checks every character individually in the input string
    for ch in name:
        if not (ch.isalpha() or ch.isspace()):
            if errMsg: sys.stdout.write(errMsg)
            return False
    return True

#Checks if product's name contains any spaces
def prodNameValid(prod:str, errMsg:str = None)->bool:
    #checks every character individually in the input string
    for ch in prod:
        if ch.isspace():
            if errMsg: sys.stdout.write(errMsg)
            return False
    return True

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

#Checks if the number is within the mathematical set R (real number)
def realNumValid(num:float, errMsg:str = None)->bool:
    if not str(num).replace(".", "", 1).replace("-", "", 1).isdecimal():
        if errMsg: sys.stdout.write(errMsg)
        return False
    return True

#Checks if an integer, index, is within the bounds of a list's size
def indexValid(index:int, checkList:list, errMsg:str = None)->bool:
    if index < 0 or index > len(checkList) - 1:
        if errMsg: sys.stdout.write(errMsg)
        return False
    return True


#Helper function to convert single validations to apply to every element
#in a data structure
def dataStructValid(dataStruct, valid, errMsg:str = None)->bool:
    for item in dataStruct:
        if not valid(item):
            if errMsg: sys.stdout.write(errMsg)
            return False
    return True

#Checks for if the item is null, such as None or empty string
def noNullValid(item, errMsg:str = None)->bool:
    if not item:
        if errMsg: sys.stdout.write(errMsg)
        return False
    return True

#Checks if item is alphanumeric
def alphanumValid(item, errMsg:str = None)->bool:
    if not item.isalnum:
        if errMsg: sys.stdout.write(errMsg)
        return False
    return True

#Checks for duplicates in a data structure by turning the data
#structure into a set and comparings the set's length to its actual
#length, this works as sets remove duplicate elements
def noDupeValid(dataStruct, errMsg:str = None)->bool:
    if not len(set(dataStruct)) == len(dataStruct):
        if errMsg: sys.stdout.write(errMsg)
        return False
    return True

#checks if the two values are first valid,
#then checks if the first is simply greater than the second
def valueCompareValid(num1:int, num2:int, errMsg:str = None)->bool:
    if num1 == None or num2 == None:
        if errMsg: sys.stdout.write(errMsg)
        return False
    elif num1 > num2:
        if errMsg: sys.stdout.write(errMsg)
        return False
    return True

#Checks if at least one element in listPrice is valid
def onePriceValid(listPrice:list, errMsg:str = None)->bool:
    for price in listPrice:
        if str(price).replace(".", "", 1).isdecimal():
            return True
    if errMsg: sys.stdout.write(errMsg)
    return False

#Checks for the conditions that the price is free and the customer is new
#if so then it is an invalid purchase
def freeProductValid(price:float, existCust:bool, errMsg:str = None)->bool:
    if price == 0 and not existCust:
        if errMsg: sys.stdout.write(errMsg)
        return False
    return True


"""
Originally I used while(True) to keep a loop going on constantly asking for input until
broken out of the loop.
Currently a boolean declared "loop" initiated as "True" is used which I can later
change inside the while loop to the value of "False".
"""
#Requirement 1.1
#get name input from user
def getName()->str:
    #loop to ask for input if input was invalid
    loop = True
    while loop:
        #get input
        sys.stdout.write("Please enter the name of the customer: ")
        custName = input()
        if nameValid(custName,\
                "The name must only contain alphabet characters or spaces.\n"):
            loop = False
    #finally return name
    return custName

#Requirement 1.2 and 2.1
#get product input from user
def getProduct(listProducts:list)->str:
    #loop to ask for input if input was invalid
    loop = True
    while loop:
        #get input
        sys.stdout.write("Please enter the name of a product: ")
        productName = input()
        if bulkValidation(\
                prodNameValid(productName,\
                    "The product's name must not contain any spaces.\n"),\
                #Requirement 2.1
                existValid(productName, listProducts,\
                    "That product does not exist.\n")\
        ):
            loop = False
    #finally return product
    return productName

#Requirement 1.3
#get product quantity input from user
def getQuantity()->int:
    #loop to ask for input if input was invalid
    loop = True
    while loop:
        #get input
        sys.stdout.write("Please enter quantity you wish to order: ")
        quantity = input()
        if naturalNumValid(quantity,\
                "Please enter a positive whole number.\n"):
            loop = False
    #finally return quantity
    return int(quantity)

#Requirement 1.4 and 1.7
#calculate the price of single product with discount
def calcUnitPrice(existingCustomer, productName, listProducts, listPrices):
    #get product index
    index = listProducts.index(productName)

    if not indexValid(index, listPrices):
        return
    else:
        price = listPrices[index]

    #Requirement 1.7
    #if existing customer apply 10% discount
    if existingCustomer:
        price *= 0.9
    return price

#Requirement 1.8 helper function
#mulitplies price by quantity
def calcTotalPrice(price:float, quantity:int)->float:
    try:
        return price * quantity
    except Exception as e:
        printError("calculating total pricing", str(e))
        return

#Requirement 1.8
#prints output as directed in part 1 of assignment
def printReceipt(custName, productName, price, quantity):
    sys.stdout.write(\
            custName + " purchased " + str(quantity) + " x " + productName + "\n" +\
            "Unit price:  $" + str(formatPrice(price)) + "\n" +\
            "Total price: $" + str(formatPrice(calcTotalPrice(price, quantity)))\
            + "\n"\
    )

#Combines the order functionality of part 1 into a single function
#Requirment 2.5, 3.1, 3.2 and 3.4
#ask for input to make order
def makeOrder(listCustomers:list, listProducts:list, listPrices:list,\
        dictStock:dict, dictTotalSpend:dict, dictOrderHistory:dict):
    sys.stdout.write("\n")

    #if there is no way to make a purchase
    if not bulkValidation(\
            noNullValid(listProducts,\
                    "There are currently no products to purchase.\n"),\
            onePriceValid(listPrices,\
                    "There are currently no valid prices set.\n")):
        sys.stdout.write("The order has been cancelled.\n\n")
        #return back to main menu
        return

    #get input from customer
    custName = getName()
    existCust = custName in listCustomers

    #loop to ask for input if input was invalid
    loop = True
    while loop:
        #get input
        productName = getProduct(listProducts)
        unitPrice = calcUnitPrice(existCust, productName, listProducts, listPrices)

        #temporary validation code before swapping to the bulkValidation method

        """
        if unitPrice == None:
            sys.stdout.write("That product does not have a price.\n")
        elif unitPrice < 0: #Requirement 3.1
            sys.stdout.write("The product's price is invalid.\n")
        elif unitPrice == 0 and not existCust: #Requirement 3.2
            sys.stdout.write("Free products are not available to new customers.\n")
        elif getProdStock(productName, dictStock) == 0: #Requirement 3.4
            sys.stdout.write("That product is currently out of stock.\n")
        else:
            loop = False
        """
        if bulkValidation(\
                noNullValid(unitPrice,\
                        "That product does not have a price.\n"),\
                valueCompareValid(0, unitPrice,\
                        "The product's price is invalid.\n"),\
                valueCompareValid(1, getProdStock(productName, dictStock),\
                        "That product is currently out of stock.\n"),\
                freeProductValid(unitPrice, existCust,\
                        "Free products are not available to new customers.\n")):
            loop = False

    #TODO
    #loop to ask for input if input was invalid
    loop = True
    while loop:
        quantity = getQuantity()
        stockRemaining = str(getProdStock(productName, dictStock))
        if valueCompareValid(quantity, getProdStock(productName, dictStock),\
                "Unfortunately we only have " + stockRemaining +\
                " in stock.\nYou may only order up to " + stockRemaining +\
                " of that product.\n"):
            dictStock[productName] = dictStock[productName] - quantity
            loop = False

    sys.stdout.write("\n")
    #print receipt output
    printReceipt(custName, productName, unitPrice, quantity)
    #Requirement 2.5
    #add customer to customer list if they are new
    if not existCust:
        listCustomers.append(custName)
    updateTotalSpend(dictTotalSpend, custName, calcTotalPrice(unitPrice, quantity))
    updateOrderHistory(dictOrderHistory, custName, productName, quantity)
    sys.stdout.write("\n")

"""
Originally I used globals to call the lists outside of the main function's scope.
I later found calling the list with .clear and .append worked, which is the current
implementation.
Perhaps using a set/dictionary could be good as well since that'll force uniqueness
but that'll also be weird with ordering as older Python 3 versions had dictionaries
unsorted.
The final implemention uses a list with data validation to check for duplicates.
"""
#Requirement 2.2
#Clears and sets listProducts with new products from user input
#I interpretted the requirements of 2.2 and 2.3 as two separate functionalities
#that can be called independently which is why they are separate.
#For now I've set a warning after this function to set a new price list too.
#If I had more time I would use red text on the warning.
def newProductList():
    #loop to ask for input if input was invalid
    loop = True
    while loop:
        #get input
        sys.stdout.write("Please enter a new list of products separated by spaces:\n")
        try:
            productInput = input().split()
        except Exception as e:
            printError("entering a new product list", str(e))
        else:
            if bulkValidation(
                    noDupeValid(productInput,\
                            "Please have every product be unqiue.\n"),\
                    dataStructValid(productInput, alphanumValid,\
                            "Please have every product be one word and " +\
                            "contain only alphabet or numeric characters.\n"),\
                    dataStructValid(productInput, noNullValid,\
                            "Please do not have any null inputs.\n")
            ):
                loop = False

    #set new list
    try:
        listProducts.clear()
        for item in productInput:
            listProducts.append(str(item))
        sys.stdout.write("New product list successfully set.\nPlease update the pricing.\n\n")
    except Exception as e:
        printError("creating a new product list", str(e))

#Requirement 2.3 and 2.4
#Clears and sets listProducts with new prices from user input
def newPriceList():
    #loop to ask for input if input was invalid
    loop = True
    while loop:
        #get input
        sys.stdout.write("Please enter a new list of prices separated by a space and " +\
                "without the $ symbol:\n")
        try:
            priceInput = input().split()
        except Exception as e:
            printError("entering a new price list", str(e))
        else:
            if bulkValidation(\
                    dataStructValid(priceInput, realNumValid,\
                            "Please use numbers or decimal numbers without a $ symbol.\n"),
                    dataStructValid(priceInput, noNullValid,\
                            "Please do not have any null inputs.\n")\
            ):
                loop = False

    #set new list
    try:
        listPrices.clear()
        for item in priceInput:
            listPrices.append(float(item))
        sys.stdout.write("New price list successfully set.\n\n")
    except Exception as e:
        printError("creating a new price list", str(e))

#Requirement 2.6
#prints all existing customers
def printCustomers(listCustomers:list):
    #checks if list is empty
    if not listCustomers:
        sys.stdout.write("There are currently no existing customers.")
    else:
        sys.stdout.write("Existing customers:")
        neatPrintList(listCustomers)
    sys.stdout.write("\n\n")

#Requirement 2.7
#prints product list
def printProducts(listProducts:list, listPrices:list, dictStock:dict):
    #formatting variables for the print
    padProd = 15
    padPrice = 9
    padStock = 6
    formProd = "{:<" + str(padProd) + "}"
    formPrice = "{:>" + str(padPrice) + "}"
    formStock = "{:>" + str(padStock) + "}"
    formatting = formProd + formPrice + formStock + "\n"

    #validation to see if list exists
    if not listProducts:
        sys.stdout.write("There are currently no products.\n") 
    else:
        #If I had more time I would properly set the try except to be more specific
        #and not just catch teh whole for loop
        try:
            sys.stdout.write(formatting.format("Products", "Price", "Stock"))
            for i in range(len(listProducts)):
                if i > len(listPrices) - 1 or listPrices[i] < 0:
                    price = "No Price"
                else:
                    price = formatPrice(listPrices[i])
                prod = listProducts[i]
                stock = getProdStock(prod, dictStock)
                sys.stdout.write(formatting.format(prod[:padProd], price, stock))
        except Exception as e:
            printError("printing product list", str(e))
    sys.stdout.write("\n")

#Requirement 3.3 helper function
#Gets user input on the replenish quantity with data validation
def getReplenish()->int:
    #loop to ask for input if input was invalid
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

#Requirement 3.3
#Replenish resets the dictStock list to a certain value
#inputted by the user
def replenish(dictStock:dict, listProducts:list):
    #get input
    quantity = getReplenish()
    #validation
    if not noNullValid(quantity):
        printError("replenishing stock")
    else:
        dictStock.clear()
        for prod in listProducts:
            dictStock[prod] = quantity
        sys.stdout.write("All products successfully replenished.\n\n")

#Requirement 3.4 helper function
#some data sanitation that turns Nones into 0s
def getProdStock(product:str, dictStock:dict)->int:
    #if key does not exist
    if not dictStock.get(product):
        return 0
    else:
        return dictStock.get(product)

#Requirement 3.5 helper function
#helper function that simply updates the amount spent by each customer
def updateTotalSpend(dictTotalSpend:dict, name:str, price:float):
    #if there customer is new
    if not dictTotalSpend.get(name):
        dictTotalSpend[name] = price
    #if the customer has purchased before
    else:
        dictTotalSpend[name] = dictTotalSpend.get(name) + price

#Requirement 3.5 helper function
#returns a list of customers who have spent the most
#list instead of a single string in case of a tie on spending
def getMostValued(dictTotalSpend:dict, listCustomers:list)->list:
    listNames = []
    highest = 0
    #loops through every customer
    for names in listCustomers:
        amount = dictTotalSpend.get(names)
        #if they have spent anything
        if amount:
            #if customer matches the highest spending amount
            if amount == highest:
                #add them to return list
                listNames.append(names)
            #if new highest is found
            elif amount > highest:
                #clear the list and add the new name
                listNames.clear()
                listNames.append(names)
                highest = amount
    #finally return names
    return listNames

#Requirement 3.5
#Call to print the customer who has the most total order value
#this is stored with a dictionary of all the customers
#whose values are updated every time they make a purchase.
#Their value is the total amount of money spent.
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

"""
A lot of errors occured using the direct call method of dict[key]
the dict.get(item) method returns None if no such value exists
which I found very handy.
"""
#Requirement 3.6 helper function
#Helper to simplify updating dictOrderHistory
def updateOrderHistory(dictOrderHistory:dict, name:str, prod:str, quantity:int):
    #checks if the key exists for dictOrderHistory
    if not dictOrderHistory.get(name):
        dictTempVal = {prod: quantity}
        dictOrderHistory[name] = dictTempVal 
    #checks if the value exists for dictOrderHistory from key
    elif not dictOrderHistory.get(name).get(prod):
        dictOrderHistory[name][prod] = quantity
    #this happens if there already exists the key and value
    else:
        oldVal = dictOrderHistory.get(name).get(prod)
        dictOrderHistory[name][prod] = oldVal + quantity

#Requirement 3.6 helper function
#This function is a bit of data santisation,
#it grabs the value using the two keys for dictOrderHistory
#but returns 0 if no value exists
def getOrderHistory(dictOrderHistory:dict, prod:str, name:str)->int:
    if not dictOrderHistory.get(name):
        return 0
    elif not dictOrderHistory.get(name).get(prod):
        return 0
    else:
        return dictOrderHistory.get(name).get(prod)
    return

#Requirement 3.6
#Call to print the total orderes from all customers and for which products
def printOrderHistory(listCustomers:list, listProducts:list, dictOrderHistory:dict):
    #checks if there is anything stopping the list from appearing
    if not listCustomers:
        sys.stdout.write("There have been no recorded purchases.\n")
    elif not listProducts:
        sys.stdout.write("There are no products to make a purchase history table.\n")
    else:
        #formatting variables for the print
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
            sys.stdout.write(formName.format(name)[:padName] + " ")
            for prod in listProducts:
                sys.stdout.write(" " + formProd.format(\
                        getOrderHistory(dictOrderHistory, prod, name)))
            sys.stdout.write("\n")
    sys.stdout.write("\n")

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
#Requirement 1.5, 1.6 and 2.8
if __name__ == '__main__':
    #Requirement 1.6
    """
    Both products and prices are stored as a list.
    The way the price relates to the product is the index of the price is associated
    with the index of the product, such that listPrice[0] is the price for the
    product of listProduct[0].
    This was done as I interpretted requirement 1.5 as a hard requirement.
    It was later stated the data structure of these are not rigid.
    Perhaps using a dictionary for products with the values of the keys
    lead to the price would be a neater approach but doing it this way would make
    requirement 2.3 rather difficult as it is a requirement that the prices are 
    entered as a list, though it is not impossible.
    Using classes is another possibility and would probably be the neatest approach,
    though this has not been covered in the course yet.
    """
    #Requirement 1.5
    listCustomers =[]       #list of existing customers
    listProducts = []       #list of current products
    listPrices = []         #list of prices associated with product
    dictStock = {}          #dict with product as key, stock as the value
    dictTotalSpend = {}     #dict with customer as key, float of total spendings as value
    dictOrderHistory = {}   #dict with customers as key, and a dict of products as value
                            #the 2nd dict contains the number of items purchased.

    #debugging code to automatically fill the data structures above
    #debug boolean is located at the top of the program if you wish
    #to set it to true
    if debug:
        listCustomers = ["John", "John Smith"]
        listProducts = ["invalid", "valid", "free", "outside"]
        listPrices = [-1, 12.5555, 0]
        for prod in listProducts:
            dictStock[prod] = 10

    #Requirement 2.8
    while True:
        printMenu()
        option = input()
        if   option == "1":
            makeOrder(listCustomers, listProducts, listPrices,\
                    dictStock, dictTotalSpend, dictOrderHistory)
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
