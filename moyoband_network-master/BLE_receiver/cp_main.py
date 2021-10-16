import struct
import bluepy.btle as bl
import socket
import os
import json
import netifaces as ni
import time
import signal
ni.ifaddresses('wlan0')
HOST = ni.ifaddresses('wlan0')[ni.AF_INET][0]['addr']
SERVER = '192.168.0.144'
PORT = 7508
PORT_S = 7509
MAX_BANDS = 8
global data_packet

data_packet = {
        "mac_addr":"",
        "HR": 0,
        "SPO2":0,
        "Temperature":0
        }

patients = []
pipein, pipeout = os.pipe()

def update_bands_list(n, m):
    # #Receive dictionaries with bands info from server
    income = bytearray(65000) 
    bytes_num = os.readv(pipein,[income]) 
    print("Received!") 
    received_payload = income[:bytes_num].decode('utf-8') 
    jsn = ''.join(chr(int(x,2)) for x in received_payload.split())
    global patients
    patients = json.loads(jsn) 

def on_exit(*args):
    print("I try to kill ", os.getpid() + 1)
    os.kill(os.getpid() + 1, signal.SIGKILL)
    print("\nNow i go suicide.. \n")
    os.kill(os.getpid(), signal.SIGKILL)
    

if os.fork() > 0:
    
    print("Parent is here ", os.getpid(),"\n")
    signal.signal(signal.SIGINT, on_exit)
    time.sleep(2)
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        while(1):
            s.listen()
            conn, addr = s.accept()
            with conn:
                print("Connection from ", addr[0])
                while True:
                    data = conn.recv(1024)
                    if not data:
                        break
                    received = data.decode("utf-8")
                    
                    if received[17] == "1":
                        data_packet["mac_addr"] = received[:17]
                        patients.append(data_packet.copy())
                    else:
                        for scan in patients:
                            if scan["mac_addr"] == received[:17]:
                                patients.remove(scan)
                    str = json.dumps(patients)
                    binary = ' '.join(format(ord(letter), 'b') for letter in str)
                    os.write(pipeout,bytearray(binary,'utf-8'))                    
                    os.kill(os.getpid() + 1, signal.SIGUSR1)
                    
else:
    
    print("Child is here")
    band_iterator = 0
    signal.signal(signal.SIGUSR1,update_bands_list)
    time.sleep(5)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((SERVER,PORT))
    while(1):        
        if(patients):
            #print(patients)
            print("Continue " + str(band_iterator))
            
            mac = patients[(band_iterator%len(patients))]["mac_addr"]           
            band_iterator += 1
            con = 0;
            print("Connecting with " + mac)
            try:
                if((data_packet["mac_addr"] == mac) and (len(patients) > 1)):
                    continue
                con = bl.Peripheral(mac,bl.ADDR_TYPE_RANDOM)
                print("Connection established",con)

    #characteristics
                ch = con.getCharacteristics()

    #data
                data= [[] for k in range(len(ch))]

    #Loading descriptors
                for count,k in enumerate(ch):
                    data[count].append(str(ch[count]))

#loading characteristics to data
                for k in range(1):
                    for count,i in enumerate(ch):
                            try:     
                                    data[count].append(i.read())
                            except:
                                    data[count].append("Data is not readable")

#closing connection
                con.disconnect()
                print("data5: ", type(data[6][1]), "  ", data[6][1])
                print("Disconnected")
                data_packet["mac_addr"] = mac
                data_packet["HR"] = str(int.from_bytes(data[5][1], byteorder='big'))
                data_packet["SPO2"] = str(int.from_bytes(data[7][1],byteorder='big'))
                data_packet["Temperature"] = str(data[6][1][1]) + "." +str(data[6][1][0])            
                print("Writing done")
                
            
                #Generate and send data
                payload = ""
                for i in data_packet:
                    payload += data_packet[i] +", "

                print(payload)
                try:    
                    #with socket.socket(socekt.AF_INET, socket.SOCK_STREAM) as ss:
                    #    print("0!!!")
                    #    ss.connect((SERVER,PORT))
                    #   print("1!!")
                    #    ss.sendto(b'text', (SERVER,PORT))
                   
                    s.sendto(bytearray(payload,'utf-8'),(SERVER,PORT))
                    print("Sent!")
                except:
                    print("couldn't send ")
                
            except:
                 print("conn failed",con)
                
#writing data to file
           # writing_to_file = open("Data.txt","w+")
           # for kcount,k in enumerate(data):
           #         for count,i in enumerate(k):
           #                 if (count!=0 and (kcount==3 or kcount==5 or kcount==7) ):
           #                         writing_to_file.write(str(struct.unpack('b',i)[0])+"\n")


            #                elif(count!=0 and kcount==2):
            #                        writing_to_file.write(str(struct.unpack('q',i)[0])+"\n")
            #                elif(count!=0 and kcount==1):
            #                        writing_to_file.write(str(struct.unpack('h',i)[0])+"\n")

            #                elif(count!=0 and kcount==6):
            #                        d, f = struct.unpack('cc',i)
            #                        print(d)
            #                        print(f)
            #                        d = int.from_bytes(d, byteorder="big", signed=False)
            #                        f = int.from_bytes(f, byteorder="big", signed=False)
            #                        writing_to_file.write(str(d) + "." + str(f) +"\n")
            #                else:
            #                        writing_to_file.write(str(i)+"\n")
            #        writing_to_file.write("\n")
            print("Reading done")
            time.sleep(2)
