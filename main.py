
print("\t*************************************")
print("\t****  Express!  ****")
print("\t*************************************")


while True:             
    user_input = input("Choice (a/s/r/x): ")
    if user_input not in ["a", "s", "r", "x"]:
        print("a = add customer")
        print("s = serve customer")
        print("r = show report")
        print("x = exit\n")

    if user_input == "a":
        customer_mobile = input("Please enter a mobile number: ")
        customer.add_customer(customer_mobile)
    
    if user_input == "s":
        customer_mobile = input("Please enter a mobile number: ")
        customer.serve_customer(customer_mobile)

    if user_input == "r":
        customer.show_report()
        
    if user_input == "x":
        print("Bye!")
        break
