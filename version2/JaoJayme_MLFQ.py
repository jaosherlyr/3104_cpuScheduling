# Work of:  JAO, Sherly R.
#           JAYME, Joel T.
# --------------------------
import copy


def get_input():
    num_layers = int(input("\nEnter the # of Layers: "))
    quantum_time = []

    print("\n")
    for i in range(num_layers - 1):
        user_input_qt = input(f"Quantum Time {i + 1}: ")

        quantum_time.append(int(user_input_qt))

    print("\n[1] First Come First Serve - [FCFS]")
    print("[2] Shortest Job First - [SJF]")
    print("[3] Priority - Nonpreemptive - [P-NP]")
    end_layer = int(input("Choose the algorithm for the End Layer: "))

    num_processes = int(input("\nEnter the # of Processes: "))
    process_list = []

    end_time = 0
    turnaround_time = 0
    waiting_time = 0

    if end_layer == 3:
        print("\nEnter the ARRIVAL TIME, BURST TIME, and PRIORITY of each P (separate with a space):")
    else:
        print("\nEnter the ARRIVAL TIME and BURST TIME of each P (separate with a space): ")

    for i in range(num_processes):
        user_input_time = input(f"P{i + 1}: ")

        times = user_input_time.split()

        arrival_time = int(times[0])
        burst_time = int(times[1])
        process_id = int(i + 1)

        if len(times) == 3:
            priority = int(times[2])
            process_list.append(
                [process_id, arrival_time, burst_time, priority, end_time, turnaround_time, waiting_time])
        elif end_layer != 3:
            process_list.append([process_id, arrival_time, burst_time, end_time, turnaround_time, waiting_time])

    return process_list, quantum_time, end_layer, num_layers


def display(process_list, calculated_process, quantum_time, end_layer):
    for i in range(len(quantum_time)):
        print(f"\nQT {i + 1}: {quantum_time[i]}", end="")

    print("\nTABLE:")
    if end_layer == 3:
        print(
            f"{'Process' : <10} {'Arrival Time' : ^15} {'Burst Time' : ^15} {'Priority' : ^15} {'End Time' : ^15} {'Turnaround Time' : ^15} {'Waiting Time' : >15}")
    else:
        print(
            f"{'Process' : <10} {'Arrival Time' : ^15} {'Burst Time' : ^15} {'End Time' : ^15} {'Turnaround Time' : ^15} {'Waiting Time' : >15}")

    process_list.sort(key=lambda x: x[0])
    for i, process in enumerate(process_list):
        if end_layer == 3:
            print(
                f"{'P' + str(process[0]) : <10} {process[1] : ^15} {process[2] : ^15} {process[3] : ^15} {process[4] : ^15} {process[5] : ^15} {process[6] : >15}")
        else:
            print(
                f"{'P' + str(process[0]) : <10} {process[1] : ^15} {process[2] : ^15} {process[3] : ^15} {process[4] : ^15} {process[5] : >15}")

    end_index = 3 if end_layer != 3 else 4
    turnaround_index = 4 if end_layer != 3 else 5
    waiting_index = 5 if end_layer != 3 else 6

    max_end_time = max(process[end_index] for process in process_list)
    total_burst_time = sum(process[2] for process in process_list)
    total_turnaround_time = sum(process[turnaround_index] for process in process_list)
    total_waiting_time = sum(process[waiting_index] for process in process_list)
    length = len(process_list)

    print(f"\nAVERAGE Turnaround Time: {total_turnaround_time / length :.2f}")
    print(f"AVERAGE Waiting Time: {total_waiting_time / length :.2f}")
    print(f"CPU Utilization: {(total_burst_time / max_end_time) * 100 :.2f}%")

    print("\nGANTT CHART:")
    print("|-------" * len(calculated_process) + "|")
    print("|", end="")
    for i, process in enumerate(calculated_process):
        if process['value'] == 'idle':
            print(" idle  |", end="")
        else:
            print(f"\tP{process['value']}\t|", end="")

    print("\n" + "|-------" * len(calculated_process) + "|")
    print("0", end="")
    for i, process in enumerate(calculated_process):
        print(f"\t\t{process['end']}", end="")


def create_process(value, start, end):
    return {
        'value': value,
        'start': start,
        'end': end
    }


