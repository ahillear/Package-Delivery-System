# Andrew Hilleary
# Student ID: 011315946
# Data Structures and Algorithms II - C950 Sub#1

import csv
from datetime import timedelta



#Loading the CSV files into AddressCSV and DistanceCSV
with open("CSVFiles/addressCSV.csv") as address_CSV:
    AddressCSV = list(csv.reader(address_CSV))

with open("CSVFiles/distanceCSV.csv") as distance_CSV:
    DistanceCSV = list(csv.reader(distance_CSV))


# Creating the hash table with chaining
class ChainedHashTable:
    def __init__(self, size):
        self.size = size
        self.table = []
        for i in range(size):
            self.table.append([])

    # Hash function to save time
    def _hash(self, key):
        return hash(key) % self.size

    # Insert into table
    def insert(self, key, package):
        bucket = self._hash(key)
        buck_list = self.table[bucket]
        for pair in buck_list:
            if pair[0] == key:
                pair[1] = package
                return
        buck_list.append((key, package))

    # Look_up function for specific keys
    def search(self, key):
        index = self._hash(key)
        buck_list = self.table[index]
        for pair in buck_list:
            if pair[0] == key:
                return pair[1]
        return None

    #remove function for table
    def remove(self, key):
        index = self._hash(key)
        buck_list = self.table[index]
        if key in buck_list:
            buck_list.remove(key)
    
    #used for debugging
    def printTable(self):
        print(self.table)
        return
    
# Creating the Package class
class Package:
    def __init__(self, ID, street, city, state, zip_code, deadline, weight, notes, status, departure_time, delivery_time):
        self.ID = ID
        self.street = street
        self.city = city
        self.state = state
        self.zip_code = zip_code
        self.deadline = deadline
        self.weight = weight
        self.notes = notes
        self.status = status
        self.departure_time = None
        self.delivery_time = None

    # Defining the return of a str
    def __str__(self):
        return f"ID: {self.ID}, {self.street}, {self.city}, {self.state}, {self.zip_code}, Deadline: {self.deadline}, Weight: {self.weight}, Status: {self.status}, Departure Time: {self.departure_time}, Delivery Time: {self.delivery_time}"
    
    # Updates the status of the package depending on loc, added logic for package 9 issue
    def statusUpdate(self, timeChange):
        if self.delivery_time == None:
            self.status = "At the hub"
        elif timeChange < self.departure_time:
            self.status = "At the hub"   
        elif timeChange < self.delivery_time:
            self.status = "En route"     
        else:
            self.status = "Delivered" 
        if self.ID == 9: 
            if timeChange > timedelta (hours=10, minutes= 20):
                self.street = "410 S State St"  
                self.zip = "84111"  
            else:
                self.street = "300 State St"
                self.zip = "84103"    

# Load package data from CSV file into the hash table
def loadPackageData(filename, package_hash):
    with open(filename) as packages:
        package_info = csv.reader(packages, delimiter=',')
        for package in package_info:
            packID = int(package[0])
            packStreet, packCity, packState, packZip = package[1:5]
            packDeadline, packWeight, packNotes = package[5:8]
            packStatus = "At the Hub"
            packDepartureTime = None
            packDeliveryTime = None

            # Create Package object
            new_pack = Package(packID, packStreet, packCity, packState, packZip, packDeadline, packWeight, packNotes, packStatus, packDepartureTime, packDeliveryTime)

            # Insert Package into the hash table
            package_hash.insert(packID, new_pack)

# Creating the truck class
class Truck:
    def __init__(self, speed, miles, current_location, depart_time, packages):
        self.speed = speed
        self.miles = miles
        self.current_location = current_location
        self.time = depart_time
        self.depart_time = depart_time
        self.packages = packages

    # Truck as str
    def __str__(self):
        return "%s,%s,%s,%s,%s,%s" % (self.speed, self.miles, self.current_location, self.time, self.depart_time, self.packages)
    
# Checks the CSV for an address
def find_address(address):
    for row in AddressCSV:
        if address in row[2]:
           return int(row[0])
        
