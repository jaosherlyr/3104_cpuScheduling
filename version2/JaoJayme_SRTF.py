# Work of:  JAO, Sherly R.
#           JAYME, Joel T.
# --------------------------
import copy

def get_input():
    num_processes = int(input("\nEnter the # of Processes: "))
    process_list = []

    end_time = 0
    turnaround_time =0
    waiting_time = 0

    print("\nEnter the ARRIVAL TIME and BURST TIME of each P (separate with a space):")
    for i in range(num_processes):
        user_input_time = input(f"P{i + 1}: ")

        times= user_input_time.split()

        if len(times) == 2:
            arrival_time = int(times[0])
            burst_time = int(times[1])
            process_id = int(i + 1)

            process_list.append([process_id, arrival_time, burst_time, end_time, turnaround_time, waiting_time])

    return process_list

def display(process_list, calculated_process):
    print("\nTABLE:")
    print(f"{'Process' : <10} {'Arrival Time' : ^15} {'Burst Time' : ^15} {'End Time' : ^15} {'Turnaround Time' : ^15} {'Waiting Time' : >15}")

    process_list.sort(key=lambda x: x[0])
    for i, process in enumerate(process_list):
        print(f"{'P' + str(process[0]) : <10} {process[1] : ^15} {process[2] : ^15} {process[3] : ^15} {process[4] : ^15} {process[5] : >15}")

    max_end_time = max(process['end'] for process in calculated_process)
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

def srtf(process_list):
    process_list.sort(key=lambda x: x[1])
    timeline = []
    order_list = []
    current_time = 0
    copy_list = copy.deepcopy(process_list)
    length = int(len(copy_list))

    for i in range(len(copy_list)):
        if current_time < copy_list[i][1] and not order_list:
            idle = create_process('idle', current_time, copy_list[i][1])
            current_time = idle['end']
            timeline.append(idle)

        if i != length - 1:
            order_list.append(copy_list[i][:])
            order_list.sort(key=lambda x: x[2])
            while current_time != copy_list[i + 1][1]:
                if not order_list:
                    idle = create_process('idle', current_time, copy_list[i + 1][1])
                    current_time = idle['end']
                    timeline.append(idle)
                else:
                    popped_order = order_list.pop(0)
                    ndx = copy_list.index(popped_order)
                    temp = copy_list[i + 1][1] - current_time
                    end = current_time + popped_order[2] if popped_order[2] < temp else current_time + temp

                    process = create_process(popped_order[0], current_time, end)
                    current_time = process['end']
                    timeline.append(process)
                    copy_list[ndx][2] = copy_list[ndx][2] - (popped_order[2] if popped_order[2] < temp else temp)

                    if copy_list[ndx][2] != 0:
                        order_list.append(copy_list[ndx][:])
                        order_list.sort(key=lambda x: x[2])
                    else:
                        end_time = current_time
                        turnaround_time = end_time - process_list[ndx][1]
                        waiting_time = turnaround_time - process_list[ndx][2]

                        process_list[ndx][3:6] = [end_time, turnaround_time, waiting_time]

        else:
            order_list.append(copy_list[i][:])
            order_list.sort(key=lambda x: x[2])
            while order_list:
                popped_order = order_list.pop(0)
                ndx = copy_list.index(popped_order)
                if current_time < popped_order[1]:
                    idle = create_process('idle', current_time, popped_order[1])
                    current_time = idle['end']
                    timeline.append(idle)
                else:
                    process = create_process(popped_order[0], current_time, current_time + popped_order[2])
                    current_time = process['end']
                    timeline.append(process)

                    end_time = current_time
                    turnaround_time = end_time - process_list[ndx][1]
                    waiting_time = turnaround_time - process_list[ndx][2]

                    process_list[ndx][3:6] = [end_time, turnaround_time, waiting_time]

    return timeline

def main():
    print("\nSHORTEST REMAINING TIME FIRST [SRTF]")
    process_list = get_input()
    calculated_process = srtf(process_list)
    display(process_list, calculated_process)

if __name__ == "__main__":
    main()