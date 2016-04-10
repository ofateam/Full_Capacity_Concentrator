#   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #
# Full capacity concentrator (designed by Emre Gunduzhan) implementation    #
# Advances Switching Networks, @Bilkent University, Turkey                  #
# Spring 2016, by Omer Faruk Aktulum, ofaruk(dot)tou(at)gmail(dot)com       #
#   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #


import sys, os


#   #   #   #   #   #   #   #   STEPS of the ALGORITHM to CONCENTRATE PACKETS in FULL CAPACITY CONCENTRATORS    #   #   #   #   #   #   #
#                                                                                                                                       #
#       1. Fill three parts (I_1, I_2 and I_3) in Emre Gunduzhan's full capacity buffered concentrator design by using his formulas.    #
#       2. Meanwhile, set needed connection points among the inputs and outputs.                                                        #
#       3. Assign an output buffer to each existing packets in input buffers in I_1 and I_2 parts.                                      #
#       4. In output buffers, if there are some empty buffers (after we concentrate the existing packets in I_1 and I_2 parts)          #
#               - Fill those empty buffers with existing packets in I_3 part                                                            #
#   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #

def main():
    print '#--- SET CONCENTRATOR ATTRIBUTES ---#'
    n = int(raw_input('-- Number of inputs   (n) = '))
    m = int(raw_input('-- Number of outputs  (m) = '))
    v = int(raw_input('-- Input buffer size  (v) = '))
    w = int(raw_input('-- Output buffer size (w) = '))

    # initialize the implementation
    initialize(n, m, v, w)

def initialize(n, m, v, w):
    # Define a few variables will be used in implementation #
    capacity = m*w # capacity of the concentrator
    print '\n#--- Capacity of the concentrator = ', capacity, '---#'
    
    # Define a matrix (2D array) to keep which inputs and outputs are connected to each other
    # The value is 1 if the input has the column index is connected to the output has the row index
    connections = [[0 for column in range(n)] for row in range(m)]
    hasPartI1 = False # to know the concentrator has part I1 or not
    currentInputIndex = 0 # keep current input index
    
    # Fill part I_1
    if w/v > 0:
        hasPartI1 = True # add needed packets in part I_1
        currentInputIndex += fillPartI1(connections, m, v, w)
    
    # Fill part I_2 and part I_3
    if w%v == 0: # directly go to fill I_3
        fillPartI3(connections, hasPartI1, currentInputIndex, n, m, v, w)
    else:
        currentInputIndex += fillPartI2(connections, currentInputIndex, m, v, w)
        fillPartI3(connections, hasPartI1, currentInputIndex, n, m, v, w)
    
    # Print output connection matrix
    printConnectionMatrix(connections)

    # The last value of currentInputIndex shows the read line in the implementation
    packets = getInputPackets(capacity, n, v)
    
    # Fill the output buffers according to input packets
    fillOutputBuffers(connections, currentInputIndex ,packets, n, m, v, w)


#   #   #   #   #   Fill part I1    #   #   #   #   #   #
# Connect each output disjointly to floor(w/v) inputs   #
# Return the number of inputs used in I_1 part          #
#   #   #   #   #   #   #   #   #   #   #   #   #   #   #
def fillPartI1(connections, m, v, w):
    inputIndex = 0
    for i in range(m):
        for j in range(w/v):
            connections[i][inputIndex] = 1
            inputIndex += 1 # update index input

    return (w/v)*m # number of the inputs newly connected to outputs in I_1


#   #   #   #   #   Fill part I2    #   #   #   #   #   #   #
# Connect correct inputs and outputs according to formulas  #
# Return the number of inputs used in I_2 part              #
#   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #
def fillPartI2(connections, currentInputIndex, m, v, w):
    # some calculations
    z = w - v*(w/v) # minimum number of empty spaces at each output buffer after I_1 part
    numberOf_Ai = m*z/v # dividing a line (m*z) into intervals ;
    numberOf_Bj = m # number of the inputs, Ai_s ; number of the outputs, Bj_s
    
    # Set start and end points for each A[i] and A[j] by using a delimeter ':'
    A = [0 for row in range(numberOf_Ai)]
    startPoint = 0
    endPoint = startPoint + v
    for i in range(numberOf_Ai):
        A[i] = str(startPoint) + ':' + str(endPoint)
        startPoint = endPoint
        endPoint += v
    
    B = [0 for column in range(numberOf_Bj)]
    startPoint = 0
    endPoint = startPoint + z
    for j in range(numberOf_Bj):
        B[j] = str(startPoint) + ':' + str(endPoint)
        startPoint = endPoint
        endPoint += z

    # Fill part I_2
    for i in range(numberOf_Ai):
        for j in range(numberOf_Bj):
            if compareIntervals(A[i], B[j]) == True:
                connections[j][currentInputIndex+i] = 1 # it starts from m+i, since we connected first m of the inputs in 1st step

    return numberOf_Ai # number of the inputs newly connected to outputs in I_2


#   #   #   #   #   Fill part I3    #   #   #   #   #   #   #   #   #
# Connect each remain input (after I_1 and I_2) with each output    #
#   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #
def fillPartI3(connections, hasPartI1, currentInputIndex, n, m, v, w):
    # Fill part I_3
    for i in range(currentInputIndex, n): # number of the remain inputs after first 2 inputs
        for j in range(m):
            # Handle first input of part I_3 by checking the total number of connections in each row
            if i == currentInputIndex:
                sum = 0
                for column in range(currentInputIndex):
                    if connections[j][column] == 1:
                        sum += 1
                correctSum = 2 if hasPartI1 == False else (w/v)+2
                if sum == correctSum:
                    connections[j][i] = 0
                else:
                    connections[j][i] = 1
            else:
                connections[j][i] = 1 # fill remain inputs with 1 (connect each remain input with each output)


