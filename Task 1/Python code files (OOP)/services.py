import random
from models import RecommendationGraph
from utils import DistanceCalculator, ShellSort, save_review_image, MAP_AVAILABLE


class RestaurantService:
    def __init__(self, db_manager):
        self.db = db_manager
        self.graph = RecommendationGraph()
        self.build_sample_graph()

    def build_sample_graph(self):
        # Build a simple graph for recommendation.
        self.graph = RecommendationGraph()
        restaurants = self.db.get_restaurants()
        id_list = []

        for restaurant in restaurants:
            id_list.append(restaurant.id)
            self.graph.add_restaurant(restaurant.id)

        if len(id_list) >= 2:
            self.graph.add_similarity(id_list[0], id_list[1])
        if len(id_list) >= 3:
            self.graph.add_similarity(id_list[0], id_list[2])
        if len(id_list) >= 4:
            self.graph.add_similarity(id_list[1], id_list[3])
        if len(id_list) >= 5:
            self.graph.add_similarity(id_list[2], id_list[4])
        if len(id_list) >= 6:
            self.graph.add_similarity(id_list[3], id_list[5])

    def refresh_graph(self):
        self.build_sample_graph()

    def get_all_restaurants(self):
        return self.db.get_restaurants()

    def filter_restaurants(self, area=None, cuisine=None, max_budget=None):
        restaurants = self.db.get_restaurants()
        results = []

        for restaurant in restaurants:
            area_ok = True
            cuisine_ok = True
            budget_ok = True

            if area and area != "All":
                if restaurant.area != area:
                    area_ok = False

            if cuisine and cuisine != "All":
                if restaurant.cuisine != cuisine:
                    cuisine_ok = False

            if max_budget is not None:
                if restaurant.price_level > max_budget:
                    budget_ok = False

            if area_ok and cuisine_ok and budget_ok:
                results.append(restaurant)

        return results

    def sort_restaurants(self, restaurants, sort_key):
        if sort_key == "Rating":
            return ShellSort.sort(restaurants, lambda r: r.avg_rating, True)
        elif sort_key == "Price":
            return ShellSort.sort(restaurants, lambda r: r.price_level, False)
        else:
            return ShellSort.sort(restaurants, lambda r: r.name.lower(), False)

    def recommend_by_history(self, selected_restaurant_id):
        similar_ids = self.graph.get_similar_restaurants(selected_restaurant_id)
        all_restaurants = self.db.get_restaurants()
        result = []

        for restaurant in all_restaurants:
            if restaurant.id in similar_ids:
                result.append(restaurant)

        return result

    def random_recommendation(self, restaurants):
        if restaurants:
            return random.choice(restaurants)
        return None

    def restaurants_with_distance(self, user_lat, user_lon):
        restaurants = self.db.get_restaurants()
        result = []

        for restaurant in restaurants:
            distance = DistanceCalculator.haversine(
                user_lat, user_lon, restaurant.latitude, restaurant.longitude
            )
            result.append((restaurant, distance))

        result.sort(key=lambda item: item[1])
        return result

    def save_image(self, source_path):
        return save_review_image(source_path)


class EmbeddedMapService:
    def __init__(self, map_widget=None):
        self.map_widget = map_widget
        self.current_markers = []

    def set_map_widget(self, map_widget):
        self.map_widget = map_widget

    def clear_markers(self):
        for marker in self.current_markers:
            try:
                marker.delete()
            except Exception:
                pass
        self.current_markers = []

    def show_restaurants_on_map(self, restaurants, center_lat=22.3180, center_lon=114.1740):
        if MAP_AVAILABLE is False:
            return False
        if self.map_widget is None:
            return False

        self.clear_markers()
        self.map_widget.set_position(center_lat, center_lon)
        self.map_widget.set_zoom(15)

        for restaurant in restaurants:
            text = (
                restaurant.name + "\n"
                + "Area: " + restaurant.area + "\n"
                + "Cuisine: " + restaurant.cuisine + "\n"
                + "Budget: HKD " + str(restaurant.price_level) + "\n"
                + "Rating: " + format(restaurant.avg_rating, ".1f")
            )
            marker = self.map_widget.set_marker(restaurant.latitude, restaurant.longitude, text=text)
            self.current_markers.append(marker)

        return True
