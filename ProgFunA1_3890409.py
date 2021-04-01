import sys

debug = True

#template for displaying error messages
def printError(desc:str, e:str)->str:
    sys.stdout.write("An error has occured with " + str(desc) + ", " + str(e) + ".\n")

#get name input from user
def getName():
    """
    While loop with an always true condition is used
    in order infinitely loop the prompt to the user
    if they enter it incorrectly.
    """
    loop = True
    while loop:
        sys.stdout.write("Please enter the name of the customer: ")
        custName = input()
        #Checks if input is all alpha characters.
        if custName.isalpha():
            loop = False
        else:
            sys.stdout.write("The name must start with a capital letter and the name " +\
                    "must only contain alphabet characters or spaces.\n")
    return custName

#get product input from user
def getProduct(listProducts:list)->str:
    """
    While loop with an always true condition is used
    in order infinitely loop the prompt to the user
    if they enter it incorrectly.
    """
    loop = True
    while loop:
        sys.stdout.write("Please enter the name of a product: ")
        productName = input()
        #checks to see if product exists in product list
        if productName in listProducts:
            loop = False
        else:
            sys.stdout.write("That product does not exist.\n")
    return productName

#get product quantity input from user
def getQuantity():
    """
    While loop with an always true condition is used
    in order infinitely loop the prompt to the user
    if they enter it incorrectly.
    """
    loop = True
    while loop:
        sys.stdout.write("Please enter quantity you wish to order: ")
        #checks if input is an integer
        quantity = input()
        try:
            if quantity.isdigit():
                loop = False
            else:
                sys.stdout.write("Please enter a whole number.\n")
        except Exception as e:
            printError("getting quantity input", str(e))
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
I'm not sure if this is the best way to do things because it uses globals.
defining a product class would be better but that seems outside the
scope of this course at the moment.
Perhaps using a set/dictionary could be good as well since that'll force uniqueness
but that'll also be weird with ordering.
"""
def newProductList():
    #uses global in order to change the list of products
    global listProducts
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
        except Exception as e:
            printError("creating a new product list", str(e))

        #print relevant error messages to user
        if flagUnique:
            sys.stdout.write("Please have every product be unqiue.\n")
        if flagAlpNum:
            sys.stdout.write("Please have every product be one word and " +\
                    "contain only alpha numeric characters.\n")
        #break out of loop if no errors were detected or flags raised
        #this makes it so user cannot reenter input once valid input is entered
        if not flagUnique and not flagAlpNum:
            loop = False
        sys.stdout.write("\n")

    #set new list
    sys.stdout.write("New product list successfully set.\n\n")
    listProducts = productInput

def newPriceList():
    #uses global in order to change the list of prices
    global listPrices

    loop = True
    while loop:
        #get input
        sys.stdout.write("Please enter a new list of prices separated by spaces and " +\
                "without the $ symbol: ")
        priceInput = input().split(" ")

        flagDecimal = False
        flagNeg = False

        #error checking to see if all items in products are alphanumeric
        for item in priceInput:
            if debug: print(is_float(item))
            if is_float(item):
                if float(item) < 0:
                    flagNeg = True
            else:
                flagDecimal = True

        #print relevant error messages to user
        if flagDecimal:
            sys.stdout.write("Please use numberic characters for the prices.\n")
        if flagNeg:
            sys.stdout.write("Please use positive numbers for the prices.\n")

        #get out of loop if no error detected
        if not flagDecimal and not flagNeg:
            loop = False

    #set new list
    floatListPrices = []
    for item in priceInput:
        floatListPrices.append(float(item))
    sys.stdout.write("New price list successfully set.\n\n")
    listPrices = floatListPrices

#prints product list
def printProducts(listProducts):
    #check if list is empty
    if not listProducts:
        sys.stdout.write("There are currently no products.\n\n")
    else:
        #print list as normal
        sys.stdout.write("Current products: ")
        for i in range(len(listProducts)):
            sys.stdout.write(listProducts[i])
            #separates items in list with commas
            if not i == len(listProducts) - 1:
                sys.stdout.write(", ")
            #if last item use full stop instead
            else:
                sys.stdout.write(".\n\n")

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
        listPrices = [2.90, 1]
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
        elif option == "5":
            printProducts(listProducts)
        elif option == "0":
            sys.stdout.write("Goodbye.\n")
            quit()
