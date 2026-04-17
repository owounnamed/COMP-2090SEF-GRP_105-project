UniEats: Food Review Application for Kowloon's Ho Man Tin and Mong Kok
1. Real-Life Problem to Be Addressed
Ho Man Tin and Mong Kok, Kowloon districts, boast many diverse restaurant options (Chinese, Japanese, Thai, Korean, Western, café-style, etc.). This has lead to several major issues for both users and administrators:
Users' side:
Cannot efficiently filter restaurants according to important attributes (area, cuisine type, budget);
Lack of personalized restaurant recommendation (similiar restaurants according to dining history, random picks, etc.);
Lack of centralized platform for posting and viewing full reviews (with text, rating, and image attachment);
Cannot easily find restaurant locations on the map.
Admins' side:
Need of tool for managing restaurant metadata (create/add/update/delete records for name, area, cuisine type, budget, geographical coordinates, etc.);
Need of tool for reviewing and moderating reviews (delete inappropriate posts, archive deleted reviews along with delete reasons, etc.);
Need of tool for updating map information (for restaurant names and other relevant attributes).
The main problem is to create an efficient localized platform combining restaurant recommendation, review management and administration.
2. Survey of Real-Life Solutions to the Problem
In real life, commercial solutions tackle the task of restaurant discovery and management. Key approaches are:
Platforms for consumers (e.g., OpenRice, Dianping): have filter/sorting function according to different parameters (area, cuisine type, price level), user-provided restaurant reviews (including text and images), personal recommendations for users (based on their browsing/consumption history), mapping function which allows finding restaurant location. However, these platforms tend to be nationwide/citywide rather than district-specific and they require constant internet connection.
Tools for administrations: restaurant management systems provide ability to add/update restaurant entries while review tools allow flagging/deleting inappropriate reviews and maintaining an audit trail with delete reasons (e a.). These tools often proprietary and are expensive in terms of maintenance cost.
Technical approach:
Use relational database (e.g., MySQL or SQLite) with foreign keys to store structured restaurant/review data;
Implement graph-based algorithms which can generate "similar restaurant" recommendation;
Embed map API in order to visualize restaurant location data (Google Maps, OpenStreetMap and other);
Implement sorting algorithms to enhance filtering experience (quicksort, shellsort, etc.)
UniEats adapts these real-life techniques but avoids using commercial tools by creating a simple solution without internet connection for Ho Man Tin and Mong Kok districts.
3. Data Structures Used and Their Usage in the Project
Several kinds of data structures were used in the project to address specified problems:
3.1 Graph (RecommendationGraph class):
Structure: implemented as an adjacency list of graph (dictionary adjacency with keys - restaurant IDs, values - lists of restaurant IDs connected with edge).
Usage: enables the "Similar Recommendation" feature. Adjacency between restaurant IDs can be created through specifying similarity relations (e g., connecting two Chinese restaurants located in the same area). When selected, the graph returns a list of similar restaurants with respect to the selected one by the means of get_similar_restaurants() method. The graph data structure is perfect for creating recommendation systems.
3.2 List (Dynamic arrays):
Structure: Python list can contain Restaurant/Review objects and lists for filtered results and map markers.
Usage:
Contains all restaurant/review entries taken from the database (current_restaurants variable in UniEatsApp);
Serves as input data for Shell Sort algorithm (implemented in utils.py), which performs sorting by rating (desc), price (asc) or name (alphabetically). Such algorithm was chosen due to its simplicity, efficiency on small to medium-size data (characteristic for localized restaurant lists) and adaptability for sorting by specific key.
3.3 Relational Database (SQLite + structured tables):
Structure: three core tables, including foreign key constraints for maintaining integrity of data:
restaurants - contains restaurant attributes (ID, name, area, cuisine type, budget, latitude/longitude); ID is a primary key;
reviews - links restaurant records through restaurant_id (foreign key with on_delete cascade); allows adding reviews (user name, rating, comment, image);
deleted_reviews - archive table for keeping deleted reviews (original ID, deletion reason).
Usage: enables persistent storage of data. Foreign key allows maintaining integrity of relations (deleting restaurant automatically deletes its reviews); allows retrieving filtered data through queries.
3.4 Dictionary (hash table):
Structure: used in RecommendationGraph (as adjacency list) and tkinter UI (StringVar mapping for filter options in drop-down menu).
Usage: allows implementing O(1) look-ups (e g., checking whether ID is stored in an adjacency list of recommendation graph) and fast bind operations in UI (mapping filter options - area, cuisine type, budget).
3.5 Map Markers (list of Tkintermapview.Marker objects):
Structure: list of Marker objects, stored in current_markers variable in EmbeddedMapService class.
Usage: tracks Marker objects added to OpenStreetMap in order to implement clear_markers() method which allows batch deleting map markers. Markers list also helps implementing filtered map view according to applied filters.
4. Declaration of Prior Work
This project involves original development of software which is not a fork from any existing project. However, the code borrows some ideas implemented by real-world applications (e.g., OpenRice, Dianping) but applies them to a localized, district-specific restaurant review platform. Technical methods such as relational data storage (SQLite), recommendation (graph), sorting (shell sort) were borrowed and adapted to the project requirements. No prior projects are reused; standard Python modules (tkinter, sqlite3) and open-source projects (tkintermapview, PIL) are used but not copied in any form; UI, database, recommendation and map modules were implemented from scratch. Moreover, several self-studied techniques (Shellsort algorithm, Graph data structure) were utilized in order to demonstrate implementation of core functionalities.
