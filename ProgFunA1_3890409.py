import sys
import re

debug = True

#get name input from user
def getName():
    """
    While loop with an always true condition is used
    in order infinitely loop the prompt to the user
    if they enter it incorrectly.
    """
    while True:
        sys.stdout.write("Please enter the name of the customer: ")
        custName = input()
        """
        Regular expression is used to force the first letter
        to be a capitalised alpha character while the rest of the
        regex simply checks that it is an alpha character or space.
        A better regex could probably be used in order to enforce
        only a single space between words and to enforce a capital
        letter infront of every new word.
        """
        #Checks if input is all alpha characters.
        if re.match('([A-Z][a-z]*)', custName):
            break
        else:
            sys.stdout.write("The name must start with a capital letter and the name must only contain alphabet characters or spaces.\n")
    return custName

#get product input from user
def getProduct(listProducts):
    """
    While loop with an always true condition is used
    in order infinitely loop the prompt to the user
    if they enter it incorrectly.
    """
    while True:
        sys.stdout.write("Please enter the name of a product: ")
        productName = input()
        #checks to see if product exists in product list
        if productName in listProducts:
            break
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
    while True:
        sys.stdout.write("Please enter quantity you wish to order: ")
        #checks if input is an integer
        try:
            quantity = int(input())
            break
        except:
            sys.stdout.write("Please enter a whole number.\n")
    return quantity

#checks to see if customer's name exists in the existing customers list
def isExistingCustomer(custName, listCustomers):
    #true if existing, false if new
    if custName in listCustomers:
        return True
    return False

#calculate the price of single product with discount
def calcUnitPrice(existingCustomer, productName, listProducts, listPrices):
    #get product index
    index = listProducts.index(productName)
    #get price using product index
    try:
        if index > len(listPrices) or index < 0:
            #if no price listed, outside of list
            return 0.0
        else:
            price = listPrices[index]
    except:
        sys.stdout.write("An error has occurred at pricing.\n")
        return 0.0
    #if existing customer apply 10% discount
    if existingCustomer:
        price *= 0.9
    return price

#mulitplies price by quantity
def calcTotalPrice(price, quantity):
    return price * quantity

#formats price to be 2 decimal places and rounds pricing
def formatPrice(price):
    return "{:.2f}".format(round(price, 2))

#prints output as directed in part 1 of assignment
def printReceipt(custName, productName, price, quantity):
    sys.stdout.write(custName + " purchased " + str(quantity) + " x " + productName + "\n")
    sys.stdout.write("Unit price:  $" + str(formatPrice(price)) + "\n")
    sys.stdout.write("Total price: $" + str(formatPrice(calcTotalPrice(price, quantity)))\
            + "\n\n")

def printMenu():
    sys.stdout.write("Please enter an option:\n")
    sys.stdout.write("1. Make a new purchase\n")
    sys.stdout.write("2. Replace product list\n")
    sys.stdout.write("3. Replace product prices\n")
    sys.stdout.write("4. Display all existing customers\n")
    sys.stdout.write("5. Display all products and prices\n\n")
    sys.stdout.write("0. Exit\n\n")
    sys.stdout.write("> ")

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
I think defining a product class would be better but that seems outside the
scope of this course at the moment.
Perhaps using a dictionary could be good as well.
"""
def newProductList():
    #uses global in order to change the list of products
    global listProducts
    #get input
    sys.stdout.write("Please enter a new list of products separated by spaces:\n")
    productInput = input().split()
    #error checking to see if all items in products are alphanumeric
    flag = False
    for item in productInput:
        if not item.isalnum():
            flag = True
    if flag:
        sys.stdout.write("Please use alphanumeric characters with each product separated by spaces.\n\n")
    else:
        #set new list
        sys.stdout.write("New product list successfully set.\n\n")
        listProducts = productInput

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
            if not i == len(listProducts) - 1:
                sys.stdout.write(", ")
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
        listcustomers = ["John Smith", "Jane Doe"]
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
        elif option == "5":
            printProducts(listProducts)
        elif option == "0":
            sys.stdout.write("Goodbye.\n")
            quit()
