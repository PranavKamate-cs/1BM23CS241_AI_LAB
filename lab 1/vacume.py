def vacuum_world():
    # 0 indicates Clean and 1 indicates Dirty
    goal_state = {'A': '0', 'B': '0'}
    cost = 0

    location_input = input("Enter Location of Vacuum (A or B): ").strip().upper()
    status_input = input(f"Enter status of {location_input} (0 for Clean, 1 for Dirty): ").strip()
    status_input_complement = input("Enter status of the other room (0 for Clean, 1 for Dirty): ").strip()

    print("\nInitial Location Condition:", goal_state)

    if location_input == 'A':
        print("\nVacuum is placed in Location A")

        if status_input == '1':
            print("Location A is Dirty.")
            goal_state['A'] = '0'
            cost += 1  # cost for cleaning
            print("Location A has been Cleaned. Cost: ", cost)
        else:
            print("Location A is already clean.")

        if status_input_complement == '1':
            print("Location B is Dirty.")
            print("Moving RIGHT to Location B.")
            cost += 1  # cost for moving
            goal_state['B'] = '0'
            cost += 1  # cost for cleaning
            print("Location B has been Cleaned. Total Cost: ", cost)
        else:
            print("Location B is already clean. No action taken.")

    elif location_input == 'B':
        print("\nVacuum is placed in Location B")

        if status_input == '1':
            print("Location B is Dirty.")
            goal_state['B'] = '0'
            cost += 1  # cost for cleaning
            print("Location B has been Cleaned. Cost: ", cost)
        else:
            print("Location B is already clean.")

        if status_input_complement == '1':
            print("Location A is Dirty.")
            print("Moving LEFT to Location A.")
            cost += 1  # cost for moving
            goal_state['A'] = '0'
            cost += 1  # cost for cleaning
            print("Location A has been Cleaned. Total Cost: ", cost)
        else:
            print("Location A is already clean. No action taken.")

    print("\nGOAL STATE:", goal_state)
    print("Performance Measurement (Total Cost):", cost)


# Run the function
vacuum_world()
