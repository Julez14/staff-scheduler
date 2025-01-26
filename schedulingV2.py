import csv
from collections import defaultdict

def can_cover_appointment(staff_available_hours, appointment):
    """
    Checks if any of the staff's availability intervals
    can fully cover the entire appointment interval.
    """
    appointment_start, appointment_end = appointment
    for (staff_start, staff_end) in staff_available_hours:
        if staff_start <= appointment_start and staff_end >= appointment_end:
            return True
    return False

def intervals_overlap(interval1, interval2):
    """
    Returns True if two intervals (s1, e1) and (s2, e2) overlap.
    Intervals overlap if s1 < e2 and e1 > s2.
    """
    s1, e1 = interval1
    s2, e2 = interval2
    
    return s1 < e2 and e1 > s2

def can_assign_appointment(staff_name, appointment, staff_assigned_intervals):
    """
    Check if the given appointment overlaps with any of the existing
    appointments for this staff member.
    Returns True if NO overlap (i.e., can assign),
    or False if it overlaps with an existing appointment.
    """
    for existing_interval in staff_assigned_intervals[staff_name]:
        if intervals_overlap(existing_interval, appointment):
            # Found an overlap -> cannot assign
            return False
    return True

def match_staff_to_clients(staff_list, clients):
    """
    Returns a dictionary mapping:
      {
        client_name: {
          (appointment_start, appointment_end): staff_member_name (or None)
        }
      }
    and ensures no staff member is assigned to overlapping appointments.
    """
    schedule = {}
    # Track assigned intervals for each staff member
    staff_assigned_intervals = defaultdict(list)

    for client in clients:
        client_name = client["name"]
        appointment_times = client["appointment_times"]
        schedule[client_name] = {}

        for appointment in appointment_times:
            assigned_staff = None

            for staff in staff_list:
                if not staff["available"]:
                    continue  # Skip staff not available at all

                # Skip if staff is not allowed to work with this client
                if client_name not in staff["allowed_clients"]:
                    continue

                # Check if the staff's available hours cover the appointment
                if not can_cover_appointment(staff["available_hours"], appointment):
                    continue

                # Check if staff has no overlap with existing assigned intervals
                if can_assign_appointment(staff["name"], appointment, staff_assigned_intervals):
                    assigned_staff = staff["name"]
                    # Record this interval as assigned to the staff
                    staff_assigned_intervals[assigned_staff].append(appointment)
                    break

            schedule[client_name][appointment] = assigned_staff

    return schedule

def fractional_hour_to_hhmm(fractional_hour):
    """
    Convert a fractional hour (e.g. 9.5, 10.25) into HH:MM format.
      9.5    -> "09:30"
      10.25  -> "10:15"
      9.75   -> "09:45"
    """
    hour = int(fractional_hour)                     # e.g. 9 from 9.5
    minute = int(round((fractional_hour - hour) * 60))
    return f"{hour:02d}:{minute:02d}"

