#! /usr/bin/env python

#Program written on November 2016, Ines Barreiros - Interdisciplinary Bioscience DTP

#This is a  Game of Life-like Cellular Automaton, it provides a way to model populations by modification of input variables.
#You can interact with this Cellular Automaton by creating an initial configuration and observing how it evolves. You will also be able to define a number of initial variables.

import matplotlib.pyplot as plt
import random, copy, os, timeit #Import all the necessary modules.

print 'This program is a a Cellular Auomaton aka Game of Life, it will allow you to observe the evolution of state of the animal population over time and according the parameters inital set. \n The rules of this Game of Life are: \n   (1) Animals need to eat at least a minimum amount of food to survive; \n   (2) An animal grazes in every place one unit away from the position in which it was created; \n    (3) An animal eating food reduces the amount of food in those field units; \n   (4) Food regrows at a constant rate; \n (5) If there is space, an animal will breed;\n   (6) Animals can breed up, down, left or right. \n '

print 'In this game you will be able to define a number of variables: height and width - dimensions of the board/field of the game; number_of_animals - inital number of animals in the field;  start food - inital food available, which is also the maximum food; regrowth rate - food regrowth rate per cycle of the game; numer of loops - number of generations you want to display.\n '


sim_name = str(raw_input ('Please provide a name for your simulation: \n '))

script_dir = os.getcwd()
results_dir = os.path.join(script_dir, sim_name)

if not os.path.isdir(results_dir):
    os.makedirs(results_dir)
    
output_file = open(os.path.join(results_dir,'Game_of_Life_output.txt'), 'w') #Create file in which the output of the game will be written.


#Ask for input from the user for variables:
height = int(raw_input ('Please define the size of the board/field of the game. What will be the height? \n '))
if type(height) != int:
    print 'That is not a number! Please enter a number for the height of the board game.'

width = int(raw_input ('Please define the size of the board/field of the game. What will be the width? \n '))
if type(width) != int:
    print 'That is not a number! Please enter a number for the width of the board game.'

number_of_animals = int(raw_input ('How many animals there will in the board at the beggining of the game? \n '))
if type(number_of_animals) != int:
    print 'That is not a number! Please enter a number for the initial number of animals in the board game.'

start_food = int(raw_input ('What will be the maximum amount of food available per space? This will also be the amount of food initially available. \n '))
if type(start_food) != int:
    print 'That is not a number! Please enter a number for the maximum amount of food available per space.'

regrowth_rate = int(raw_input ('What will be the food regrowth rate per cycle of the game? \n '))
if type(regrowth_rate) != int:
    print 'That is not a number! Please enter a number for the regrowth rate.'

num_loops = int(raw_input ('How many further generations would you like to display? \n '))
if type(num_loops) != int:
    print 'That is not a number! Please enter a number for the regrowth rate.'

#Print summary of initial conditions to output file
print >> output_file,'Input conditions \n', 'Height of the board game - ', height, '\n', 'Width of the board game - ', width, '\n', 'Initial number of animals - ', number_of_animals, '\n', 'Starting/maximum food - ', start_food, '\n', 'Food regrowth rate - ', regrowth_rate, '\n', 'Number of generations - ', num_loops, '\n'

def food_neighbours(col,row,height,width): #An animal grazes in every place one unit away from the position in which it was created. This function defines the coordinates for eating taking into account the position of the animal, also considering where animals are in corners or sides of the board.
    list_food_neighbours = [[col,row]]
    if (col == 0) & (row == 0): #Corner of the board 
        list_food_neighbours.append([col+1,row])
        list_food_neighbours.append([col+1,row+1])
        list_food_neighbours.append([col,row+1])
    elif (col == 0) & (row == (height-1)): #Another corner of the board 
        list_food_neighbours.append([col+1,row])
        list_food_neighbours.append([col+1,row-1])
        list_food_neighbours.append([col,row-1])
    elif (col == (width-1)) & (row == 0): #Another corner of the board 
        list_food_neighbours.append([col-1,row])
        list_food_neighbours.append([col-1,row+1])
        list_food_neighbours.append([col,row+1])
    elif (col == (width-1)) & (row == (height-1)): #Another corner of the board 
        list_food_neighbours.append([col-1,row])
        list_food_neighbours.append([col-1,row-1])
        list_food_neighbours.append([col,row-1])
    elif (col == 0): #Left column of the board
        list_food_neighbours.append([col,row+1])
        list_food_neighbours.append([col,row-1])
        list_food_neighbours.append([col+1,row-1])
        list_food_neighbours.append([col+1,row+1])
        list_food_neighbours.append([col+1,row])
    elif (col) == ((width-1)):  #Right column of the board
        list_food_neighbours.append([col,row+1])
        list_food_neighbours.append([col,row-1])
        list_food_neighbours.append([col-1,row-1])
        list_food_neighbours.append([col-1,row+1])
        list_food_neighbours.append([col-1,row])
    elif (row == 0): #Top column of the board
        list_food_neighbours.append([col+1,row])
        list_food_neighbours.append([col-1,row])
        list_food_neighbours.append([col-1,row+1])
        list_food_neighbours.append([col+1,row+1])
        list_food_neighbours.append([col,row+1])
    elif (row == (height-1)): #Bottom row of the board
        list_food_neighbours.append([col+1,row])
        list_food_neighbours.append([col-1,row])
        list_food_neighbours.append([col-1,row-1])
        list_food_neighbours.append([col+1,row-1])
        list_food_neighbours.append([col,row-1])
    else: #Any other place on the board
        list_food_neighbours.append([col,row+1])
        list_food_neighbours.append([col,row-1])
        list_food_neighbours.append([col-1,row])
        list_food_neighbours.append([col-1,row-1])
        list_food_neighbours.append([col-1,row+1])
        list_food_neighbours.append([col+1,row])
        list_food_neighbours.append([col+1,row-1])
        list_food_neighbours.append([col+1,row+1])
        
    return list_food_neighbours

