BE AWARE, BE SAFE – Disaster Preparedness and Response System

BE AWARE, BE SAFE is a Python-based desktop application designed to provide real-time disaster preparedness and response information. It allows users to access emergency hotlines, manage disaster information, send safe/location messages, and view evacuation maps.


Features

Dashboard: Central hub providing access to all app functions.

Emergency Hotlines: Scrollable list of key hotlines with copy-to-clipboard functionality.

Disaster Info CRUD: Add, update, delete, and view disaster events with details such as type, date, location, overview, and safety tips.

Send Safe / Location: Quickly send an “I am safe” message with detected GPS location.

Evacuation Map: Interactive map showing evacuation points and routes using TkinterMapView.

Visual Design: Modern dashboard layout with custom colors, fonts, and images.


DASHBOARD
<img width="898" height="630" alt="Screenshot 2025-12-11 195618" src="https://github.com/user-attachments/assets/f7e54d7b-b40e-4aad-a918-7408afb36519" />
Hotlines
<img width="939" height="632" alt="Screenshot 2025-12-11 195655" src="https://github.com/user-attachments/assets/1c1cbc5a-5365-458f-9260-00d8b9cc402e" />
Disaster Info
<img width="1572" height="740" alt="Screenshot 2025-12-11 195705" src="https://github.com/user-attachments/assets/093078e4-2568-4164-9500-8100e69908a2" />
Send Safe / Location
<img width="1175" height="636" alt="Screenshot 2025-12-11 195713" src="https://github.com/user-attachments/assets/2e0fe59a-834f-4d10-88f7-e61f81e343a2" />
Evacuation Map
<img width="1342" height="641" alt="Screenshot 2025-12-11 195645" src="https://github.com/user-attachments/assets/ff3c96fb-c386-426d-ac7d-8c9a87a726a1" />


Installation

Clone the repository:
git clone https://github.com/yourusername/be-aware-be-safe.git
cd be-aware-be-safe

Install dependencies:
pip install -r requirements.txt

Dependencies include:
tkinter (built-in with Python)
Pillow
requests
tkintermapview

Run the application:
python main.py

Usage
Launch the application. The Dashboard will open.
Use the feature buttons to navigate:
Evacuation Area: View the interactive map.
Hotline: Access emergency contacts.
Disaster Info: Manage disaster records (CRUD).
Send Safe/Location: Automatically detect your location and send a safe message.
Use the side navigation menu for additional options (Home, Profile, Services, About Us, Survey/Feedback).ps.Completely cosmetic because of time

Database
The app uses a SQLite database (Disaster_info.db) to store disaster information.

Table: Disaster_info
| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER PRIMARY KEY | Unique record ID |
| Disaster_type | TEXT | Type of disaster (e.g., Flood, Earthquake) |
| Name | TEXT | Name of the disaster |
| Date | TEXT | Date of occurrence |
| Location | TEXT | Location of landfall |
| Overview | TEXT | Brief description of disaster |
| Safety_Tips | TEXT | Safety guidelines |

The database is automatically created when the app runs for the first time.

Dependencies
Make sure you have Python 3.8+ installed. Install the required libraries using pip:
pip install Pillow requests tkintermapview
tkinter – GUI framework
Pillow – Image handling
requests – HTTP requests for location detection
tkintermapview – Interactive maps

