# Work of:  JAO, Sherly R.
#           JAYME, Joel T.
# --------------------------
def get_input():
    num_processes = int(input("\nEnter the # of Processes: "))
    process_list = []

    end_time = 0
    turnaround_time =0
    waiting_time = 0

    print("\nEnter the ARRIVAL TIME, BURST TIME, and PRIORITY of each P (separate with a space):")
    for i in range(num_processes):
        user_input_time = input(f"P{i + 1}: ")

        times= user_input_time.split()

        if len(times) == 3:
            arrival_time = int(times[0])
            burst_time = int(times[1])
            priority = int(times[2])
            process_id = int(i + 1)

            process_list.append([process_id, arrival_time, burst_time, priority, end_time, turnaround_time, waiting_time])

    return process_list

def display(process_list, calculated_process):
    print("\nTABLE:")
    print(f"{'Process' : <10} {'Arrival Time' : ^15} {'Burst Time' : ^15} {'Priority' : ^15} {'End Time' : ^15} {'Turnaround Time' : ^15} {'Waiting Time' : >15}")

    process_list.sort(key=lambda x: x[0])
    for i, process in enumerate(process_list):
        print(f"{'P' + str(process[0]) : <10} {process[1] : ^15} {process[2] : ^15} {process[3] : ^15} {process[4] : ^15} {process[5] : ^15} {process[6] : >15}")

    max_end_time = max(process['end'] for process in calculated_process)
    total_burst_time = sum(process[2] for process in process_list)
    total_turnaround_time = sum(process[5] for process in process_list)
    total_waiting_time = sum(process[6] for process in process_list)
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

def p_np(process_list):
    process_list.sort(key=lambda x: x[1])
    timeline = []
    order_list = []
    current_time = 0

    for i in range(len(process_list)):
        ndx = i

        if current_time > process_list[i][1]:
            order_list.append(process_list[i][:])
            order_list.sort(key=lambda x: x[3])

        else:
            if not order_list:
                if current_time < process_list[i][1]:
                    idle = {
                        'value': 'idle',
                        'start': current_time,
                        'end': process_list[i][1]
                    }
                    timeline.append(idle)
                    current_time = process_list[i][1]

                process = {
                    'value':  process_list[i][0],
                    'start': current_time,
                    'end': current_time + process_list[i][2]
                }
                current_time = process['end']
                timeline.append(process)

            else:
                if current_time == process_list[i][1]:
                    order_list.append(process_list[i][:])
                    order_list.sort(key=lambda x: x[3])

                popped_order = order_list.pop(0)
                ndx = process_list.index(popped_order)

                process = {
                    'value':  popped_order[0],
                    'start': current_time,
                    'end': current_time + popped_order[2]
                }
                current_time = process['end']
                timeline.append(process)

                if popped_order[0] != process_list[i][0]:
                    if current_time > process_list[i][1]:
                        order_list.append(process_list[i][:])
                        order_list.sort(key=lambda x: x[3])

            end_time = current_time
            turnaround_time = end_time - process_list[ndx][1]
            waiting_time = turnaround_time - process_list[ndx][2]

            process_list[ndx][4:7] = [end_time, turnaround_time, waiting_time]

    while order_list:
        popped_order = order_list.pop(0)
        index = process_list.index(popped_order)

        process = {
            'value':  popped_order[0],
            'start': current_time,
            'end': current_time + popped_order[2]
        }
        current_time = process['end']
        timeline.append(process)

        end_time = current_time
        turnaround_time = end_time - popped_order[1]
        waiting_time = turnaround_time - popped_order[2]

        process_list[index][4:7] = [end_time, turnaround_time, waiting_time]

    return timeline

def main():
    print("\nPRIORITY - NONPREEMPTIVE [P-NP]")
    process_list = get_input()
    calculated_process = p_np(process_list)
    display(process_list, calculated_process)

if __name__ == "__main__":
    main()