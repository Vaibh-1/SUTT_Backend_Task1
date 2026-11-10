import json
from datetime import datetime
import heapq
from pathlib import Path


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


#Accpeted inputs for RideRequest
times_accepted = ["morning","evening","afternoon","night"]
locations_accepted = ["delhi","jaipur"]
max_year = 5
waiting_request = []
cabs_available = []


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


#Find matches (Final)
def find_matches(cabs_available):
    for cabs in cabs_available:
        if cabs.status == False:
            temporary_passengers = []
            queue = waiting_queues.get((cabs.headed_to, cabs.time_slot), [])
            selected = heapq.nsmallest(cabs.seats, queue)
            for requests in selected:
                temporary_passengers.append(requests[3])    
            cabs.display()  
            if len(temporary_passengers) == 0:
                print("There are no matches for this cab...") 
                continue
            print("Tentative Passengers:")    
            print(f"Potential Seats filled:{len(temporary_passengers)}/{cabs.seats}")         
            for passengers in temporary_passengers:
                passengers.display()
            

#Final Dispatches considering seniority 
def dipatch_cabs(cab_destination,cab_time,cabs_available):
    for cabs in cabs_available:
            if cabs.status == False and cabs.time_slot == cab_time and cabs.headed_to == cab_destination:
                passengers = []
                queue = waiting_queues.get((cabs.headed_to, cabs.time_slot), [])
                while(len(passengers)<cabs.seats and len(queue)!=0):
                    selected = heapq.heappop(queue)
                    passengers.append(selected[3])
                    waiting_request.remove(selected[3])   
                cabs.students_list = passengers.copy()      
                if len(cabs.students_list) == 0:
                    print("There are no matches for this cab...") 
                    return 0
                print(f"Seats filled:{len(passengers)}/{cabs.seats}")
                print("Details of all the passengers of the cab")    
                for passenger in passengers:
                    passenger.display()
                cabs.status = True 
                cabs.display()            
                print("Final Passengers are above mentioned:")
                save_state(waiting_request, cabs_available, count) #Auto save after Dispacth
                return 0
    print("no cabs are available at this time for this location please try again later...")
    return 0
                
                    
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


#Functions to load and save app data
def save_state(waiting_request,cabs_available,count):
    requests = []
    for request in waiting_request:
        requests.append({
            "time_slot" : request.time_slot,
            "name" : request.name,
            "year" : request.year,
            "request_time" : request.request_time.isoformat(),
            "destination" : request.destination
            })
    cabs_save = []
    for cabs in cabs_available:
        passengers = []
        for passenger in cabs.students_list:
            passengers.append({
                "time_slot" : passenger.time_slot,
                "name" : passenger.name,
                "year" : passenger.year,
                "request_time" : passenger.request_time.isoformat(),
                "destination" : passenger.destination
             })
        cabs_save.append({
            "name": cabs.name,
            "seats": cabs.seats,
            "status": cabs.status,
            "headed_to": cabs.headed_to,
            "time_slot": cabs.time_slot,
            "students_list": passengers
        })
    state = {
        "waiting_requests": requests,
        "cabs": cabs_save,
        "count_of_requests": count 
    }
    with open("state.json", "w") as file:
        json.dump(state, file, indent=4)    


def load_data(waiting_request,cabs_available,waiting_queues):
    with open("state.json", "r") as file:
        state = json.load(file)
    saved_requests = state["waiting_requests"]
    saved_cabs = state["cabs"]
    for data in saved_requests:
        request_time = datetime.fromisoformat(data["request_time"])
        name = data["name"]
        year = data["year"]
        time_slot = data["time_slot"]
        destination = data["destination"]
        request = RideRequest(name,destination,time_slot,year,request_time)
        waiting_request.append(request)      
    for index, request in enumerate(waiting_request):
        key = (request.destination, request.time_slot)

        heapq.heappush(
            waiting_queues.setdefault(key, []),
            (-request.year, request.request_time, index, request)
        )
    for cabs in saved_cabs:
        passengers = []
        for passenger_info in cabs["students_list"]:
            passenger = RideRequest(passenger_info["name"],passenger_info["destination"],passenger_info["time_slot"],passenger_info["year"],datetime.fromisoformat(passenger_info["request_time"]))
            passengers.append(passenger)
        cab = Cab(cabs["name"],cabs["seats"],cabs["status"],cabs["headed_to"],passengers,cabs["time_slot"])      
        cabs_available.append(cab)  
    return max(
        len(waiting_request),
        state.get("count_of_requests", 0)
    )  



#inputting cabs from json or previous save file and creating them into objects
waiting_queues = {}
count = 0 
fresh_start = True


if Path("state.json").is_file():
    try:
        count = load_data(waiting_request, cabs_available, waiting_queues)
        print("Previous session restored successfully.")
        fresh_start = False

    except (json.JSONDecodeError, KeyError, TypeError, ValueError, OSError) as error:  #informing user about error
        print("Saved state is invalid:", error)
        print("Starting fresh using cabs.json...")

        waiting_request.clear()
        waiting_queues.clear()
        cabs_available.clear()
        count = 0
else:
    print("No previous state found starting fresh...")

# Load original cabs if saved data is unavailable
if fresh_start:
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

        print("Initial cabs loaded successfully.")

    except (FileNotFoundError, json.JSONDecodeError, KeyError, TypeError, AttributeError) as error:
        cabs_available.clear()
        print("Could not load initial cabs error in cabs.json:", error)

#App menu and logic
while True:
    print("===CAB_FINDER===")
    print("1.to add new request")
    print("2.to view waiting students and available cabs")
    print("3.to find mathces")
    print("4.to dispatch cabs")
    print("5.to close app")
    choice = input("Choose an option: ")


    if choice == "1":
        #input the correct info  
        name = get_correct_name()
        location = get_correct_input("where to",locations_accepted)
        time = get_correct_input("time of travelling",times_accepted)
        year = get_correct_year(max_year)
        request_time = datetime.now()   
        request = RideRequest(name,location,time,year,request_time)  
        waiting_request.append(request)
        heapq.heappush(waiting_queues.setdefault((location,time), []), (-(request.year),request.request_time,count,request))
        count+=1
        save_state(waiting_request,cabs_available,count) #Auto Saving


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
        find_matches(cabs_available)


    elif choice == "4":
        cab_destination = input("Enter the destination of cab to be dispatched:").strip().lower()
        cab_time = input("Enter the time:").strip().lower()
        dipatch_cabs(cab_destination,cab_time,cabs_available)  


    elif choice == "5" :
        break

    
    else:
        print("Invalid input")        
        
