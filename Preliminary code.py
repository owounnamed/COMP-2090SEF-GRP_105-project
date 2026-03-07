import random

# simple data storage
restaurants = []
reviews = []


# add restaurant
def add_restaurant(name, area):
    restaurants.append({"name": name, "area": area})


# show restaurants
def show_restaurants():
    return restaurants


# add review
def add_review(user, restaurant, comment):
    reviews.append({
        "user": user,
        "restaurant": restaurant,
        "comment": comment
    })


# random restaurant recommendation
def random_restaurant():
    if restaurants:
        return random.choice(restaurants)
    else:
        return "No restaurant available"


# test example
add_restaurant("Cafe One", "Mong Kok")
add_restaurant("Food House", "Ho Man Tin")

add_review("Tom", "Cafe One", "Very tasty!")

print("Restaurants:", show_restaurants())
print("Random suggestion:", random_restaurant())
