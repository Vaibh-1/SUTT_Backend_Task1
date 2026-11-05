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
        print("Empty seats: ",self.seats-len(self.students_list),"/",self.seats)

class RideRequest:
    def __init__(self, name, destination, time_slot, year):
        self.name = name
        self.destination = destination
        self.time_slot = time_slot
        self.year = year

    def display(self):
        print(self.name,self.destination,self.time_slot,self.year)
#Accpeted inputs for RideRequest
times_accepted = ["Morning","Evening","Afternoon","Night"]
locations_accepted = ["Delhi","Jaipur"]

waiting_request = []
cabs_available = []
#sample cabs test cases later to be changed by a csv or json file
list1 = []
list2 = []
cabs_available.append(Cab("Amit",3,False,"Jaipur",list1,"Morning"))
cabs_available.append(Cab("Rajesh",4,False,"Delhi",list2,"Evening"))
while True:
    print("===CAB_FINDER===")
    print("1.to add new request")
    print("2.to view waiting students and available cabs")
    print("3.to close app")
    choice = input("Choose an option: ")
    if choice == "1":
        #input the correct info
        while True:
            name = input("Enter name: ")
            destination = input("Enter destination:")
            if destination in locations_accepted:
                pass
            else:
                print("The destination is invlaid please try something else...")
                continue
            time = input("Enter time slot: ")
            if time in times_accepted:
                pass
            else:
                print("Time invalid Error try something else...")
                continue
            try:
                year = int(input("Enter year:"))
            except ValueError:
                print("Try again...")  
                continue  
            if 1 <=year<= 5:
                break
            else:
                print("Try again...")        
        waiting_request.append(RideRequest(name, destination, time, year))
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
    else:
        print("Invalid input")        