# UniEats: Food Review Application for Kowloon’s Ho Man Tin and Mong Kok
## 1. Real-Life Problem to Be Addressed
In the densely populated Kowloon districts of Ho Man Tin and Mong Kok, there is a proliferation of diverse dining options (Chinese, Japanese, Thai, Korean, Western, café, etc.), leading to several critical pain points for both diners and administrators:  
- **For users**: 
  - Difficulty in efficiently filtering restaurants by key criteria (area, cuisine type, budget) to match personal preferences; 
  - Lack of localized, personalized restaurant recommendations (e.g., similar restaurants based on dining history, random picks for casual choices); 
  - No centralized platform to submit and view comprehensive restaurant reviews (including text, ratings, and image attachments); 
  - Inability to intuitively visualize restaurant locations to make location-aware dining decisions.  
- **For administrators**: 
  - Lack of a streamlined tool to manage restaurant metadata (add/update/delete entries for name, area, cuisine, budget, geographic coordinates); 
  - No systematic way to moderate user reviews (delete inappropriate content, track deleted reviews with reasons, and maintain data integrity); 
  - Absence of a unified interface to sync restaurant data with visual map displays.  

The core problem is to create a localized, user-friendly platform that centralizes restaurant discovery, review management, and administrative oversight for Ho Man Tin and Mong Kok, addressing the inefficiency of scattered dining information and unstructured review moderation in these areas.

## 2. Survey of Real-Life Solutions to the Problem
In real-world scenarios, the challenge of restaurant discovery and review management is addressed by commercial platforms and tools, with key patterns including:  
- **Consumer-facing platforms (e.g., OpenRice, Dianping)**: These platforms offer filter/sort functionality (by area, cuisine, price, rating), user-generated reviews (text + images), personalized recommendations (based on browsing/consumption history), and map integration to display restaurant locations. However, these platforms are often city-wide or national, lacking hyper-localized focus on small districts like Ho Man Tin/Mong Kok, and require internet connectivity.  
- **Administrative tools**: Restaurant management systems (e.g., POS-integrated backends) allow admins to update venue details, while review moderation tools (e.g., content management systems) enable deletion/flagging of inappropriate reviews and retention of audit trails (e.g., delete reasons). These tools are often proprietary and costly for small-scale, localized use cases.  
- **Technical implementations**: 
  - Relational databases (MySQL, SQLite) are used to store structured restaurant/review data with foreign key relationships (e.g., linking reviews to restaurants); 
  - Graph-based algorithms power "similar restaurant" recommendations; 
  - Embedded map APIs (e.g., Google Maps, OpenStreetMap) visualize geographic data; 
  - Sorting algorithms (e.g., quicksort, shell sort) optimize filter results for user experience.  

UniEats adapts these real-world solutions to a lightweight, offline-capable, hyper-localized tool for Ho Man Tin/Mong Kok, avoiding the complexity and cost of commercial platforms while retaining core functionality.

## 3. Data Structures Used and Their Usage in the Project
The project leverages multiple data structures to solve the targeted problems, each with a clear purpose:  

### 3.1 Graph (RecommendationGraph Class)
- **Structure**: Implemented as an adjacency list (dictionary `adjacency` where keys = restaurant IDs, values = lists of similar restaurant IDs).  
- **Usage**: Powers the "Similar Recommendation" feature. The graph is built by adding similarity edges between restaurant IDs (e.g., linking a Chinese restaurant in Mong Kok to another Chinese eatery in the same area). When a user selects a restaurant, the graph’s `get_similar_restaurants()` method retrieves adjacent restaurant IDs, returning a list of similar dining options. This structure is ideal for recommendation systems as it efficiently models pairwise relationships between entities.  

### 3.2 List (Dynamic Arrays)
- **Structure**: Python lists store collections of `Restaurant`/`Review` objects, filtered results, and map markers.  
- **Usage**: 
  - Stores all restaurants/reviews fetched from the database (e.g., `current_restaurants` in `UniEatsApp`); 
  - Serves as the input for the **Shell Sort** algorithm (custom implementation in `utils.py`) to sort restaurants by rating (descending), price (ascending), or name (alphabetical). Shell Sort is chosen for its efficiency on small-to-medium datasets (typical for hyper-local restaurant lists) and adaptability to custom sort keys.  

### 3.3 Relational Database (SQLite with Structured Tables)
- **Structure**: Three core tables with relational constraints:  
  - `restaurants`: Stores restaurant metadata (ID, name, area, cuisine, budget, latitude/longitude) with `id` as the primary key;  
  - `reviews`: Links to `restaurants` via `restaurant_id` (foreign key, cascading delete) to store user reviews (username, rating, comment, image path);  
  - `deleted_reviews`: Archives deleted reviews (original ID, delete reason) for audit trails.  
- **Usage**: Provides persistent, structured storage for all core data. Foreign key constraints ensure data integrity (e.g., deleting a restaurant auto-deletes its reviews), while SQL queries enable filtered retrieval (e.g., `get_reviews_by_restaurant()`, `filter_restaurants()`).  

### 3.4 Dictionary (Hash Table)
- **Structure**: Used in `RecommendationGraph` (adjacency list) and tkinter UI (e.g., `StringVar` mappings for filter dropdowns).  
- **Usage**: Enables O(1) average-time complexity for lookups (e.g., checking if a restaurant ID exists in the graph’s adjacency list) and efficient binding of UI elements to filter values (area, cuisine, budget).  

### 3.5 Map Markers (List of Tkintermapview Markers)
- **Structure**: List of map marker objects (`current_markers` in `EmbeddedMapService`).  
- **Usage**: Tracks markers added to the OpenStreetMap view to enable bulk clearing (via `clear_markers()`) and dynamic updates when filters are applied (e.g., showing only filtered restaurants on the map).

## 4. Declaration of Prior Work
This project is **original development** and not a direct fork/modification of an existing complete project. However, it draws inspiration from core functionality patterns of real-world restaurant review platforms (OpenRice, Dianping) and adapts established technical practices (e.g., SQLite for relational data, graph structures for recommendations, shell sort for local data sorting) to a lightweight, offline, district-specific application. The codebase uses standard Python libraries (tkinter, sqlite3) and open-source tools (tkintermapview, PIL) but does not reuse pre-existing project code—all logic (UI, data management, recommendations, map integration) is built from scratch for the Ho Man Tin/Mong Kok use case.  

The project also incorporates self-studied technical concepts (Shell Sort algorithm, Graph data structure) to demonstrate custom implementation of core functionality, rather than relying on pre-built libraries for sorting/recommendation logic.