# Checks the triangluar CSV for distance, if its '' it swaps and finds the other index
def find_distance(address1, address2):
    distance = DistanceCSV[address1][address2]
    if distance == '':
        distance = DistanceCSV[address2][address1]
    return float(distance)

# Creating and loading the hash table
Htable = ChainedHashTable(40)
loadPackageData('CSVFiles/packageCSV.csv', Htable)

# Algorithm to deliver all packages on a given truck
def deliver_packages(truck):
    print("Delivering packages for truck:", truck)
    
    # Initialize the list of packages using the hash table and the contents of the truck
    enroute_packages = []
    for package_id in truck.packages:
        package = Htable.search(package_id)
        if package:
            enroute_packages.append(package)
        else:
            print("Package not found for ID:", package_id)

    # Clears the contents of the truck showing packages that are delievered
    truck.packages.clear()

    # Execute while there are still packages to deliever
    while 0 < len(enroute_packages):
        # Initialize the distance of next package to inf to ensure there will be a shorter distance to find.
        next_address_distance = float('inf')
        next_package = None

        for package in enroute_packages:
            # Check if the package ID is in the specified list and if the current time is before 9:05
            if package.ID in [6, 25, 28, 32] and truck.time < timedelta(hours=9, minutes=5):
                continue  # Skip delivery for this package until after 9:05
                
            # Calculate the distance to the next package's address
            address_distance = find_distance(find_address(truck.current_location), find_address(package.street))
            
            # Update the next package and distance if the current package is closer
            if address_distance <= next_address_distance:
                next_address_distance = address_distance
                next_package = package

        # If there are no packages ready for delivery yet, wait for the time to pass
        if next_package is None:
            wait_time = timedelta(hours=9, minutes=5) - truck.time
            truck.time += wait_time
            continue

        # Perform delivery for the next package
        enroute_packages.remove(next_package)
        truck.packages.append(next_package.ID)    
        truck.miles += next_address_distance
        truck.current_location = next_package.street
        truck.time += timedelta(hours=next_address_distance / 18)
        next_package.delivery_time = truck.time
        next_package.departure_time = truck.depart_time


# Initialize Data for Trucks
truck1 = Truck(18, 0.0, "4001 South 700 East", timedelta(hours=8),[1,13,14,15,16,19,20,27,29,30,31,34,37,40])
# Ensure packages 3, 18, 36, 38 are on truck2
truck2 = Truck(18, 0.0, "4001 South 700 East", timedelta(hours=11),[2,3,4,5,9,18,26,28,32,35,36,38])
truck3 = Truck(18, 0.0, "4001 South 700 East", timedelta(hours=9, minutes=5),[6,7,8,10,11,12,17,21,22,23,24,25,33,39])

# Executing the fucntion to deliever
deliver_packages(truck1)
deliver_packages(truck3)

# Ensures the 3rd truck goes out after one of the 2 drivers gets back
truck2.depart_time = min(truck1.time, truck3.time)
deliver_packages(truck2)

# Display functions
def display_title():
    print("WGU Parcel Service")

def calculate_total_miles(trucks):
    total_miles = sum(truck.miles for truck in trucks)
    print("Total Miles:", total_miles)

def prompt_user_for_time():
    user_time = input("Enter a view time for package status. Format: HH:MM. ")
    return timedelta(hours=int(user_time.split(":")[0]), minutes=int(user_time.split(":")[1]))

def prompt_user_for_package_id():
    try:
        package_id = int(input("Enter Package ID or press enter for all packages: "))
        return [package_id]
    except ValueError:
        return range(1, 41)

def update_package_statuses(package_ids, time_change):
    for package_id in package_ids:
        package = Htable.search(package_id)
        if package:
            package.statusUpdate(time_change)
            print(str(package))
        else:
            print("Package not found for ID:", package_id)

# Title
display_title()

# Calculate total miles
calculate_total_miles([truck1, truck2, truck3])

# Using display functions to make loopup function for assignment
def look_up_packages():
    # Prompt user for time
    time_change = prompt_user_for_time()

    # Prompt user for package IDs
    package_ids = prompt_user_for_package_id()

    # Update package statuses with the time entered
    update_package_statuses(package_ids, time_change)
    
look_up_packages()
