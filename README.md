# BasicNetworking
An assigment I did for a networking course to create a server that sent date and time data to a client

This was an assignment for a second level networking course that required me to write two programs in python. One a client, the
other a server, using the python socket api (which, may I say, is awkward). The server listens on a set of ports for incoming 
requests, then sends the client a packet which payload includes the date an time on the server in a particular language, based on 
what port the request was recieved on. The main purpose of this assignment was to create and compile custom packets for this
communication over UDP, which I decided to use a binary string so that I could index individual bits, which is incredibly 
inefficient, but then again, it's python.
