## High Level Approach 

-Created TCP client process with a layer of Transport Layer Security (TLS) in python
-The server gave around 1000 randomly generated mathematical problems, of which client responded 
with the correct solution.


There are four files in the project

-client.py: is the main file of the program. This is called in terminal.
-inputchk.py: This file accomodates error handling and unification of both ssl and non ssl code 
within the same project
-solution.py: This code does the arithmetic operation of all operations sent by server
-socks.py: This file has functions which create a socket connection,connect to the server as well 
send and recieve data. This returns socket object as output.


### Challenges faced

-Recieve Statement right under while loop
Initially we just put the sock.recv statement right under while loop,which created a blocking condition
and no output was displayed on screen. 
Checking condition outside while loop solved the problem
-Making a unified code for both SSL and without SSL client processes
-Adding defensive coding and modular programming to increase effieciency and reusability

### Overview of How we tested the code
We divided the testing into four parts
-First we tested a simple program for client and server socket creation and communication. The server was hosted 
on localhost
-Secondly we implemented an SSL socket connection similar to above step.
-Thirdly we created a separate library for socket creation and completion functions called socks.py and called
 those functions from the main file called client.py
-The fourth testing involved all the error handling all the possiblities in passing arguments as input.
-The final testing involved interaction with the allocated server run on ccis machines,updating client.py and 
making a file called solutions.py to complete the project.
  
				

 

