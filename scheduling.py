from collections import defaultdict, deque

class Employee:
    def __init__(self, name, available=True, allowed_customers=None):
        self.name = name
        self.available = available
        self.allowed_customers = allowed_customers if allowed_customers else []
        self.assigned_customer = None

    def can_serve(self, customer):
        return customer in self.allowed_customers and self.assigned_customer == None

    def assign_customer(self, customer):
        if self.can_serve(customer):
            self.assigned_customer = customer
            return True
        return False

    def clear_assignment(self):
        self.assigned_customer = None

class EmployeeCustomerMatcher:
    def __init__(self):
        self.employees = []
        self.unmatched_customers = set()
        self.matches = {}

    def add_employee(self, employee):
        self.employees.append(employee)

    def _build_graph(self, customers):
        # Create a graph representation for the matching problem
        graph = defaultdict(list)
        
        # Add edges from source (0) to employees (1 to len(employees))
        for i, employee in enumerate(self.employees, 1):
            if employee.available:
                graph[0].append(i)
        
        # Add edges from employees to customers
        for i, employee in enumerate(self.employees, 1):
            if employee.available:
                for j, customer in enumerate(customers, len(self.employees) + 1):
                    if customer in employee.allowed_customers:
                        graph[i].append(j)
        
        return graph

    def _bfs(self, graph, source, sink, parent):
        # Returns true if there is a path from source to sink in residual graph
        visited = set()
        queue = deque([source])
        visited.add(source)
        parent[source] = -1
        
        while queue:
            u = queue.popleft()
            for v in graph[u]:
                if v not in visited:
                    queue.append(v)
                    visited.add(v)
                    parent[v] = u
                    
                    if v == sink:
                        return True
        return False

    def match_customers(self, customers):
        # Reset all assignments
        for employee in self.employees:
            employee.clear_assignment()
        
        self.unmatched_customers = set(customers)
        self.matches = {}

        # Build the graph
        graph = self._build_graph(customers)
        
        # Maximum flow algorithm (Ford-Fulkerson)
        parent = {}
        sink = len(self.employees) + len(customers) + 1
        max_flow = 0
        
        # Add edges from customers to sink
        for i in range(len(self.employees) + 1, len(self.employees) + len(customers) + 1):
            graph[i].append(sink)
        
        # Find augmenting paths and update flow
        while self._bfs(graph, 0, sink, parent):
            path_flow = float("Inf")
            s = sink
            while s != 0:
                path_flow = min(path_flow, 1)  # Each edge has capacity 1
                s = parent[s]
                
            max_flow += path_flow
            
            # Update residual graph
            v = sink
            while v != 0:
                u = parent[v]
                graph[u].remove(v)
                graph[v].append(u)  # Add reverse edge
                v = parent[v]
        
        # Convert the flow to matches
        for i, employee in enumerate(self.employees, 1):
            if employee.available:
                for v in graph:
                    if i in graph[v] and v > len(self.employees):  # If there's a reverse edge
                        customer = customers[v - len(self.employees) - 1]
                        employee.assign_customer(customer)
                        self.matches[customer] = employee
                        if customer in self.unmatched_customers:
                            self.unmatched_customers.remove(customer)

        return self.matches

    def get_matching_summary(self):
        summary = {
            "successful_matches": len(self.matches),
            "unmatched_customers": list(self.unmatched_customers),
            "matches": {
                customer: employee.name 
                for customer, employee in self.matches.items()
            },
            "available_employees": [
                emp.name for emp in self.employees if emp.assigned_customer == None and emp.available
            ],
            "unavailable_employees": [
                emp.name for emp in self.employees if not emp.available
            ]
        }
        return summary

def main():
    matcher = EmployeeCustomerMatcher()
    
    # Create a complex scenario where optimal matching isn't obvious
    employees = [
        # Team A - Specialists who can only handle specific customers
        Employee("Alice", allowed_customers=["Customer1", "Customer2"]),
        Employee("Bob", allowed_customers=["Customer2", "Customer3"]),
        Employee("Charlie", allowed_customers=["Customer3", "Customer4"]),
        
        # Team B - Flexible employees who can handle many customers
        Employee("David", allowed_customers=["Customer1", "Customer2", "Customer3", "Customer4"]),
        Employee("Eve", allowed_customers=["Customer1", "Customer2", "Customer3", "Customer4"]),
        
        # Team C - Backup specialists
        Employee("Frank", allowed_customers=["Customer1", "Customer4"]),
        Employee("Grace", allowed_customers=["Customer2", "Customer3"])
    ]
    
    for employee in employees:
        matcher.add_employee(employee)
    
    # We need to handle all customers
    customers = ["Customer1", "Customer2", "Customer3", "Customer4"]
    
    print("\nInitial Scenario:")
    print("Employees and their allowed customers:")
    for emp in employees:
        print(f"{emp.name}: {emp.allowed_customers}")
    
    # First matching round
    matches = matcher.match_customers(customers)
    summary = matcher.get_matching_summary()
    print("\nOptimal Matching Results:")
    print(f"Successful matches: {summary['successful_matches']}")
    print("\nMatches:")
    for customer, employee in summary['matches'].items():
        print(f"{customer} -> {employee}")
    print("\nUnmatched customers:", summary['unmatched_customers'])
    print("Available employees:", summary['available_employees'])
    
    # Now let's simulate a challenging scenario where some employees become unavailable
    print("\n--- Challenging Scenario ---")
    print("David and Eve (flexible employees) become unavailable")
    
    # Make the flexible employees unavailable
    for employee in employees:
        if employee.name in ["David", "Eve"]:
            employee.available = False
    
    # Try matching again
    matches = matcher.match_customers(customers)
    summary = matcher.get_matching_summary()
    print("\nOptimal Matching Results:")
    print(f"Successful matches: {summary['successful_matches']}")
    print("\nMatches:")
    for customer, employee in summary['matches'].items():
        print(f"{customer} -> {employee}")
    print("\nUnmatched customers:", summary['unmatched_customers'])
    print("Available employees:", summary['available_employees'])
    print("Unavailable employees:", summary['unavailable_employees'])

if __name__ == "__main__":
    main()