def write_schedule_to_csv(schedule, output_csv_path, appointment_date="2025-02-01"):
    """
    Writes the schedule dictionary to a CSV file in a format
    that can be imported into Google Calendar.
    
    - schedule: {
        client_name: {
          (start_hour, end_hour): staff_member_name (or None)
        }
      }
    - output_csv_path: path to the CSV file to write
    - appointment_date: string representing the date of the appointments 
                       (e.g., "2025-01-31" in yyyy-mm-dd format)
    """
    # Define column headers based on Google Calendar’s CSV requirements
    # (These can vary, but here's a commonly accepted format)
    fieldnames = [
        "Subject",
        "Start Date",
        "Start Time",
        "End Date",
        "End Time",
        "All Day Event",
        "Description",
        "Location"
    ]

    with open(output_csv_path, mode="w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()

        # Convert each appointment in the schedule to a row in the CSV
        for client_name, appts in schedule.items():
            for (start_hour, end_hour), staff_name in appts.items():
                if staff_name is None:
                    # We can decide how to handle unassigned appointments
                    staff_name = "No Staff Assigned"

                # Build a row
                subject = f"{client_name} with {staff_name}"  # Event title
                start_time = fractional_hour_to_hhmm(start_hour)
                end_time = fractional_hour_to_hhmm(end_hour)
                description = f"Care appointment for {client_name} handled by {staff_name}"
                location = "Senior Care Facility"  # Or wherever relevant

                row = {
                    "Subject": subject,
                    "Start Date": appointment_date,
                    "Start Time": start_time,
                    "End Date": appointment_date,
                    "End Time": end_time,
                    "All Day Event": False,
                    "Description": description,
                    "Location": location
                }
                writer.writerow(row)

if __name__ == "__main__": # means to only execute when the program is run, not when it's imported as a module
    staff_list = [
        {
            "name": "Alison",
            "available": True,
            "available_hours": [(10, 13)],
            "allowed_clients": ["Jim", "Roy", "Peter", "Velma", "Karen", "Bryce", "Edna", "Helen", "Jean", "Cliff", "Jean2"]
        },
        {
            "name": "Cheyenne",
            "available": True,
            "available_hours": [(9, 17)],
            "allowed_clients": ["Jim", "Roy", "Peter", "Velma", "Karen", "Bryce", "Edna", "Helen", "Jean", "Cliff", "Jean2"]    
        },
        {
            "name": "Chrissie",
            "available": True,
            "available_hours": [(0, 24)],
            "allowed_clients": ["Jim", "Roy", "Peter", "Velma", "Karen", "Bryce", "Edna", "Helen", "Jean", "Cliff", "Jean2"]
        },
        {
            "name": "Dawn",
            "available": True,
            "available_hours": [(0, 24)],
            "allowed_clients": ["Jim", "Roy", "Peter", "Velma", "Karen", "Bryce", "Edna", "Helen", "Jean", "Cliff", "Jean2"]
        },
        {
            "name": "Genet",
            "available": True,
            "available_hours": [(0, 24)],
            "allowed_clients": ["Jim", "Roy", "Peter", "Velma", "Karen", "Bryce", "Edna", "Helen", "Jean", "Cliff", "Jean2"]
        },
        {
            "name": "Jennifer",
            "available": True,
            "available_hours": [(8, 14)],
            "allowed_clients": ["Jim", "Roy", "Peter", "Velma", "Karen", "Bryce", "Edna", "Helen", "Jean", "Cliff", "Jean2"]
        },
        {
            "name": "Karen",
            "available": True,
            "available_hours": [(20, 24)],
            "allowed_clients": ["Jim", "Roy", "Peter", "Velma", "Karen", "Bryce", "Edna", "Helen", "Jean", "Cliff", "Jean2"]
        },
        {
            "name": "Marlene",
            "available": True,
            "available_hours": [(9.5, 18)],
            "allowed_clients": ["Jim", "Roy", "Peter", "Velma", "Karen", "Bryce", "Edna", "Helen", "Jean", "Cliff", "Jean2"]
        },
        {
            "name": "Miriam",
            "available": True,
            "available_hours": [(9, 12)],
            "allowed_clients": ["Jim", "Roy", "Peter", "Velma", "Karen", "Bryce", "Edna", "Helen", "Jean", "Cliff", "Jean2"]
        },
        {
            "name": "Sandy",
            "available": True,
            "available_hours": [(0, 24)],
            "allowed_clients": ["Jim", "Roy", "Peter", "Velma", "Karen", "Bryce", "Edna", "Helen", "Jean", "Cliff", "Jean2"]
        },
        {
            "name": "Tara",
            "available": True,
            "available_hours": [(7, 14)],
            "allowed_clients": ["Jim", "Roy", "Peter", "Velma", "Karen", "Bryce", "Edna", "Helen", "Jean", "Cliff", "Jean2"]
        },
        {
            "name": "Teresa",
            "available": True,
            "available_hours": [(0, 24)],
            "allowed_clients": ["Jim", "Roy", "Peter", "Velma", "Karen", "Bryce", "Edna", "Helen", "Jean", "Cliff", "Jean2"]
        },
        {
            "name": "Darla",
            "available": True,
            "available_hours": [(6, 15)],
            "allowed_clients": ["Jim", "Roy", "Peter", "Velma", "Karen", "Bryce", "Edna", "Helen", "Jean", "Cliff", "Jean2"]
        },
    ]

    clients = [
        {
            "name": "Jim",
            "appointment_times": [(14.5, 17)]
        },
        {
            "name": "Roy",
            "appointment_times": [(11, 13)]
        },
        {
            "name": "Peter",
            "appointment_times": [(9, 17)]
        },
        {
            "name": "Velma",
            "appointment_times": [(14, 16)]
        },
        {
            "name": "Karen",
            "appointment_times": [(9, 12), (17.5, 20.5)]
        },
        {
            "name": "Bryce",
            "appointment_times": [(8.5, 10), (13.5, 15), (19, 20)]
        },
        {
            "name": "Edna",
            "appointment_times": [(8, 12.5), (17.5, 19.5)]
        },
        {
            "name": "Helen",
            "appointment_times": [(10, 13), (20.25, 21.25)]
        },
        {
            "name": "Jean",
            "appointment_times": [(12.75, 14.75)]
        },
        {
            "name": "Cliff",
            "appointment_times": [(10, 12), (15, 17)]
        },
        {
            "name": "Jean2",
            "appointment_times": [(8.75, 9.75), (17, 18)]
        },
    ]

    # Generate the schedule
    schedule = match_staff_to_clients(staff_list, clients)

    # Print it out in a human-readable way
    for client_name, appts in schedule.items():
        print(f"\nClient: {client_name}")
        for times, staff in appts.items():
            start, end = times
            staff_str = staff if staff else "No staff available"
            print(f"  Appointment {start}-{end} -> {staff_str}")

    # Write schedule to a CSV file for Google Calendar
    output_csv = "senior_care_schedule.csv"
    write_schedule_to_csv(schedule, output_csv_path=output_csv, appointment_date="2025-02-01")
    print(f"\nCSV schedule written to {output_csv}")