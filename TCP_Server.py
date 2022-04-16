###############################################################################################
#Autor: EDE

#This is some Python socket programming training
#Lets user move up and down direcotries and up- and download files.

###############################################################################################
import socket
import threading
import subprocess
import os
import re

def run_command(request):
     """DOCSTRING"""


     print("run_command: ", request)
 
     try:
        output = subprocess.check_output(request, shell=True) 
     except:
        output = "Failed to execute command."
     
     return output       


def run_upload(request_string,client_socket):
   """DOCSTRING"""     
   print("uploading file")
   cwd = os.getcwd()
   filename = request_string.split()[1]
   #upload_destination = cwd + "\\" + request_string.split()[1]
   upload_destination = cwd + "/" + request_string.split()[1]
   file_descriptor = open(upload_destination,"wb") 
   
   client_socket.send("File created! Start sending Data".encode())

   data = client_socket.recv(1024)
   iterr = 0
   while(data):
      iterr+=1   
      print("RUNDE: "+str(iterr))   	   	
      file_descriptor.write(data)       
      if len(data) < 1024:   		
         break   	
      data = client_socket.recv(1024)	

   file_descriptor.close()

   #response = client.recv(1024)
   print("Fire Transfer Complete")

def run_download(request_string,client_socket):
   """DOCSTRING""" 
   print("download file")
   cwd = os.getcwd()
   filename = request_string.split()[1]
   download_destination = cwd + "/" + request_string.split()[1]
   f = open(download_destination, "rb")
   buffer = f.read(1024)        
   
   client_socket.send(buffer)

   iterr = 0
   while (buffer):                        
      iterr+=1   
      print("RUNDE: "+str(iterr))
      print("Length: "+str(len(buffer)))          
      client_socket.send(buffer)  
      buffer = f.read(1024)
      if not buffer:
         break




bind_ip = ""
bind_port = 9999
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((bind_ip,bind_port)) 
server.listen(5) 
print("[*] Listening on %s : %d" % (bind_ip,bind_port))

# this is our client-handling thread
def handle_client(client_socket): 
 """"DOCSTRING"""
 # print out what the client sends 
 
 while True: 
      cmd_recv = client_socket.recv(1024)
     
      request_string = str(cmd_recv)
      request_string_len = len(request_string)
      request_string.rstrip()
      request_string = request_string[2:request_string_len-1]
      print("recieced message: " + request_string)

      #Upload File
      if request_string.split()[0] == "-up" and len(request_string.split()) == 1:
         output = client_socket.send("No file specified!".encode())

      if request_string.split()[0] == "-up" and len(request_string.split()) == 2:       
         try:  
            output = run_upload(request_string,client_socket)
            output = client_socket.send("Successfully uploaded file".encode()) 
         except:
            output = client_socket.send("Failed to upload file".encode())

      #Download File
      if request_string.split()[0] == "-down" and len(request_string.split()) == 1:   
         output = client_socket.send("No file specified!".encode())

      if request_string.split()[0] == "-down" and len(request_string.split()) == 2:   
         try:  
            output = run_download(request_string,client_socket)
            output = client_socket.send("Successfully downloaded file".encode()) 
         except:
            output = client_socket.send("Failed to download file".encode())
         

      #only rudimentary change directory commands goin up and down one level
      try:
         if request_string.split()[0] == "-cd":
            print(os.getcwd())
            cwd = os.getcwd()

            if request_string.split()[1] != "..":
               target_dir_name = request_string.split()[1]
               #target_dir_path = cwd + "\\" + target_dir_name
               target_dir_path = cwd + "/" + target_dir_name
               target_dir_path_escaped = re.escape(target_dir_path)
               os.chdir(target_dir_path_escaped)
               client_socket.send("Changed directory to: ".encode() + target_dir_path_escaped.encode())


            if request_string.split()[1] == "..":    
               target_dir_path = os.path.dirname(cwd)
               target_dir_path_escaped = re.escape(target_dir_path)
               os.chdir(target_dir_path_escaped)
               client_socket.send("Changed directory to: ".encode() + target_dir_path_escaped.encode())
      except:
         client_socket.send("Failed to change directory".encode())
            
      if request_string.split()[0] == "client_exit":
         client_socket.close()

      if request_string.split()[0] == "-c" and len(request_string.split()) == 1:
         output = client_socket.send("No command specified!".encode())

      if request_string.split()[0] == "-c" and len(request_string.split()) != 1:
         try:
            command_input = " ".join(request_string.split()[1:])
            output = run_command(command_input)
            client_socket.send(output)
         except:
            output = "Failed to execute command or moved directory."
            client_socket.send(output.encode())


while True:
 client,addr = server.accept() 
 print("[*] Accepted connection from: %s:%d" % (addr[0],addr[1]))
 # spin up our client thread to handle incoming data
 client_handler = threading.Thread(target=handle_client,args=(client,))
 client_handler.start() 