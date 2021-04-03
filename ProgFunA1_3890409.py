import sys

debug = True

#template for displaying error messages
def printError(desc:str, e:str)->str:
    sys.stdout.write("An error has occured with " + str(desc) + ", " + str(e) + ".\n")

#get name input from user
def getName()->str:
    """
    Originally I used while(True) to keep a loop going on constantly asking for input until
    broken out of the loop.
    Currently a boolean declared "loop" initiated as "True" is used which I can later
    change inside the while loop to the value of "False".
    """
    loop = True
    while loop:
        #get input
        sys.stdout.write("Please enter the name of the customer: ")
        custName = input()

        flagChar = False
        #Checks if input is all alpha characters by checking
        #every character individually in the input string
        for ch in custName:
            if not (ch.isalpha() or ch.isspace()):
                flagChar = True

        #if states are separated (else isn't used)
        #to keep structure consistent with other input validations,
        #this layout is neater if I have to add more input validation later
        if flagChar:
            sys.stdout.write("The name must only contain alphabet characters or spaces.\n")
        if not flagChar:
            loop = False

    return custName

#get product input from user
def getProduct(listProducts:list)->str:
    loop = True
    while loop:
        #get input
        sys.stdout.write("Please enter the name of a product: ")
        productName = input()

        #checks to see if product exists in product list
        if productName in listProducts:
            loop = False
        else:
            sys.stdout.write("That product does not exist.\n")

    return productName

#get product quantity input from user
def getQuantity()->int:
    loop = True
    while loop:
        #get input
        sys.stdout.write("Please enter quantity you wish to order: ")
        quantity = input()

        try:
            #checks if input is a positive integer
            if quantity.isdecimal():
                loop = False
            else:
                sys.stdout.write("Please enter a positive whole number.\n")
        except Exception as e:
            printError("getting quantity amouont", str(e))
            return

    return int(quantity)

#checks to see if customer's name exists in the existing customers list
def isExistingCustomer(custName, listCustomers):
    if debug: print(listCustomers)
    #true if existing, false if new
    if custName in listCustomers:
        if debug: print("Existing!\n")
        return True
    if debug: print("Not existing!\n")
    return False

#calculate the price of single product with discount
def calcUnitPrice(existingCustomer, productName, listProducts, listPrices):
    #get product index
    index = listProducts.index(productName)
    #get price using product index
    try:
        if index > len(listPrices) or index < 0:
            #if no price listed, outside of list
            return
        else:
            price = listPrices[index]
    except Exception as e:
        printError("calculating pricing", str(e))
        return
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

#formats price to be 2 decimal places and rounds pricing
def formatPrice(price:float)->float:
    return "{:.2f}".format(round(price, 2))

#prints output as directed in part 1 of assignment
def printReceipt(custName, productName, price, quantity):
    sys.stdout.write(custName + " purchased " + str(quantity) + " x " +\
            productName + "\n")
    sys.stdout.write("Unit price:  $" + str(formatPrice(price)) + "\n")
    sys.stdout.write("Total price: $" + str(formatPrice(calcTotalPrice(price, quantity)))\
            + "\n\n")

#print the menu options
def printMenu():
    sys.stdout.write(\
            "Please enter an option:\n" +\
            "1. Make a new purchase\n" +\
            "2. Replace product list\n" +\
            "3. Replace product prices\n" +\
            "4. Display all existing customers\n" +\
            "5. Display all products and prices\n\n" +\
            "0. Exit\n\n" +\
            "> "\
    )

#ask for input to make order
def makeOrder(listCustomers, listProducts, listPrices):
    #get input from customer
    custName = getName()
    productName = getProduct(listProducts)
    quantity = getQuantity()
    sys.stdout.write("\n")

    #boolean to check user is existing customer
    discountCustomer = isExistingCustomer(custName, listCustomers)

    #print receipt output
    printReceipt(custName, productName,\
            calcUnitPrice(discountCustomer, productName, listProducts, listPrices),\
            quantity)

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
        listPrices.clear()
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
                #only 1 or 0 decimals were inputted
                if not item.replace(".", "", 1).isdecimal():
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

def neatPrintList(neatList:list, collection:str):
    if not neatList:
        sys.stdout.write("There are currently no " + str(collection) + ".")
    else:
        #range is used instead of "in list" to utilise index
        sys.stdout.write("Current " + str(collection) + ": ")
        for i in range(len(neatList)):
            sys.stdout.write(neatList[i])
            #separates items in list with commas
            if not i == len(neatList) - 1:
                sys.stdout.write(", ")
            #if last item use full stop instead
            else:
                sys.stdout.write(".")
    sys.stdout.write("\n\n")
    

#prints product list
def printProducts(listProducts, listPrices):
    #neatPrintList(listProducts, "products")
    if not listProducts:
        sys.stdout.write("There are currently no products.") 
    else:
        try:
            for i in range(len(listProducts)):
                if i < len(listPrices):
                    price = formatPrice(listPrices[i])
                else:
                    price = "No Price"
                sys.stdout.write("{:<15}{:>9}\n".format(listProducts[i], price))
        except Exception as e:
            printError("printing product list", str(e))
    sys.stdout.write("\n")


def printCustomers(listCustomers):
    neatPrintList(listCustomers, "customers")

#main init
if __name__ == '__main__':
    #temporary customer list
    listCustomers =[]
    #temporary product list
    listProducts = []
    #temporary product list
    listPrices = []

    if debug:
        listCustomers = ["John Smith", "Jane Doe"]
        listProducts = ["shortblack", "cappuccino", "latte"]
        listPrices = [2.900000001, 1]
        print(listProducts)

    while True:
        printMenu()
        option = input()
        if   option == "1":
            makeOrder(listCustomers, listProducts, listPrices)
        elif option == "2":
            newProductList()
        elif option == "3":
            newPriceList()
        elif option == "4":
            printCustomers(listCustomers)
        elif option == "5":
            printProducts(listProducts, listPrices)
        elif option == "0":
            sys.stdout.write("Goodbye.\n")
            quit()
