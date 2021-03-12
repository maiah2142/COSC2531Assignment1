import sys
import re
from decimal import Decimal

#get name input
def getName():
    while True:
        sys.stdout.write("Please enter the name of the customer: ")
        custName = input()
        #checks if input is all alpha characters
        if re.match('^[A-Za-z][A-Za-z\s]+$', custName):
            break
        else:
            sys.stdout.write("The name must contain alphabet characters.\n")
    return custName

#get product input
def getProduct(listProducts):
    while True:
        sys.stdout.write("Please enter the name of a product: ")
        productName = input()
        #checks to see if product exists
        try:
            listProducts.index(productName)
            break
        except:
            sys.stdout.write("That product does not exist.\n")
    return productName

#get product quantity input
def getQuantity():
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
    #if no price listed, set price to
    except:
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

def printReceipt(custName, productName, price, quantity):
    sys.stdout.write(custName + " purchased " + str(quantity) + " x " + productName + "\n")
    sys.stdout.write("Unit price:  $" + str(formatPrice(price)) + "\n")
    sys.stdout.write("Total price: $" + str(formatPrice(calcTotalPrice(price, quantity)))\
            + "\n\n")

if __name__ == '__main__':
    #temporary customer list
    listCustomers = ["John Smith", "Jane Doe"]
    #temporary product list
    listProducts = ["short black", "cappuccino", "latte"]
    #temporary product list
    listPrices = [2.90, 1]

    #get input from customer
    custName = getName()
    productName = getProduct(listProducts)
    quantity = getQuantity()
    sys.stdout.write("\n")

    #generate price checks
    discountCustomer = isExistingCustomer(custName, listCustomers)

    #print receipt output
    printReceipt(custName, productName,\
            calcUnitPrice(discountCustomer, productName, listProducts, listPrices),\
            quantity)
