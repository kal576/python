menu  ={
    "latte":{
        "ingredients":{
            "water":200,
            "milk":100,
            "coffee":20,
        },
        "cost":150

    },
    "espresso":{

        "ingredients":{
            "water":100,
            "coffee":40,
        },
        "cost":200
    },
    "cappuccino":{
        "ingredients":{
            "water":80,
            "milk":50,
            "coffee":10,

        },
        "cost":100
    }
}
def check_resources(ordered_ingredients):
    for item in ordered_ingredients:
        if ordered_ingredients[item]>resources[item]:
            print(f"sorry the {item} is not enough")
            return False
    return True

profit=0
resources={
    "water":500,
    "milk":200,
    "coffee":100,

}
def process_coin():
    print("please insert coins:")
    #total=0
    coins_five=int(input("how many ksh 5 coins?"))
    coins_ten=int(input("how many ksh 10 coins?"))
    coins_twenty=int(input("how many ksh 20 coins?"))
    total=coins_five*5 + coins_ten*10 + coins_twenty*20
    return total
def is_payment_successful(money_received,coffee_cost):
    if money_received>=coffee_cost:
        global profit
        profit+=coffee_cost
        change=money_received-coffee_cost
        print(f"here is your ksh{change} change")
        return True
    else:
        print("sorry that,s not enough money.money refunded")
        return False
def make_coffee(coffee_name,coffee_ingredients):
    for item in coffee_ingredients:
        resources[item]-= coffee_ingredients[item]
    print(f"here is your {coffee_name}.. enjoy")
    #os.system('cls')
is_on=True
while is_on:
    choice=input("what will you have?(latte/espresso/cappuccino?:\n")
    if choice=="off":
        is_on=False
    elif choice=="report":
        print(f"water={resources['water']}ml")
        print(f"milk={resources['milk']}ml")
        print(f"coffee={resources['coffee']}")
        print(f"money=ksh{profit}")
    else:
        coffee_type=menu[choice]
        print(coffee_type)
        if check_resources(coffee_type['ingredients']):
            payment=process_coin()
            if is_payment_successful(payment,coffee_type['cost']):
                make_coffee(choice,coffee_type['ingredients'])

    #latteos.system('cls')



 