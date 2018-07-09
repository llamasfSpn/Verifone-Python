###############################################################################
#    Author: llamasfSpn 
#    2018 - now
#    Example Python Function to send amount to PinPad Verifone Vx820
#    Response from PinPad in Spanish Languages
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
##############################################################################
#!/usr/bin/python
# python executable
import socket

def send_amount(host,port,total_with_tax,user,name,client,shop,tpv):
	_logger.info('Send Amount to PinPad')
	HOST = host
	PORT = port
	BUFFER_SIZE = 1024
	amount = float(total_with_tax)
	amount = "%.2f" % amount
	amount = str(amount).replace('.', '')
	amount = amount.replace(',', '')
	user = str(user)
	name= str(name).replace('-', '') #replace if is necesary
	name = name.replace('/', '') #replace if is necesary
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	_logger.info('HOST PORT')
	try:
		s.connect((HOST, PORT))
		s.send("\x02"+str(client)+";"+str(shop)+";"+str(tpv)+";" + user + ";" + name + ";1;" + amount + ";;;;;;;\x03")
		data = s.recv(BUFFER_SIZE)
		if "OPERACION ACEPTADA" in data:
		    print "OPERACION ACEPTADA:", data
		    card = [x for x in data.split(';')]
		    print card
		    card_ticket = ";OP.:"+card[5]+";Cuenta:"+card[12]+";Trj:"+card[11]+";Num.OP:"+card[24]+";Cod.Aut:"+card[25]
		    s.send("\x02ACK\x03")
		    s.close()
		    return "OK"+card_ticket

		if "OPERACION CANCELADA" in data:
		    print "OPERACION CANCELADA:", data
		    s.send("\x02ACK\x03")
		    s.close()
		    return "ERROR OPERACION CANCELADA"

		if "ERROR" or "error" in data:
		    print "ERROR:", data
		    s.send("\x02ACK\x03")
		    s.close()
		    return "ERROR LECTURA TARJETA"
		    # break

	except EOFError as e:
	    print "ERROR: Connection closed: %s" % e

#Call Function
host='127.0.0.1' #char
port = 1234 #number
total_with_tax = 10 #number
user = 'david' #char
name = 'david' #char
client = #your code of pinpad client
shop =  #code of shop
tpv =  #code of tpv

send_amount(host,port,total_with_tax,user,name,client,shop,tpv)
