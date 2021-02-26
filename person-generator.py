# Mason Collett - Sprint 3 Assignment
# Person Generator Project
# 2/11/2021

from tkinter import *
import sys
import os
import random
import csv

# when click submit on the gui
def submit():
    # clear previous entry from gui
    output.delete('1.0', END)

    # get filename
    filename = selected_state.get()
    state_name = filename # save for later
    filename = "archive/"+filename.lower() + ".csv"
    # open input file
    lines = open(filename).read().splitlines()

    # write to file, save addresses to print to gui
    gui_addresses = write_output_csv(lines,state_name,int(number.get()),True)
    # write to gui
    for address in gui_addresses:
        output.insert(END,address)

# Gets random addresses from the correct state csv
# Cleans up and writes addresses to csv
def write_output_csv(lines,state_name,num_addr,gui):
    gui_addresses = []
    with open("output2.csv",mode="w",newline='') as outfile:
        outfile_writer = csv.writer(outfile,delimiter=',',quotechar='"',quoting=csv.QUOTE_MINIMAL)
        outfile_writer.writerow(['input_state', 'input_number_to_generate', 'output_content_type','output_content_value'])

        # get random addresses
        i = 0
        while(i < num_addr):
            street_address = get_address(lines)

            #clean address up, make sure it's valid/readable  
            if(len(street_address[3]) > 1 and len(street_address[2])> 1):
                output_address = make_output_address(street_address)
                # write to file
                outfile_writer.writerow([state_name, num_addr, 'street address',output_address])
                # write to gui list
                output_address = output_address  + "\n"
                gui_addresses.append(output_address)
                i = i+1

    # addresses needed for gui
    if(gui):
        return gui_addresses
    return

# Gets a random address from lines
def get_address(lines):
    address = random.choice(lines)
    street_address = address.split(',')
    return street_address

# Does the "cleanup" of an address, converts to string
def make_output_address(street_address):
    # start at address number
    output_address = street_address[2]
    j = 3
    while(j < 9):
        # add all parts to the output address
        if(street_address[j]):
            output_address = output_address + " " 
        output_address = output_address + street_address[j]
        j = j + 1
    return output_address

# Call other program to create data
def request_data():
    print("person-generator.py REQUESTING DATA FROM life-generator.py")
    # run other service
    os.system("python3 life-generator.py input.csv")  # change this to match
    lines = open('output.csv').read().splitlines()  
    # print the other service's data
    print("data received:")
    for i in lines:
        print(i)
    print("=========")


def main():
    # input file given
    if(len(sys.argv) == 2):
        # get data from input.csv
        infile = open(sys.argv[1]).read().splitlines()
        num_addr = infile[1].split(',')
        filename = num_addr[0]
        num_addr = int(num_addr[1])

        # get filename
        state_name = filename # save for later
        filename = "archive/"+filename.lower() + ".csv"

        # open correct csv file
        lines = open(filename).read().splitlines()

        # get addresses, write to output file
        write_output_csv(lines,state_name,num_addr,False)

    elif(len(sys.argv)==3):
        # get other microservice data
        request_data()


# Global GUI setup
# Dropdown menu list implemented with help from: 
# https://stackoverflow.com/questions/45441885/how-can-i-create-a-dropdown-menu-from-a-list-in-tkinter
if(len(sys.argv)<2):
    master = Tk()
    number = StringVar()

    # create state dropdown
    state_list = []
    # initialize list of state names for menu
    for filename in os.listdir('archive'):
        state_list.append(filename[:-4].upper())
    state_label = Label(master, text = "Select state")
    selected_state = StringVar(master)
    selected_state.set(state_list[0]) # default value
    w = OptionMenu(master, selected_state, *state_list)
    state_label.pack()
    w.pack()

    # create number input
    number_label = Label(master, text = "# Addresses to get")
    number_entry = Entry(master,textvariable = number, font=('calibre',10,'normal'))
    number_label.pack()
    number_entry.pack()
    gen_number = number.get()

    # create button
    button = Button(master, text="Submit", command=submit)
    button.pack()

    # create output area
    # implemented with help from:
    # https://www.python-course.eu/tkinter_text_widget.php
    output_label = Label(master, text = "Output")
    output = Text(master, height = 10, width = 50)
    S = Scrollbar(master)
    S.pack(side=RIGHT, fill=Y)
    output_label.pack()
    output.pack(side=LEFT, fill = Y)
    S.config(command = output.yview)
    output.config(yscrollcommand=S.set)
            
    mainloop()

if __name__ == "__main__":
    main()
