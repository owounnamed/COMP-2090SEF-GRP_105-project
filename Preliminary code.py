import random

# simple data storage
restaurants_list = []
reviews_list = []


# add restaurant
def add_restaurant(name, area):
    restaurants_list.append({"name": name, "area": area})


# show restaurants
def show_restaurants():
    return restaurants_list


# add review
def add_review(user, restaurant, comment):
    reviews_list.append({
        "user": user,
        "restaurant": restaurant,
        "comment": comment
    })


# random restaurant recommendation
def random_restaurant():
    if restaurants_list:
        return random.choice(restaurants_list)
    else:
        return "No restaurant available"

def search_restaurant(name):
    target = next((x for x in restaurants_list if x["name"] == name), None)
    if target:
        print("Restaurant found: ", target["name"], "\n\t\tArea: ", target["area"])
    else:
        print("No restaurant found!")

def reviews(name):
    found = False
    for i in reviews_list:
        if i["restaurant"] == name:
            print(i["user"] + ":", i["comment"])
            found = True
    if not found:
        print(name, "has no comment currently")
    

# test example
add_restaurant("Cafe One", "Mong Kok")
add_restaurant("Food House", "Ho Man Tin")

add_review("Tom", "Cafe One", "Very tasty!")

print("Restaurants:", show_restaurants())
print("Random suggestion:", random_restaurant())
