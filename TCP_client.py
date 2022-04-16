from encodings import utf_8
from operator import truediv
import socket
import subprocess
import sys
import os

target_host = "127.0.0.1"
#target_host = "10.0.2.255"
#target_host = "192.168.56.1"
target_port = 9999

# create a socket object
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
# connect the client
client.connect((target_host,target_port))

f = open("cat.png", "rb")
#size = os.stat("cat.png").st_size

f = open("uptext1.txt", "rb")
#print("size: "+ str(size))
buffer = f.read(1024)

while True:
   cmd_input = input("Input: ")

   #Run Command
   if cmd_input.split()[0] == "-c":
      try:
         client.send(cmd_input.encode())
         response = client.recv(4096) #recv(<Buffersize>)
         print(response)
      except:
         output = "Failed to execute command."

   #Change directory
   if cmd_input.split()[0] == "-cd":
      try:
         client.send(cmd_input.encode())
         response = client.recv(4096) #recv(<Buffersize>)
         print(response)
      except:
         output = "Failed to change directory."         
  
   #Upload file
   if cmd_input.split()[0] == "-up":
      try:
         
         client.send(cmd_input.encode())

         #recieve Ack from Server
         response = client.recv(1024)
         print(response)

         #client.send(buffer)
         iterr = 0
         while (buffer):            
            
            iterr+=1
            print("RUNDE: "+str(iterr))
            print("Length: "+str(len(buffer)))                
            #client.send(bytes(iterr))
            client.send(buffer)  
            buffer = f.read(1024)
            if not buffer:
               break

      except:
         output = "Failed to upload file."

   #download file
   if cmd_input.split()[0] == "-down":
      """DOCSTRING"""     
      print("downloading file")
      cwd = os.getcwd()
      print("TEST")
      filename = cmd_input.split()[1]
      print("TEST2")
      #upload_destination = cwd + "\\" + request_string.split()[1]
      upload_destination = cwd + "/" + cmd_input.split()[1]
      file_descriptor = open(upload_destination,"wb") 
      print("TEST3")
      #client.send("File created! Start sending Data".encode())

      data = client.recv(1024)
      print("Data: " + str(data))
      
      iterr = 0
      while(data):
         iterr+=1
         print("RUNDE: "+str(iterr))
         print("Length: "+str(len(data)))
         print("Data: "+str(data))            	   	
         file_descriptor.write(data)          
         if len(data) < 1024:   		
            print("Break!")
            break   	
         data = client.recv(1024)	

      file_descriptor.close()


   if cmd_input == "help":
      print("exit - exits program")
   
   if cmd_input == "exit":
      client.send("client_exit".encode())
      client.close()
      exit()


###### TODO
#linux unterschied / und \, na toll
#Server: socket.close()
#client: args für filename
#exit server command

