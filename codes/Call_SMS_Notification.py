import serial, time

port = serial.Serial("/dev/ttyUSB0", baudrate=115200, timeout=1)

##########function to send message############
def send_message( number, message):
    print (number)
    print (message)
    port.write(str.encode('AT'+'\r\n')) # check the GSM+GPRS module, should return OK if working
    receive = port.read(100)
    print (receive)
    time.sleep(1)
    
    port.write(str.encode('AT+CMGF=1'+'\r\n'))# set to text mode
    receive= port.read(100)
    print (receive)
    time.sleep(1)
    
    AT_number='AT+CMGS="{n}"'.format(n=number)# format AT input with variable 
    
    port.write(str.encode(AT_number+'\r\n'))# the number where message is to be sent
    receive= port.read(100)
    print (receive)
    time.sleep(1)
    
    port.write(str.encode(message+'\r\n'))# the message text
    receive = port.read(100)
    print (receive)
    
    port.write(str.encode('\032'))

##########function to send message############
def call_number(number):
    print(number)

    AT_number = 'ATD{n}'.format(n = number)# format AT input with variable
    port.write(str.encode(AT_number+'\r\n'))# calls the number
    
    while (True):
        
        flag = False
        receive= port.read(100)
        print(receive)
        try : 
            if(receive[19] == 48):
                port.write(str.encode('ATH\r\n'))
                # time.sleep(15) 
                break  
        except :
            pass 