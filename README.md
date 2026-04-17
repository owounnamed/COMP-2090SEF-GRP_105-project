UniEats: Food Review Application for Kowloon’s Ho Man Tin and Mong Kok
1. Real-Life Problem to Be Addressed
In the densely populated Kowloon districts of Ho Man Tin and Mong Kok, there are many diverse dining options (Chinese, Japanese, Thai, Korean, Western, café, etc.). This lead to several big problems for diners and administrators:
For users:
Hard to quickly filter restaurants by key criteria (area, cuisine type, budget) to match their preferences;
No localized, personalized restaurant recommendations (like similar restaurants based on dining history, random picks for casual choices);
No central platform to submit and view full restaurant reviews (include text, ratings, and image attachments);
Can’t easily see restaurant locations on a map to make location-based dining decisions.
For administrators:
No simple tool to manage restaurant metadata (add/update/delete entries for name, area, cuisine, budget, geographic coordinates);
No systematic way to check user reviews (delete inappropriate content, track deleted reviews with reasons, and keep data integrity);
No single interface to sync restaurant data with map displays.
The main problem is to build a localized, easy-to-use platform that brings together restaurant discovery, review management, and administrative oversight for Ho Man Tin and Mong Kok. It solve the inefficiency of scattered dining information and unstructured review moderation in these areas.
2. Survey of Real-Life Solutions to the Problem
In real life, commercial platforms and tools address the challenge of restaurant discovery and review management. Key patterns are:
Consumer-facing platforms (e.g., OpenRice, Dianping): These platforms have filter/sort functions (by area, cuisine, price, rating), user-made reviews (text + images), personalized recommendations (based on browsing/consumption history), and map integration to show restaurant locations. But these platforms are often city-wide or national, they lack hyper-local focus on small districts like Ho Man Tin/Mong Kok, and need internet to work.
Administrative tools: Restaurant management systems (e.g., POS-integrated backends) let admins update venue details, while review moderation tools (e.g., content management systems) allow delete/flag inappropriate reviews and keep audit trails (e.g., delete reasons). These tools are often proprietary and expensive for small, localized use cases.
Technical implementations:
Relational databases (MySQL, SQLite) store structured restaurant/review data with foreign key relationships (e.g., link reviews to restaurants);
Graph-based algorithms power "similar restaurant" recommendations;
Embedded map APIs (e.g., Google Maps, OpenStreetMap) show geographic data;
Sorting algorithms (e.g., quicksort, shell sort) make filter results better for users.
UniEats adapt these real-world solutions into a lightweight, offline tool for Ho Man Tin/Mong Kok. It avoid the complexity and cost of commercial platforms but keep core functions.
3. Data Structures Used and Their Usage in the Project
The project uses multiple data structures to solve the target problems, each with a clear purpose:
3.1 Graph (RecommendationGraph Class)
Structure: Made as an adjacency list (dictionary adjacency where keys = restaurant IDs, values = lists of similar restaurant IDs).
Usage: Powers the "Similar Recommendation" feature. The graph is built by adding similarity edges between restaurant IDs (e.g., link a Chinese restaurant in Mong Kok to another Chinese eatery in the same area). When a user select a restaurant, the graph’s get_similar_restaurants() method gets adjacent restaurant IDs, return a list of similar dining options. This structure is perfect for recommendation systems because it efficiently model pairwise relationships between entities.
3.2 List (Dynamic Arrays)
Structure: Python lists store collections of Restaurant/Review objects, filtered results, and map markers.
Usage:
Stores all restaurants/reviews get from the database (e.g., current_restaurants in UniEatsApp);
Used as input for the Shell Sort algorithm (custom implementation in utils.py) to sort restaurants by rating (descending), price (ascending), or name (alphabetical). Shell Sort is chosen because it is efficient on small-to-medium datasets (typical for hyper-local restaurant lists) and adapt to custom sort keys.
3.3 Relational Database (SQLite with Structured Tables)
Structure: Three core tables with relational constraints:
restaurants: Stores restaurant metadata (ID, name, area, cuisine, budget, latitude/longitude) with id as primary key;
reviews: Links to restaurants via restaurant_id (foreign key, cascading delete) to store user reviews (username, rating, comment, image path);
deleted_reviews: Archives deleted reviews (original ID, delete reason) for audit trails.
Usage: Provides persistent, structured storage for all core data. Foreign key constraints ensure data integrity (e.g., delete a restaurant auto-deletes its reviews), while SQL queries enable filtered retrieval (e.g., get_reviews_by_restaurant(), filter_restaurants()).
3.4 Dictionary (Hash Table)
Structure: Used in RecommendationGraph (adjacency list) and tkinter UI (e.g., StringVar mappings for filter dropdowns).
Usage: Enables O(1) average-time complexity for lookups (e.g., check if a restaurant ID exists in the graph’s adjacency list) and efficient binding of UI elements to filter values (area, cuisine, budget).
3.5 Map Markers (List of Tkintermapview Markers)
Structure: List of map marker objects (current_markers in EmbeddedMapService).
Usage: Tracks markers added to the OpenStreetMap view to allow bulk clearing (via clear_markers()) and dynamic updates when filters are applied (e.g., show only filtered restaurants on the map).
4. Declaration of Prior Work
This project is original development and not a direct fork/modification of an existing complete project. But it take inspiration from core functions of real-world restaurant review platforms (OpenRice, Dianping) and adapt established technical practices (e.g., SQLite for relational data, graph structures for recommendations, shell sort for local data sorting) to a lightweight, offline, district-specific application. The codebase uses standard Python libraries (tkinter, sqlite3) and open-source tools (tkintermapview, PIL) but do not reuse pre-existing project code—all logic (UI, data management, recommendations, map integration) is built from scratch for the Ho Man Tin/Mong Kok use case.
The project also include self-studied technical concepts (Shell Sort algorithm, Graph data structure) to show custom implementation of core functionality, instead of rely on pre-built libraries for sorting/recommendation logic.
