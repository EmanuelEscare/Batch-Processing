import random
import time
import tkinter as tk

# Initialize global variables
global_batches = []
pending_batches = 0
clock = 0
pending_processes = []
finished_processes = []
i_button = 0
e_button = 0

def validate_input(P):
    if P == "" or P.isdigit():
        return True
    else:
        return False
    
# Clean the program's state
def clean_program():
    global global_batches, pending_batches, clock, pending_processes, finished_processes
    global_batches = []
    pending_batches = 0
    clock = 0
    pending_processes = []
    finished_processes = []
    output_text_finished_processes.delete(1.0, tk.END)
    i_button = 0
    e_button = 0

# Generate processes and save them to a file
def generate_processes():
    n = input_process_num.get()
    clean_program()
    batch_count = 1
    names = ["Jose", "Carlos", "Carolina", "Juan"]
    operations = ["+", "-", "*", "/"]
    data = []
    
    # Generate random processes
    for _ in range(int(n)):
        name = random.choice(names)
        operation = random.choice(operations)
        numerator = random.randrange(0, 99)
        denominator = random.randrange(0, 99)
        task = f"{numerator}{operation}{denominator}"
        tme = random.randrange(4, 13)
        data.append([name, task, tme])
        
    try:
        # Write processes to a file
        with open(f"Lote.txt", "w") as file:
            for idx, (name, task, tme) in enumerate(data, start=1):
                if batch_count == 1:
                    file.write(f"Lote {batch_count}\n\n")
                    batch_count += 1
                
                file.write(f"{idx}. {name}\n{task}\nTME: {tme}\n")
                
                if idx < len(data) and idx % 5 == 0:
                    file.write(f"\nLote {batch_count}\n")
                    batch_count += 1
                if idx < len(data):
                    file.write("\n")
        load_processes()
    except Exception as e:
        print("Error:", e)

# Load process information from file
def load_processes():
    global global_batches
    with open('Lote.txt', 'r') as file:
        content = file.read()

    batches = content.split('Lote')
    batch = [batch.strip() for batch in batches if batch.strip()]

    # Process records in each batch
    for batch in batches:
        line = batch.split('\n')
        num_batches = line[0]
        tasks = line[1:]
        
        task_flag = 1
        flag = 1
        tasks_batch = []
        task_name = ''
        task_task = ''
        task_tme = ''
        
        # Process individual tasks in a batch
        for task in tasks:
            if task != '':
                if flag == 1 and task_flag == 1:
                    task_name = task
                    task_flag = 2
                    flag = 0
                if flag == 1 and task_flag == 2:
                    task_task = task
                    task_flag = 3
                    flag = 0
                if flag == 1 and task_flag == 3:
                    task_tme = task
                    task_flag = 1
                if task_flag == 1:
                    tasks_batch.append([task_name, task_task, task_tme])
                flag = 1
        global_batches.append(tasks_batch)
    global_batches.pop(0)
    process_processes()

# Process pending processes
def process_processes():
    global global_batches, pending_batches, clock, pending_processes, finished_processes
    
    total_batches = len(global_batches)
    
    for batch_data in global_batches:
        total_batches -= 1
        
        output_pending_batches.config(text="Lotes Pendientes: " + str(total_batches))
                
        while 0 != len(batch_data):
            process = batch_data.pop(0)
            
            print_pending_processes = '\n'.join(['\n'.join(item) + "\n" for item in batch_data])
            
            output_text_pending_processes.delete(1.0, tk.END)
            output_text_pending_processes.insert(tk.END, print_pending_processes)
            
            process = processing(process)
            if len(process) == 3:
                batch_data.append(process)
            else:
                finished_processes.append(process)
                show_finished_processes()
                
        output_text_pending_processes.delete(1.0, tk.END)