def breeding_neighbours(col,row,height,width): # If there is space, an animal will breed and animals can breed up, down, left or right. This function defines the coordinates for breeding taking into account the position of the animal, also considering where animals are in corners or sides of the board.
    list_breeding_neighbours = []
    if (col == 0) & (row == 0):  #Corner of the board 
        list_breeding_neighbours.append([col+1,row])
        list_breeding_neighbours.append([col,row+1])
    elif (col == 0) & (row == (height-1)): #Another corner of the board 
        list_breeding_neighbours.append([col+1,row])
        list_breeding_neighbours.append([col,row-1])
    elif (col == (width-1)) & (row == 0): #Another corner of the board 
        list_breeding_neighbours.append([col-1,row])
        list_breeding_neighbours.append([col,row+1])
    elif (col == (width-1)) & (row == (height-1)): #Another corner of the board 
        list_breeding_neighbours.append([col-1,row])
        list_breeding_neighbours.append([col,row-1])
    elif (col == 0): #Left column of the board
        list_breeding_neighbours.append([col,row+1])
        list_breeding_neighbours.append([col,row-1])
        list_breeding_neighbours.append([col+1,row])
    elif (col == (width-1)): #Right column of the board
        list_breeding_neighbours.append([col,row+1])
        list_breeding_neighbours.append([col,row-1])
        list_breeding_neighbours.append([col-1,row])
    elif (row == 0): #Top column of the board
        list_breeding_neighbours.append([col+1,row])
        list_breeding_neighbours.append([col-1,row])
        list_breeding_neighbours.append([col,row+1])
    elif (row == (height-1)): #Bottom row of the board
        list_breeding_neighbours.append([col+1,row])
        list_breeding_neighbours.append([col-1,row])
        list_breeding_neighbours.append([col,row-1])
    else: #Any other place on the board
        list_breeding_neighbours.append([col,row+1])
        list_breeding_neighbours.append([col,row-1])
        list_breeding_neighbours.append([col-1,row])
        list_breeding_neighbours.append([col+1,row])
        
    return list_breeding_neighbours

def initialise_animals(height,width,number_of_animals): #Confirms the initial number of animals is not larger than space available & randomly places the initial number of animals in the game board.
    
    if number_of_animals > int(width*height):
        print'Error: number of starting animals is larger than space available.'
        return

    
    temp_board_animals = [[0 for col in range(width)] for row in range(height)]

    count = 1 

    while count <= number_of_animals:
        col = random.randrange(width)
        row = random.randrange(height)
        
        if temp_board_animals[row][col] == 0:
            temp_board_animals[row][col] = 1
            count += 1

    return temp_board_animals #Temporary position of animals in the board for initial cycle is defined.


def eating(board_animals,board_food,master_list_food_neighbours): #Makes animals eat on the adequate location (one unit away from their location, in any direction).
    temp_board_animals = copy.deepcopy(board_animals)
    temp_board_food = copy.deepcopy(board_food)
    
    for col in range(width):
        for row in range(height):
            
            if board_animals[row][col] == 1:
                eating_areas = master_list_food_neighbours[row][col]

                eaten_check = 0 #Before eating, the amount of eating for the current cycle is 0.

                for item in eating_areas: #Where each animals ie eating whithin the eating areas the animal can eat.
                    if board_food[item[1]][item[0]] > 0: #item 1 is row, item 0 is column; here the function will go through all the items of the list of neighbours that we previously created
                        temp_board_food[item[1]][item[0]] -=1
                        eaten_check = 1 #Means the animal did ate.

                if eaten_check == 0: #If the animal still did not eat after the eating phase (because there was no food available), then the animal will die.
                    temp_board_animals[row][col]= 0
    
    return temp_board_animals,temp_board_food #Temporary position of animals in the board and board of food with new amounts.

