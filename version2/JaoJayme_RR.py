import copy

def get_input():
    num_processes = int(input("\nEnter the # of Processes: "))
    process_list = []

    end_time = 0
    turnaround_time =0
    waiting_time = 0

    print("\nEnter the ARRIVAL TIME and BURST TIME(separate with a space):")
    for i in range(num_processes):
        user_input_time = input(f"P{i + 1}: ")

        times= user_input_time.split()

        if len(times) == 2:
            arrival_time = int(times[0])
            burst_time = int(times[1])
            process_id = int(i + 1)

            process_list.append([process_id, arrival_time, burst_time, end_time, turnaround_time, waiting_time])

    return process_list

def get_qt():
    return int(input("\nEnter Quantum Time: "))

def display(process_list, calculated_process, quantum_time):
    print(f"\nQUANTUM TIME: {quantum_time}")

    print("\nTABLE:")
    print(f"{'Process' : <10} {'Arrival Time' : ^15} {'Burst Time' : ^15} {'End Time' : ^15} {'Turnaround Time' : ^15} {'Waiting Time' : >15}")

    process_list.sort(key=lambda x: x[0])
    for i, process in enumerate(process_list):
        print(f"{'P' + str(process[0]) : <10} {process[1] : ^15} {process[2] : ^15} {process[3] : ^15} {process[4] : ^15} {process[5] : >15}")

    max_end_time = max(process[3] for process in process_list)
    total_burst_time = sum(process[2] for process in process_list)
    total_turnaround_time = sum(process[4] for process in process_list)
    total_waiting_time = sum(process[5] for process in process_list)
    length = len(process_list)

    print(f"\nAVERAGE Turnaround Time: {total_turnaround_time / length :.2f}")
    print(f"AVERAGE Waiting Time: {total_waiting_time / length :.2f}")
    print(f"CPU Utilization: {(total_burst_time/max_end_time) * 100 :.2f}%")


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

def rr(process_list, quantum_time):
    completed_processes = process_list[:]

    process_list.sort(key=lambda x: x[1])
    timeline = []
    order_list = []
    current_time = 0
    copy_list = copy.deepcopy(process_list)
    length = int(len(copy_list))

    running_process = 0
    current_process_idx = 0


    queued_list = []
    remaining_burst_time = 0

    for x in range(len(copy_list)):
        remaining_burst_time += copy_list[x][2]

    while remaining_burst_time != 0:
        while len(copy_list) > 0 and copy_list[0][1] <= current_time:
            if len(queued_list) == 0:
                if len(timeline) == 0 or timeline[-1]['end'] != current_time:
                    p = create_process(queued_list[-1][0] if len(queued_list) > 0 else "idle", copy_list[0][1], current_time)
                    timeline.append(p)
            queued_list.append(copy_list[0])
            copy_list.pop(0)

        if len(queued_list) > 0:
            if queued_list[0][2] <= quantum_time:
                current_time += queued_list[0][2]
                remaining_burst_time -= queued_list[0][2]

                completed_processes[queued_list[0][0]-1][3] = current_time

                p = create_process(queued_list[0][0], queued_list[0][1], current_time)
                timeline.append(p)

                queued_list.pop(0)
            else:
                current_time += quantum_time

                p = create_process(queued_list[0][0], queued_list[0][1], current_time)
                timeline.append(p)

                while len(copy_list) > 0 and copy_list[0][1] <= current_time:
                    queued_list.append(copy_list[0])
                    copy_list.pop(0)

                queued_list[0][2] -= quantum_time
                queued_list.append(queued_list.pop(0))

                remaining_burst_time -= quantum_time
        else:
            current_time += 1

    for p in range(len(completed_processes)):
        completed_processes[p][4] = completed_processes[p][3] - completed_processes[p][1]
        completed_processes[p][5] = completed_processes[p][4] - completed_processes[p][2]

    return completed_processes, timeline

print("\nROUND ROBIN [RR]")
process_list = get_input()
quantum_time = get_qt()
completed_processes, calculated_process = rr(process_list, quantum_time)
display(completed_processes, calculated_process, quantum_time)