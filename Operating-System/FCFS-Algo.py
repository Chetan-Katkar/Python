"""
p1.txt
p1 0 3

p2.txt
p2 0 2

p3.txt
p3 4 2

p4.txt
p4 3 6

Fcfs_output.txt
Process Table:
pids  AT  BT
p1    0    0
p2    0    0
p3    4    0
p4    3    0

Process Table:
pids  AT  BT  CT  TAT  WT
p1    0    3    3    3    0
p2    0    2    5    5    3
p4    3    6    11    8    2
p3    4    2    13    9    7

average tat time = 6.25average tat time = 3.0
"""





#new state.
def new(number_of_files):
    file_paths = []
    for i in range(number_of_files):
        print(f"input file : ")
        file_paths.append(input())

    processes = []
    for i in range(number_of_files):
        file = open(file_paths[i])
        data = file.readline()#type of data string.
        processes.append(data)
        file.close()

    process_table = []
    for i in range(number_of_files):
        tokens = processes[i].split()
        process_table.append([])
        for t in tokens:
            process_table[i].append(t)

    return process_table


#ready
def ready(process_table):
    sorted_process_table = sorted(process_table, key = lambda x : x[1])
    return sorted_process_table


#running
def running(sorted_process_table,number_of_processes):
    copy = [process.copy() for process in sorted_process_table]
    time = 0 #System time.
    Running = []
    completed_processes = 0
    flag = 1
    j =0

    while(completed_processes < number_of_processes):
        while sorted_process_table and time >= int(sorted_process_table[0][1]):
            Running.append(sorted_process_table[0])
            sorted_process_table.pop(0)

        if(Running == []):
            time += 1
            continue

            # Get the burst time of the current process
        burst_time = int(Running[j][2])

        if burst_time > 0:
            burst_time -= 1
            time += 1
            Running[j][2] = burst_time  # Update the remaining burst time
        else:
            # Process is completed
            copy[j].append(time)  # Store completion time
            completed_processes += 1
            j += 1  # Move to the next process in the Running list

            # Reset burst_time for the next process
            if j < len(Running):
                burst_time = int(Running[j][2])

    return copy

# Print process table
def print_table(process_table):
    output = "Process Table:\n"
    output += "pids  AT  BT\n"
    for i in process_table:
        output += "    ".join(map(str, i)) + "\n"  # Convert all elements to strings
    return output


# Display process table with CT, TAT, and WT
def display(copy):
    output = "Process Table:\n"
    output += "pids  AT  BT  CT  TAT  WT\n"
    for i in copy:
        output += "    ".join(map(str, i)) + "\n"
    return output


number_of_files = int(input("enter the number of files : \n"))

#function calls
process_table = new(number_of_files)

sorted_process_table = ready(process_table)

copy = running(sorted_process_table,number_of_files)

# Average TAT and WT calculation
avg_tat = 0
avg_wt = 0
for i in range(len(copy)):
    ct = copy[i][3]  # Completion Time
    at = int(copy[i][1])  # Arrival Time
    bt = int(copy[i][2])  # Burst Time

    tat = ct - at  # Turnaround Time
    wt = tat - bt  # Waiting Time

    copy[i].append(tat)
    copy[i].append(wt)

    avg_tat += tat
    avg_wt += wt

avg_tat /= number_of_files
avg_wt /= number_of_files

file = open("Fcfs_output.txt","w")
file.write(print_table(process_table))
file.write("\n")
file.write(display(copy))
file.write("\n")
file.write(f"average tat time = {avg_tat}")
file.write(f"average tat time = {avg_wt}")
file.close()

