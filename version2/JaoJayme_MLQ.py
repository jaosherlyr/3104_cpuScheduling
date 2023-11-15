# Work of:  JAO, Sherly R.
#           JAYME, Joel T.
# --------------------------

import queue

class Process:
    def __init__(self, process_id, arrival_time, burst_time):
        self.process_id = process_id
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.remaining_time = burst_time
        self.end_time = 0
        self.turnaround_time = 0
        self.waiting_time = 0

def mlq_scheduling(process_list, quantum_time):
    # Separate processes into multiple queues based on priority
    high_priority_queue = queue.Queue()
    medium_priority_queue = queue.Queue()
    low_priority_queue = queue.Queue()

    for process in process_list:
        if process.burst_time <= 5:
            high_priority_queue.put(process)
        elif 5 < process.burst_time <= 10:
            medium_priority_queue.put(process)
        else:
            low_priority_queue.put(process)

    time = 0
    timeline = []

    while not (high_priority_queue.empty() and medium_priority_queue.empty() and low_priority_queue.empty()):
        if not high_priority_queue.empty():
            current_process = high_priority_queue.get()
        elif not medium_priority_queue.empty():
            current_process = medium_priority_queue.get()
        else:
            current_process = low_priority_queue.get()

        if current_process.remaining_time <= quantum_time:
            time += current_process.remaining_time
            current_process.end_time = time
            timeline.append((current_process.process_id, current_process.end_time))
        else:
            time += quantum_time
            current_process.remaining_time -= quantum_time
            if current_process.burst_time <= 5:
                medium_priority_queue.put(current_process)
            elif 5 < current_process.burst_time <= 10:
                low_priority_queue.put(current_process)
            else:
                low_priority_queue.put(current_process)

    return timeline

def display(process_list, calculated_process):
    print("\nTABLE:")
    print(f"{'Process' : <10} {'Arrival Time' : ^15} {'Burst Time' : ^15} {'End Time' : ^15} {'Turnaround Time' : ^15} {'Waiting Time' : >15}")

    process_list.sort(key=lambda x: x.process_id)
    for i, process in enumerate(process_list):
        print(f"{f'P{process.process_id}' : <10} {process.arrival_time : ^15} {process.burst_time : ^15} {process.end_time : ^15} {process.turnaround_time : ^15} {process.waiting_time : >15}")

    max_end_time = max(process.end_time for process in process_list)
    total_burst_time = sum(process.burst_time for process in process_list)
    total_turnaround_time = sum(process.turnaround_time for process in process_list)
    total_waiting_time = sum(process.waiting_time for process in process_list)
    length = len(process_list)

    avg_turnaround_time = total_turnaround_time / length
    avg_waiting_time = total_waiting_time / length
    cpu_utilization = (total_burst_time / max_end_time) * 100

    print(f"\nAVERAGE Turnaround Time: {avg_turnaround_time:.2f}")
    print(f"AVERAGE Waiting Time: {avg_waiting_time:.2f}")
    print(f"CPU Utilization: {cpu_utilization:.2f}%")

    print("\nGANTT CHART:")
    print("|-------" * len(calculated_process) + "|")
    print("|", end="")
    for process_id, end_time in calculated_process:
        print(f"\tP{process_id}\t|", end="")

    print("\n" + "|-------" * len(calculated_process) + "|")
    print("0", end="")
    for _, end_time in calculated_process:
        print(f"\t\t{end_time}", end="")

def main():
    print("\nMULTI-LEVEL QUEUE [MLQ] CPU SCHEDULING")
    num_processes = int(input("\nEnter the # of Processes: "))
    process_list = []

    print("\nEnter the ARRIVAL TIME and BURST TIME of each P (separate with a space):")
    for i in range(num_processes):
        user_input_time = input(f"P{i + 1}: ")
        times = user_input_time.split()

        if len(times) == 2:
            arrival_time = int(times[0])
            burst_time = int(times[1])
            process_id = int(i + 1)
            process_list.append(Process(process_id, arrival_time, burst_time))


    quantum_time = int(input("\nEnter the Quantum Time for the MLQ scheduling: "))
    timeline = mlq_scheduling(process_list, quantum_time)

    for i, (process_id, end_time) in enumerate(timeline):
        process_list[i].end_time = end_time
        process_list[i].turnaround_time = process_list[i].end_time - process_list[i].arrival_time
        process_list[i].waiting_time = process_list[i].turnaround_time - process_list[i].burst_time

    display(process_list, timeline)

if __name__ == "__main__":
    main()