def mlfq(process_list, quantum_time, end_layer, num_layers):
    current_index = 0
    current_time = 0
    current_oder = 0

    timeline = []
    order_last_layer = []
    order_list = [[] for i in range(num_layers)]
    list_length = len(process_list)
    empty = True

    #  sort by arrival time
    process_list.sort(key=lambda x: x[1])
    #  make a copy of the sorted list for the altered burst time
    copy_list = copy.deepcopy(process_list)

    #  first while loop for the arrival times
    while current_index < list_length:
        #  check if the current time is greater than or equal to the arrival time
        if current_time >= copy_list[current_index][1]:
            #  if yes, then append to order[0]
            order_list[0].append(current_index)
            current_index += 1
        #  if not then loop through the order_list and find which one is not empty
        else:
            for i in range(num_layers):
                if order_list[i]:
                    #  set not_empty to true
                    empty = False
                    current_oder = i
                    break

            #  if the current time is < the arrival time and the order_list is empty then dile
            if empty:
                idle = create_process('idle', current_time, copy_list[current_index][1])
                timeline.append(idle)
                current_time = idle['end']
            #  if not_empty then pop and make process
            else:
                popped_index = order_list[current_oder].pop(0)
                #  determine the time to use if burst time or quantum time
                b_time = copy_list[popped_index][2]
                if current_oder != num_layers - 1:  # the current_order is the last order layer
                    time = b_time if b_time < quantum_time[current_oder] else quantum_time[current_oder]
                else:
                    time = b_time
                #  create process
                process = create_process(copy_list[popped_index][0], current_time, current_time + time)
                timeline.append(process)
                current_time = process['end']
                copy_list[popped_index][2] = copy_list[popped_index][2] - time

                #  determine if the remaining burst time is zero
                if copy_list[popped_index][2] != 0:  # if there is still left over burst time then append
                    if current_oder != num_layers - 1:
                        order_list[current_oder + 1].append(popped_index)
                    else:
                        order_list[current_oder].append(popped_index)
                else:
                    end_time = current_time
                    turnaround_time = end_time - process_list[popped_index][1]
                    waiting_time = turnaround_time - process_list[popped_index][2]

                    if end_layer == 3:
                        process_list[popped_index][4:7] = [end_time, turnaround_time, waiting_time]
                    else:
                        process_list[popped_index][3:6] = [end_time, turnaround_time, waiting_time]

            empty = True

    #  second loop for the remaining orders
    for i in range(num_layers - 1):
        # while the current order_list index is not empty
        while order_list[i]:
            popped_index = order_list[i].pop(0)
            b_time = copy_list[popped_index][2]
            time = b_time if b_time < quantum_time[i] else quantum_time[i]
            # make process
            process = create_process(copy_list[popped_index][0], current_time, current_time + time)
            timeline.append(process)
            current_time = process['end']
            copy_list[popped_index][2] = copy_list[popped_index][2] - time

            #  determine if the remaining burst time is zero
            if copy_list[popped_index][2] != 0:  # if there is still left over burst time then append
                order_list[i + 1].append(popped_index)
            else:
                end_time = current_time
                turnaround_time = end_time - process_list[popped_index][1]
                waiting_time = turnaround_time - process_list[popped_index][2]

            if end_layer == 3:
                process_list[popped_index][4:7] = [end_time, turnaround_time, waiting_time]
            else:
                process_list[popped_index][3:6] = [end_time, turnaround_time, waiting_time]

    while order_list[num_layers - 1]:  # while the last layer order is not empty
        order_last_layer.append(process_list[order_list[num_layers - 1].pop(0)][:])

    if end_layer == 2:
        order_last_layer.sort(key=lambda x: x[2])
    elif end_layer == 3:
        order_last_layer.sort(key=lambda x: x[3])

    #  third loop for the last layer set of orders
    while order_last_layer:
        popped_order = order_last_layer.pop(0)
        ndx = process_list.index(popped_order)
        b_time = copy_list[ndx][2]
        # make process
        process = create_process(popped_order[0], current_time, current_time + b_time)
        timeline.append(process)
        current_time = process['end']

        end_time = current_time
        turnaround_time = end_time - process_list[ndx][1]
        waiting_time = turnaround_time - process_list[ndx][2]

        if end_layer == 3:
            process_list[ndx][4:7] = [end_time, turnaround_time, waiting_time]
        else:
            process_list[ndx][3:6] = [end_time, turnaround_time, waiting_time]

    return timeline


def main():
    print("\nMULTILEVEL FEEDBACK QUEUE - [MLFQ]")
    process_list, quantum_time, end_layer, num_layers = get_input()
    # process_list = [
    #     [1, 5, 30, 4],
    #     [2, 25, 15, 3],
    #     [3, 15, 25, 1],
    #     [4, 10, 10, 1],
    #     [5, 20, 35, 2],
    #     [6, 13, 5, 5]
    # ]
    # quantum_time = [10, 15]
    # end_layer = 3
    # num_layers = 3
    calculated_process = mlfq(process_list, quantum_time, end_layer, num_layers)
    display(process_list, calculated_process, quantum_time, end_layer)


if __name__ == "__main__":
    main()
