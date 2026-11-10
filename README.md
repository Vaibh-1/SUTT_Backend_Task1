do this before pushing to github 
git add README.md
git commit -m "Add README with project documentation and complexity analysis"

# Cab Pool Matcher

A command-line app in Python for the end-of-semester cab rush. This is my submission for SUTT Backend Task 1.

## 1. Project Overview

Students want cabs to Delhi or Jaipur at the same few times, and seats are limited. This app collects ride requests, keeps them waiting in a queue, and lets one person (the person running the app) preview matches and send cabs off. When there are more students than seats, seniors get in first (5th year, then 4th, ... then 1st). If two students are in the same year, whoever asked first gets the seat. There are no logins or separate student/admin modes.

## 2. Features

- Add a ride request (name, destination, time slot, year). The time of the request is stored.
- View everyone who is still waiting, plus all cabs (open and already left).
- Find Matches: a preview of who would get a seat in each open cab. It changes nothing.
- Dispatch Cab: fills one open cab for a trip with the most senior waiting students and marks it as left.
- One `heapq` priority queue for every destination + time slot combination.
- Cabs are loaded from `cabs.json`.
- Everything is saved to `state.json` after every change and loaded again on the next start.

## 3. Technologies and Requirements

Only Python and its standard library: `json`, `datetime`, `heapq` and `pathlib`. No external packages, so there is no `requirements.txt`. It needs Python 3.7 or newer because I use `datetime.fromisoformat`.

## 4. Project Structure

| File | Purpose |
|---|---|
| `main.py` | The whole app: `Cab` and `RideRequest` classes, matching and dispatch, saving and loading, and the menu. |
| `cabs.json` | The initial list of cabs (24 in the sample, three for every destination/time slot). |
| `state.json` | Created automatically while the app runs. Stores the waiting students and the cabs. Don't edit it by hand. |
| `README.md` | This file. |
## 5. Installation and Running

```bash
git clone https://github.com/Vaibh-1/SUTT_Backend_Task1.git
cd SUTT_Backend_Task1
python main.py
```


