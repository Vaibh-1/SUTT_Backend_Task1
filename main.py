class Cab:
    def __init__(self, name, seats, status, headed_to, students_list, time_slot):
        self.name = name
        self.seats = seats
        self.status = status
        self.headed_to = headed_to
        self.students = students_list
        self.time_slot = time_slot

class RideRequest:
    def __init__(self, name, destination, time_slot, year):
        self.name = name
        self.destination = destination
        self.time_slot = time_slot
        self.year = year

    def display(self):
        print(self.name,self.destination,self.time_slot,self.year)


waiting_request = []

while True:
    print("===CAB_FINDER===")
    print("1.to add new request")
    print("2.to view waiting students and available cabs")
    print("3.to close app")
    choice = input("Choose an option: ")
    if choice == "1":
        print("Adding new request")
        waiting_request.append(RideRequest(input("Enter name: "), input("Enter destination: "), input("Enter time slot: "), input("Enter year: ")))
    elif choice == "2" :
        pass #print waiting students and available cabs
    elif choice == "3" :
        break
    else:
        print("Invalid input")