from abc import ABC, abstractmethod


class Person(ABC):
    # Abstract class for OOP abstraction.
    def __init__(self, username):
        self._username = username

    @property
    def username(self):
        return self._username

    @abstractmethod
    def get_role(self):
        pass


class User(Person):
    def get_role(self):
        return "User"


class Admin(Person):
    def get_role(self):
        return "Admin"


class Review:
    def __init__(self, restaurant_id, username, rating, comment, image_path=""):
        self.restaurant_id = restaurant_id
        self.username = username
        self.rating = rating
        self.comment = comment
        self.image_path = image_path

    def __str__(self):
        if self.image_path:
            photo_text = self.image_path
        else:
            photo_text = "No image"

        return (
            "User: " + str(self.username) + "\n"
            "Rating: " + str(self.rating) + "/5\n"
            "Comment: " + str(self.comment) + "\n"
            "Photo: " + photo_text
        )


class Restaurant:
    def __init__(self, restaurant_id, name, area, cuisine, price_level, latitude, longitude, avg_rating=0.0):
        self.id = restaurant_id
        self.name = name
        self.area = area
        self.cuisine = cuisine
        self.price_level = price_level
        self.latitude = latitude
        self.longitude = longitude
        self.avg_rating = avg_rating

    def display_text(self):
        return (
            self.name
            + " | " + self.area
            + " | " + self.cuisine
            + " | Budget: HKD " + str(self.price_level)
            + " | Avg Rating: " + format(self.avg_rating, ".1f")
        )


class FeaturedRestaurant(Restaurant):
    # This shows inheritance and polymorphism.
    def __init__(self, restaurant_id, name, area, cuisine, price_level, latitude, longitude, avg_rating=0.0, tag="Popular"):
        Restaurant.__init__(self, restaurant_id, name, area, cuisine, price_level, latitude, longitude, avg_rating)
        self.tag = tag

    def display_text(self):
        return "[Featured: " + self.tag + "] " + Restaurant.display_text(self)


class RecommendationGraph:
    # Self-study data structure: Graph
    def __init__(self):
        self.adjacency = {}

    def add_restaurant(self, restaurant_id):
        if restaurant_id not in self.adjacency:
            self.adjacency[restaurant_id] = []

    def add_similarity(self, source_id, target_id):
        self.add_restaurant(source_id)
        self.add_restaurant(target_id)

        if target_id not in self.adjacency[source_id]:
            self.adjacency[source_id].append(target_id)

    def get_similar_restaurants(self, restaurant_id):
        if restaurant_id in self.adjacency:
            return self.adjacency[restaurant_id]
        return []
