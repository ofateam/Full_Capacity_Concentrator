# Full Capacity Buffered Concentrator (desgined by Emre Gunduzhan) Implementation in Python.

The steps of Gunduzhan's design for full capacity buffered concentrators are implemented in Python. With this implementation, you can create your concentrators by giving the parameters below, enter input packets, and find the output buffer positions of the input packets by following the directions on the program screen.
        
        Parameters:
                -- Number of inputs   (n)
                -- Number of outputs  (m)
                -- Input buffer size  (v)
                -- Output buffer size (w)
        
According to given parameters, the program calculates capacity of the concentrator, and input-output connection matrix by using
theoretical formulas created and designed by Emre Gunduzhan. You can easily know which inputs and outputs are connected to each other by examining the input-output connection matrix.

After calculation of the input-output connection matrix, the program asks you to decide whether you want to enter information of some input packets or not. If you want, you can enter the information by the help of guidance of the program. On the other hand, you also select the other way where all the input buffers are assumed full. It means that there is a packet to concentrate at each input buffer. In both of these two cases, the program calculates the correct output buffer and prints on the program screen.

This implementation is a good example of full capacity buffered concentrators in terms of its a few smart features. 

        -- It always considers input packets in Part I_1 and Part I_2 of Emre Gunduzhan's design to concentrate at first.
        -- After concentrate those packets, if there is still empty buffers at outputs, the program automatically fills them by using the packets in Part I_3 of Emre Gunduzhan's design. 
        
Omer Faruk Aktulum