(Use `python3` if `python` doesn't work on your system.) No packages need to be installed. Run it from inside the project folder, because `cabs.json` and `state.json` are opened by relative path.

I have not given state.json in the repo and added it to .gitignore because it is not required and will be formed by the user when running the code automatically with the correct data

## 6. Cab Input File Format

`cabs.json` is a list of cabs. Example (taken from the sample file):

```json
[
  {
    "name": "Amit Sharma",
    "seats": 4,
    "headed_to": "delhi",
    "time_slot": "morning"
  },
  {
    "name": "Rohit Meena",
    "seats": 3,
    "headed_to": "delhi",
    "time_slot": "morning"
  }
]
```

| Field | Meaning | Valid values |
|---|---|---|
| `name` | Driver's name | Any text |
| `seats` | Number of seats | Whole number from 1 to 4 |
| `headed_to` | Destination | `delhi` or `jaipur` |
| `time_slot` | When it leaves | `morning`, `afternoon`, `evening` or `night` |

The order in the file is the order cabs are shown and picked. `headed_to` and `time_slot` are trimmed and lowercased when loaded. The code does not check that the values are valid (see Limitations), so please stick to the table above. `cabs.json` is only read when there is no usable `state.json`.

## 7. How to Use the Application

The menu is printed before every choice:

| Option | What it does |
|---|---|
| 1 | Add a new ride request. Asks for name, destination, time and year. |
| 2 | Show everyone still waiting, then all cabs with seats taken (like `2 / 4`) and whether they have left. |
| 3 | Find Matches: preview for each open cab. Nothing is changed. |
| 4 | Dispatch Cab: asks for a destination and a time slot, then sends off one open cab for that trip. |
| 5 | Close the app. |

Sample session (menu text is omitted, and `[...]` indicates shortened output):

```text
No previous state found. Starting fresh...
Initial cabs loaded successfully.

Choose an option: 1
Enter name:Ishita
Enter where to:jaipur
Enter time of travelling:night
Enter year of college:1

[... Rahul (Year 5) and Neha (Year 3) also request Jaipur/night ...]

Choose an option: 4
[... Other cabs omitted ...]
Driver name: Ramesh Yadav
No of seats: 2
headed to: jaipur
Status cab left? False
Time slot: night
Tentative Passengers:
Potential Seats filled:2/2
Requesters name: Rahul
Current academic year: 5
Requesters name: Neha
Current academic year: 3
[... Other passenger details omitted ...]

Choose an option: 5
Enter the destination of cab to be dispatched:jaipur
Enter the time:night
Seats filled:2/2
[... Rahul and Neha assigned to the cab ...]
Status cab left? True
Occupied seats: 2 / 2

Choose an option: 3
```

Rahul and Neha get the two available seats because of their higher academic years. Ishita remains in the waiting queue.

After restarting the application:

```text
Previous session restored successfully.

Choose an option: 2
Requesters name: Ishita
Going to: jaipur
Current academic year: 1
[...]
Driver name: Ramesh Yadav
Status cab left? True
Occupied seats: 2 / 2
[...]
```

The waiting request and dispatched cab are both restored from `state.json`.

## 8. Matching and Dispatch Algorithm

**Grouping.** `waiting_queues` is a dictionary. The key is `(destination, time_slot)` and the value is a heap (a normal Python list used with `heapq`) for that trip. A cab only looks at the queue for its own `headed_to` and `time_slot`. The queue belongs to the trip, not to a particular cab.

**Queue entries.** Each entry is a tuple:

```python
(-year, request_time, count, request)
```

- `-year`: `heapq` is a min-heap, so I store the year as a negative number. A 5th year (-5) comes before a 1st year (-1).
- `request_time`: for the same year, the earlier request is smaller, so it comes first.
- `count`: a counter that goes up by one for every new request. If year and time are both equal, Python would go on to compare the `RideRequest` objects and crash. The counter is always different, so that never happens.
- `request`: the `RideRequest` object itself.

A new request is added with `heapq.heappush()` on its trip's heap (and also appended to the `waiting_request` list, which is used for the "view waiting" screen).

**Find Matches (preview).** For every open cab, in the order they appear in the file, it calls `heapq.nsmallest(cab.seats, queue)`. This returns the best `seats` entries as a new list and leaves the heap as it is, so nobody is removed or given a seat.

**Dispatch.** It finds the first open cab (in file order) with the given destination and time. Then it calls `heapq.heappop()` on the trip's queue until the cab is full or the queue is empty. Each popped student is also removed from `waiting_request` and added to the cab's `students_list`. Then the cab is marked as left and the state is saved. Only one cab is sent per dispatch.

**Capacity and departed cabs.** The pop loop stops at `cab.seats`, so a cab can't get more students than seats. Both Find Matches and Dispatch skip cabs that have already left, so a departed cab never gets more students.

**Preview vs dispatch.** Find Matches only looks, Dispatch actually removes students and sends the cab. Both use the same queue ordering, so if nothing changes in between, Dispatch takes the same students (in the same order) that the preview showed for that cab.

## 9. Data Persistence

I used a JSON file (`state.json`) instead of `pickle` because JSON can be opened and read in any text editor, and loading it can't run code like loading a pickle file can. It's just a file, there's no database.

**What is saved:** the waiting requests (name, destination, time slot, year, request time), every cab (name, seats, left or not, destination, time slot, and its passengers with the same details), and the request counter.

**When:** after every added request and after every successful dispatch. Viewing and Find Matches don't change anything, so they don't save. Quitting doesn't need an extra save because everything is already saved. If nothing has been added or dispatched, `state.json` is not created.

**Loading.** On start, if `state.json` exists, the app rebuilds `RideRequest` and `Cab` objects from it (`request_time` is saved as an ISO string and converted back with `datetime.fromisoformat`). The heaps are not saved. They are rebuilt by pushing each waiting request again with `(-year, request_time, index, request)`, where `index` is its position in the saved list. That list is in the order requests arrived, and the original request times are kept, so everyone keeps their place in line. The request counter is restored too, so new requests always come after old ones. When a save is loaded, the cabs come from `state.json`, not from `cabs.json`.

**Missing or broken file.** If there is no `state.json`, it prints `No previous state found starting fresh...` and loads `cabs.json`. If it exists but is broken (not valid JSON, missing keys, wrong types, bad dates), it prints `Saved state is invalid: ...`, throws away whatever it had partly loaded, and starts fresh from `cabs.json`. The broken file stays on disk until the next save overwrites it.

**Reset.** Delete `state.json` and start the app again.

## 10. Edge Cases and Input Validation

**Handled**

| Case | What happens |
|---|---|
| Destination not delhi/jaipur, or time slot that doesn't exist | `Invalid Input try again`, asks again. Capital letters and extra spaces are ignored. |
| Year that isn't a number, or isn't 1 to 5 (like 7) | `Try again...`, asks again. |
| Empty name | `Enter valid name`, asks again. |
| Wrong menu choice | `Invalid input` |
| Nobody waiting | Option 2 prints `No students are currently waiting...`. Find Matches prints `There are no matches for this cab...` for that cab. Dispatch prints the same message and changes nothing (the cab stays open). |
| No open cab for the trip | Dispatch prints `no cabs are available at this time for this location please try again later...`. Waiting students stay in the queue. |
| Cab not full | It leaves with whoever is waiting, up to its seats. |
| Cab already dispatched | It is skipped. The next open cab for that trip is used, or the "no cabs" message is shown. |
| Restart | Saved state is restored (section 9). |
| `state.json` missing or broken | Message, then a fresh start (section 9). |
| `cabs.json` missing, not valid JSON, missing fields, or wrong structure | `Could not load initial cabs error in cabs.json: ...` and the app keeps running with no cabs. |

**Not handled**

- The values inside `cabs.json` are not checked. Seats like 0, -1 or 5, or a city/time that doesn't exist, load without any error. Seats written as text (`"4"`) make Find Matches crash.
- A hand-edited `state.json` is only checked for structure, not for sensible values.
- The destination and time typed for Dispatch aren't validated. A typo just gives the "no cabs are available" message.
- Ctrl+C or Ctrl+D shows a Python traceback (the data is still safe because it is saved after every change).

**Tricky situations from the assignment**

1. **Half-empty cab:** Dispatch takes whoever is waiting, up to the seats. If only 1 or 2 are waiting, the cab leaves with 1 or 2 and is marked as left, and nobody else can be added after that. If nobody is waiting, the cab doesn't leave.
2. **No cabs left:** new requests are still accepted. They stay in the queue and in the waiting list, and Dispatch shows the "no cabs are available" message. They never get removed. The message only shows up when dispatching, not when adding a request.
3. **Same year:** the heap compares `request_time` after the year, so whoever asked first wins. The counter in the tuple handles an exact tie. Request times are saved, so this also holds after a restart.
4. **Lots of students:** see section 11.

## 11. Time and Space Complexity

- **N** = total waiting requests (all trips)
- **M** = requests in one trip's queue (M ≤ N)
- **C** = number of cabs
- **K** = students picked for one cab (at most the seats, so K ≤ 4)
- **P** = students already sitting in departed cabs

Because of autosave, the real cost of adding or dispatching is higher than the heap cost alone:

| Operation | Heap part only | Whole operation, as coded | Why |
|---|---|---|---|
| Add one request | `heappush` O(log M) | **O(N + C + P)** | After every add, `save_state` goes through all waiting requests, cabs and passengers and rewrites the file. |
| Add all 1,000 | O(N log N) | **O(N²)** | Each add saves everything, so it's about 1 + 2 + ... + 1000 request records written in total (roughly half a million). |
| Find Matches | `nsmallest` O(M log K) per cab | **O(C · M)** | It runs for each open cab. `nsmallest` goes through the whole queue, not just the top few. With K ≤ 4 that's about O(M) per cab. |
| Find an open cab for a trip | none | **O(C)** | A simple loop over the cabs list. |
| Dispatch one cab (up to 4) | K pops, O(K log M) | **O(N + C + P)** | Finding the cab is O(C). Each of the K students is also removed from `waiting_request` with `list.remove`, which is O(N) each, so O(K · N). Then it saves the whole state, O(N + C + P). With K ≤ 4 the whole thing is linear. |
| View (option 2) | none | O(N + C) | Prints the waiting list and all cabs. |
| Load at startup | N pushes, O(N log M) | O(N log M + C + P) | Reads the file, creates the objects, and pushes every waiting request back into its heap. |
| Save | none | O(N + C + P) | Builds the dictionaries and writes them with `json.dump`. |
| Space | O(N) | O(N + C + P) | The waiting list and the heaps both hold the same `RideRequest` objects (no copies), plus the cabs and their passengers. `state.json` is about the same size. |

**With about 1,000 requests:**

- *Adding one request:* O(N + C + P), because of the autosave (the heap push itself is only O(log M)). *Adding all 1,000:* O(N²) in total. N is only 1,000, so it still works, but this is the slowest part of the app.
- *Sending off one cab (up to 4 students):* O(N + C + P). The heap pops are cheap, but the list removals and the save are not.
- *Finding an open cab for a trip:* O(C). The sample file only has 24 cabs.

Without autosave, adding would be O(log M) and dispatching would be O(C + N).

## 12. Limitations

- Autosave rewrites the whole `state.json` after every change, so the cost grows with the number of requests (section 11).
- `waiting_request` is a plain list, so removing a dispatched student from it is O(N).
- Once `state.json` exists, the cabs come from it and `cabs.json` is ignored. If `state.json` was saved while `cabs.json` was missing (so it has no cabs), fixing `cabs.json` won't help until `state.json` is deleted.
- No validation of the values inside `cabs.json` or `state.json` (section 10).