def breeding(board_animals,master_list_breeding_neighbours): #Breeding will happen in the appropriate locations. If 2 animals breeding areas overlap only one of them will bread on that area, therefore number of animals per space unit will not exceed 1 animal.
    temp_board_animals = copy.deepcopy(board_animals)
    
    for col in range(width):
        for row in range(height):
            
            if board_animals[row][col] == 1:
                breeding_areas = master_list_breeding_neighbours[row][col]
                
                for breeding_location in breeding_areas:
                    if board_animals[breeding_location[1]][breeding_location[0]] ==0:
                        temp_board_animals[breeding_location[1]][breeding_location[0]]  = 1
    return temp_board_animals #New temporary position of animals after the breeding.
                            
                 
def food_growth(board_food,start_food,regrowth_rate): #With time, food will regrowth at the define rate...
    temp_board_food = copy.deepcopy(board_food)
    
    for col in range(width):
        for row in range(height):
            temp_board_food[row][col] += regrowth_rate
            
            if temp_board_food[row][col] > start_food:
                temp_board_food[row][col] = start_food #...however food amount will never be higher than the initially defined maximum.
            if temp_board_food[row][col] < 0:
                temp_board_food[row][col] = 0
    return temp_board_food #New amount of food in the board, considering the food eaten at the beggining of the cycle and the amount of food that regrowth at the end of the cycle.

def generation(board_animals,board_food): #For each generation, the functions above will be called - the animal will eat (and die if it doesn't eat), breed, and food will regrowth.
    board_animals,board_food = eating(board_animals,board_food,master_list_food_neighbours)
    board_food = food_growth(board_food,start_food,regrowth_rate)
    board_animals = breeding(board_animals,master_list_breeding_neighbours)
    
    return board_animals,board_food #Location of animals and food at the end of generation cycle.

def disp_board(board): #Function that will be used to display output in different lines of text.
    str_boad = ''
    for line in board: 
        str_boad += '\n'
        str_boad += str(line)
    return str_boad


def board_image(board_food,board_animals):  #Function that makes an image of the state of the board at each generation.
    fig = plt.figure()
    plt.imshow(board_food,cmap=plt.get_cmap('RdYlGn'), clim=(0, start_food), interpolation='nearest') # a colormap from red (0) to green (maximum food) is used to display the amount of food.
    for col in range(width):
        for row in range(height):
             if board_animals[row][col]:
                    plt.scatter(x=[col], y=[row], c='k', s=1) #a scatter plot of black dots is used to display the location of living animals
    return fig


start = timeit.default_timer() #Initiates stopwatch for time the program takes to run.

#Calling all the functions necessary to run the generations with all steps and displaying output:   
board_food = [[start_food for col in range(width)] for row in range(height)]
board_animals = initialise_animals(height,width,number_of_animals)

master_list_food_neighbours = [[food_neighbours(col,row,height,width) for col in range(width)] for row in range(height)]
master_list_breeding_neighbours = [[breeding_neighbours(col,row,height,width) for col in range(width)] for row in range(height)]

print '\nSimulation running...'

print >> output_file, 'Initial food amount and distribution \n', disp_board(board_food), '\n \n', 'Initial animals location', '\n', disp_board(board_animals)

fig = board_image(board_food,board_animals)
plt.savefig(os.path.join(results_dir,('generation_0_initial_state.png')))

#Will loop through the life process during the number of generations the user wants to display
for generation_number in range(1,num_loops):
    
    board_animals,board_food = generation(board_animals,board_food)
    print >> output_file, '\n', '--------------------------------------------------------------------------------'
    print >> output_file, '\n','Generation:'
    print >> output_file, generation_number
    print >> output_file, '\n','Food amount and distribution at the end of this generation:'
    print >> output_file, disp_board(board_food)
    print >> output_file, '\n','Animals location at the end of this generation:'
    print >> output_file, disp_board(board_animals)
    fig = board_image(board_food,board_animals)
    plt.savefig(os.path.join(results_dir,('generation_' + str(generation_number) + '.png'))) #saving of the state of each generation as a PNG file
    plt.close(fig) #Close figures to avoid unnecessary memory usage.
    

generation_number = num_loops
board_animals,board_food = generation(board_animals,board_food)

print >> output_file, '\n', '--------------------------------------------------------------------------------'
print >> output_file, '\n','Final generation:'
print >> output_file, generation_number
print >> output_file, '\n','Food amount and distribution at final generation:'
print >> output_file, disp_board(board_food)
print >> output_file, '\n','Animals location at the final generation:'
print >> output_file, disp_board(board_animals)
fig = board_image(board_food,board_animals)
plt.savefig(os.path.join(results_dir,('generation_' + str(generation_number) + '_final_state.png')))

print '\nSimulation complete.'
print '\nYou can now find the evolution your population over', generation_number, ' generations in a folder with the name of your simulation in TXT and PNG formats.'

stop = timeit.default_timer() #Stops stopwatch for time the program takes to run.

print  >> output_file, '\n', '\n________________________________________________________________________________ \n','Time the Game of Life took to run: ', stop - start, ' seconds' #Prints how long the program took to run.

#End of the program, close all the files opened.
output_file.close()


