import sys
import re

#get name input from user
def getName():
    #While loop with an always true condition is used
    #in order infinitely loop the prompt to the user
    #if they enter it incorrectly.
    while True:
        sys.stdout.write("Please enter the name of the customer: ")
        custName = input()
        #Checks if input is all alpha characters.
        #Regular expression is used to force the first letter
        #to be a capitalised alpha character while the rest of the
        #regex simply checks that it is an alpha character or space.
        #A better regex could probably be used in order to enforce
        #only a single space between words and to enforce a capital
        #letter infront of every new word.
        #FIX THIS LATER
        if re.match('([A-Z][a-z]*)', custName):
            break
        else:
            sys.stdout.write("The name must start with a capital letter and the name must only contain alphabet characters or spaces.\n")
    return custName

#get product input from user
def getProduct(listProducts):
    #While loop with an always true condition is used
    #in order infinitely loop the prompt to the user
    #if they enter it incorrectly.
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
    #While loop with an always true condition is used
    #in order infinitely loop the prompt to the user
    #if they enter it incorrectly.
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
        price = listPrices[index]
    #if no price listed, outside of list
    except:
        #set price to 0
        return 0
    #apply 10% discount if existing customer
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

#main init
if __name__ == '__main__':
    #temporary customer list
    listCustomers = ["John Smith", "Jane Doe"]
    #temporary product list
    listProducts = ["short black", "cappuccino", "latte"]
    #temporary product list
    listPrices = [2.90, 1]

    while True:
        printMenu()
        option = input()
        if option == "1":
            makeOrder(listCustomers, listProducts, listPrices)
        elif option == "0":
            sys.stdout.write("Goodbye.\n")
            quit()