# Process individual process            
def processing(process):
    global clock, i_button, e_button
    operation = process[1]
    tme = process[2].split(':')
    tme = int(tme[1])
    for _ in range(tme):
        time.sleep(1)
        process_update = process[0] + "\n" + process[1] + "\nTME: " + str(tme) + "\n" 
        output_text_process.delete(1.0, tk.END)
        output_text_process.insert(tk.END, process_update)
        clock += 1
        output_clock.config(text="Reloj Global: " + str(clock))
        tme -= 1
        process[2] = 'TME:'+str(tme)
        
        if(i_button == 1):
            i_button = 0
            output_text_process.delete(1.0, tk.END)
            return process
        if(e_button == 1):
            e_button = 0
            output_text_process.delete(1.0, tk.END)
            return [process[0], process[1] + " = Error"]
            
            
        # Refresh the window to see the changes
        root.update()
        
    output_text_process.delete(1.0, tk.END)
    try:
        result = eval(process[1])
        return [process[0], process[1] + " = " + str(round(result,2))]
    except ZeroDivisionError:
        return [process[0], process[1] + " = Error"]

# Show completed processes 
def show_finished_processes():
    print_finished_processes = '===| Lote 1 |======\n\n'
    
    index = 0
    batch_count = 1
    for process in finished_processes:
        index+=1
        
        for item in process:
            print_finished_processes = print_finished_processes+item+'\n'
        print_finished_processes = print_finished_processes+'\n'
        if(index < len(finished_processes) and index % 5 == 0):
            batch_count+=1
            print_finished_processes = print_finished_processes+'===| Lote '+str(batch_count)+' |======\n\n'
            
    output_text_finished_processes.delete(1.0, tk.END)
    output_text_finished_processes.insert(tk.END, print_finished_processes)

# Get results and save them to a file
def get_results():
    with open("Resultados.txt", "w") as file:
        
        file.write("Lote 1\n\n")
        batch_counter = 1
        counter = 0
        for process in finished_processes:
            file.write(str(process[0]) + "\n")
            file.write(str(process[1]) + "\n\n")
            counter += 1
        
            if counter % 5 == 0 and counter != len(finished_processes):
                batch_counter += 1
                file.write("Lote " + str(batch_counter) + "\n\n")


def interruption_button():
    global i_button
    i_button = 1   
    return

def error_button():
    global e_button
    e_button = 1
    return

# Create the GUI interface
root = tk.Tk()

# Grid Top

process_label = tk.Label(root, text="# Procesos:")
process_label.grid(row=0, column=0, padx=5, pady=0)

validate_cmd = root.register(validate_input)
input_process_num = tk.Entry(root, validate="key", validatecommand=(validate_cmd, "%P"))
input_process_num.grid(row=1, column=0, padx=0, pady=20)

button_generate = tk.Button(root, text="GENERAR", command=generate_processes)
button_generate.grid(row=1, column=1, padx=0, pady=20)

output_clock = tk.Label(root, text="Reloj Global:")
output_clock.grid(row=0, column=2, padx=5, pady=20)

# Grid Center

output_label_pending_processes = tk.Label(root, text="EN ESPERA")
output_label_pending_processes.grid(row=2, column=0, padx=5, pady=0)
output_label_process = tk.Label(root, text="EJECUCION")
output_label_process.grid(row=2, column=1, padx=5, pady=0)
output_label_finished_processes = tk.Label(root, text="TERMINADOS")
output_label_finished_processes.grid(row=2, column=2, padx=5, pady=0)

# Text boxes 
output_text_pending_processes = tk.Text(root, height=15, width=20)
output_text_pending_processes.grid(row=3, column=0, padx=10, pady=0)

output_text_process = tk.Text(root, height=3, width=20)
output_text_process.grid(row=3, column=1, padx=10, pady=10)

output_text_finished_processes = tk.Text(root, height=15, width=20)
output_text_finished_processes.grid(row=3, column=2, padx=10, pady=0)

# Grids Bottom
# Button to interrupt process and generate error
button_get = tk.Button(root, text="INTERRUPCIÓN [X]", command=interruption_button)
button_get.grid(row=4, column=0, padx=5, pady=20)

button_get = tk.Button(root, text="ERROR [/]", command=error_button)
button_get.grid(row=4, column=1, padx=5, pady=20)

# Number of batches and button to get results
output_pending_batches = tk.Label(root, text="# de Lotes pendientes")
output_pending_batches.grid(row=5, column=0, padx=5, pady=20)

button_get = tk.Button(root, text="OBTENER RESULTADOS", command=get_results)
button_get.grid(row=5, column=2, padx=5, pady=20)

root.title("ProcesamientoPorLotes")

frame = tk.Frame(root)
frame.grid()


root.mainloop()