#   #   #   #   Comparing Intervals #   #   #   #   #   #   #   #   #
# Compare two intervals to know whether there is an intersection    #
# If there is, return True; else, return False.                     #
#   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #
def compareIntervals(int_1, int_2):
    # get start and end points of the intervals
    int_1_start = int(int_1.split(':')[0])
    int_1_end = int(int_1.split(':')[1])
    
    int_2_start = int(int_2.split(':')[0])
    int_2_end = int(int_2.split(':')[1])
    
    if int_1_start >= int_2_end or int_1_end <= int_2_start:
        return False
    else:
        return True


#   #   #   #   Print Connection Matrix   #   #   #   #   #     #   #
# Printing the input-output connection matrix                       #
#   0 : there is no connection between the input and output         #
#   1 : there is a connection between the input and output          #
#   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #
def printConnectionMatrix(connections):
    print '\n#--- INPUT-OUTPUT CONNECTION MATRIX (rows->outputs; columns->inputs) ---#'
    for i in range(len(connections)):
        print connections[i]


#   #   #   #   #   Get Input Packets    #   #   #   #   #  #
# Get input packets from the user                           #
# P[x,y] : x -> input number, y -> input buffer location    #
#   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #
def getInputPackets(capacity, n, v):
    # ask user to decide whether get some input packets or not
    userAnswer = raw_input('\nEnter some input packets (Y) or Assume that inputs are full (N): ')
    # get packets into an array, P[inputNumber][bufferLocation]
    packets = [[0 for column in range(v)] for row in range(n)]
    if userAnswer == 'Y' or userAnswer == 'y':
        numberOfInputPackets = int(raw_input('\nNumber of input packets you want to enter ( < capacity=' + str(capacity) + ' ) = '))
        print '\n#--- ENTER INPUT PACKETS P[inputNumber][bufferLocation]---#'
        if capacity < numberOfInputPackets:
            print '\n\n#--- Number of the input packets can not be greater that capacity of the concentrator ---#'
            exit()
        for packet in range(numberOfInputPackets):
            input = int(raw_input('--PACKET-' + str(packet+1) + '-- Input number of the packet ( 0 < input < ' + str(n+1) + ' ) = '))
            if input < 1 or input > n:
                print '\n\n#--- Error in entered input number ---#'
                exit()
            buffer = int(raw_input('--PACKET-' + str(packet+1) + '-- Buffer location of the packet ( 0 < buffer < ' + str(v+1) + ' ) = '))
            if buffer < 1 or buffer > v:
                print '\n#--- Error in entered buffer number ---#'
                exit()
            print '\n'
            packets[input-1][buffer-1] = 1
    elif userAnswer == 'N' or userAnswer == 'n':
        # input buffers will be full
        for i in range(len(packets)):
            for j in range(len(packets[i])):
                packets[i][j] = 1 # fill the inputs
    else:
        print '\n#--- Error in entered option ---#'
        exit()

    return packets


#   #   #   #   #   Fill Output Buffers #   #   #   #   #   #
# Fill output buffers by using the input packets            #
# P[x,y] : x -> input number, y -> input buffer location    #
# If there is some empty output buffers after concentrate   #
#       the packets in part I_1 and part I_2;               #
#          - concentrate the remain packets in part I_3     #
#   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #
def fillOutputBuffers(connections, currentInputIndex, packets, n, m, v, w):
    # define input and output buffer arrays
    outputBuffers = [[0 for column in range(w)] for row in range(m)]
    inputBuffers = [0  for column in range(n)] # each input has v buffers
    
    # use currentInputForPartI3 to keep index of the input in part I_3
    currentInputForPartI3 = currentInputIndex
    # use currentInputChange to keep number of the packets added in an input in part I_3
    currentInputChange = 0
    # implementation
    for i in range(m):
        columnIndex = 0
        for j in range(currentInputIndex): # at first, we need to get only the packets in part I_1 and I_2
            if connections[i][j] == 1: # we have a connection at this point
                for inputBuffer in range(v): # w times add a packet
                    # check the entered packets to put some packets in partI_3
                    if packets[j][inputBuffer] == 1:
                        # make understandable indexes for the user
                        outputBuffers[i][columnIndex] = str(j+1) + ':' + str(inputBuffers[j]+1)
                        inputBuffers[j] += 1 # update input buffer
                    else:
                        inputBuffers[j] += 1 # update input buffer
                        # make understandable indexes for the user
                        outputBuffers[i][columnIndex] = str(currentInputForPartI3+1) + ':' + str(inputBuffers[currentInputForPartI3]+1)
                        inputBuffers[currentInputForPartI3] += 1 # update input buffer
                        currentInputChange += 1 # update current input change
                        # update input buffer index
                        if inputBuffers[currentInputForPartI3] == v or currentInputChange == v: # if the current input is full
                            currentInputForPartI3 += 1
                            currentInputChange = 0 # update current input change
                        if currentInputForPartI3 == n:
                            break
                                
                    # update column index
                    columnIndex += 1
                    
                    if columnIndex == w or inputBuffers[j] == v:
                        break
            # current output buffer is full or each input is scanned
            if columnIndex == w or currentInputForPartI3 == n:
                break

    print '''#--- OUTPUT BUFFERS ('input_number:input_buffer(right side index)') ---#'''
    for i in range(len(outputBuffers)):
        print outputBuffers[i]

if __name__ == "__main__":
    main()