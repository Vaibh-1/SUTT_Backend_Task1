import json
from datetime import datetime


class Cab:
    def __init__(self, name, seats, status, headed_to, students_list, time_slot):
        self.name = name
        self.seats = seats
        self.status = status
        self.headed_to = headed_to
        self.students_list = students_list
        self.time_slot = time_slot
    def display(self):
        print("Driver name: ",self.name)
        print("No of seats: ",self.seats)
        print("headed to:",self.headed_to)
        print("Status cab left?",self.status)
        print("Time slot: ",self.time_slot)
        print("Occupied seats: ",len(self.students_list),"/",self.seats)

class RideRequest:
    def __init__(self, name, destination, time_slot, year, request_time):
        self.name = name
        self.destination = destination
        self.time_slot = time_slot
        self.year = year
        self.request_time = request_time

    def display(self):
        print("Requesters name:",self.name)
        print("Going to:",self.destination)
        print("Time of going",self.time_slot)
        print("Current academic year:",self.year)
        print("Time of request:",self.request_time)

#Find matches 
def find_matches(cabs_available,waiting_request):
    for cabs in cabs_available:
        if cabs.status == False:
            temporary_passengers = []
            for requests in waiting_request:
                if requests.time_slot == cabs.time_slot and requests.destination == cabs.headed_to:
                    if cabs.seats > len(temporary_passengers):
                        temporary_passengers.append(requests)
            cabs.display()            
            print("Tentative Passengers:")    
            print(f"Potential Seats filled:{len(temporary_passengers)}/{cabs.seats}")         
            for passengers in temporary_passengers:
                passengers.display()
            if len(temporary_passengers) == 0:
                print("There are no matches for this cab...")

#Functions to get inputs        
def get_correct_input(prompt,accepted_values):
    while True:
        value = input(f"Enter {prompt}:").strip().lower()
        if value in accepted_values:
            return value
        else:
            print("Invalid Input try again")
def get_correct_year(max_year):
    while True:
        try:
            year = int(input("Enter year of college:"))
        except ValueError:
            print("Try again...")  
            continue  
        if 1 <=year<= max_year:
            return year
        else:
            print("Try again...")
def get_correct_name():
    while True:
        name = input("Enter name:").strip()
        if name:
            return name
        else:
            print("Enter valid name")   
#Accpeted inputs for RideRequest
times_accepted = ["morning","evening","afternoon","night"]
locations_accepted = ["delhi","jaipur"]
max_year = 5
waiting_request = []
cabs_available = []
#inputting cabs from json and creating them into objects

try:
    with open("cabs.json", "r") as file:
        cab_data = json.load(file)

    for cab in cab_data:
        new_cab = Cab(
            cab["name"],
            cab["seats"],
            False,
            cab["headed_to"].strip().lower(),
            [],
            cab["time_slot"].strip().lower()
        )
        cabs_available.append(new_cab)

except (FileNotFoundError, json.JSONDecodeError) as error:
    print("Could not load cabs:", error)


#App menu and logic
while True:
    print("===CAB_FINDER===")
    print("1.to add new request")
    print("2.to view waiting students and available cabs")
    print("3.to close app")
    print("4.to find mathces")
    choice = input("Choose an option: ")
    if choice == "1":
        #input the correct info       
        waiting_request.append(RideRequest(get_correct_name(), get_correct_input("where to ",locations_accepted), get_correct_input("time of travelling",times_accepted), get_correct_year(max_year), datetime.now()))
    elif choice == "2" :
        #printing waiting students
        if len(waiting_request) == 0:
            print("No students are currently waiting...")
        for i in range(0,len(waiting_request)):
            waiting_request[i].display()
        #printing available cabs
        for i in range(0,len(cabs_available)):
            cabs_available[i].display()
    elif choice == "3" :
        break
    elif choice == "4" :
        find_matches(cabs_available,waiting_request)
    else:
        print("Invalid input")        