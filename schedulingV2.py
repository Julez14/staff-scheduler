def can_cover_appointment(staff_available_hours, appointment):
    """
    Checks if any of the staff's availability intervals 
    can cover the entire appointment interval.
    """
    appointment_start, appointment_end = appointment
    for (staff_start, staff_end) in staff_available_hours:
        if staff_start <= appointment_start and staff_end >= appointment_end:
            return True
    return False

def match_staff_to_clients(staff_list, clients):
    """
    Returns a dictionary mapping:
      { 
        client_name: {
          (appointment_start, appointment_end): staff_member_name (or None)
        } 
      }
    """
    schedule = {}

    for client in clients:
        client_name = client["name"]
        appointment_times = client["appointment_times"]
        schedule[client_name] = {}

        for appointment in appointment_times:
            assigned_staff = None

            for staff in staff_list:
                if not staff["available"]:
                    continue  # Skip staff not available at all

                if client_name not in staff["allowed_clients"]:
                    continue  # Skip staff not allowed for this client

                if can_cover_appointment(staff["available_hours"], appointment):
                    assigned_staff = staff["name"]
                    break  # Found a match, break out of staff loop

            schedule[client_name][appointment] = assigned_staff

    return schedule

if __name__ == "__main__": # means to only execute when the program is run, not when it's imported as a module
    staff_list = [
        {
            "name": "Alice",
            "available": True,
            "available_hours": [(9, 12), (14, 18)],
            "allowed_clients": ["Bob", "Diana"]
        },
        {
            "name": "Charlie",
            "available": True,
            "available_hours": [(8, 11), (13, 17)],
            "allowed_clients": ["Bob"]    
        },
        {
            "name": "Eve",
            "available": False,
            "available_hours": [],
            "allowed_clients": ["Diana"]
        }
    ]

    clients = [
        {
            "name": "Bob",
            "appointment_times": [(9, 10), (15, 16)]
        },
        {
            "name": "Diana",
            "appointment_times": [(10, 11), (16, 17)]
        }
    ]

    # Generate the schedule
    schedule = match_staff_to_clients(staff_list, clients)

    # Print it out in a human-readable way
    for client_name, appts in schedule.items():
        print(f"\nClient: {client_name}")
        for times, staff in appts.items():
            start, end = times
            print(f"  Appointment {start}-{end} -> {staff if staff else 'No staff available'}")
