from calculations import calculate_human_design

# Calculate Human Design for a specific birth date
result = calculate_human_design((1968, 2, 21, 11, 15, 0, 3))  # Year, Month, Day, Hour, Minute, Second, UTC Offset

# Access the results
print(f"Energy Type: {result['energy_type']}")
print(f"Authority: {result['authority_name']}")
print(f"Profile: {result['profile']}")
print(f"Defined Centers: {result['defined_centers']}")
