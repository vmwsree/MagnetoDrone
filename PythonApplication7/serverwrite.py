import socket               # Import socket module
from subprocess import Popen, PIPE

import time
import pickle
mos=[]
lettr=[]
curen=""
letter= {'ru':' ','luldrdrulurdru':'a','luldrdrurdru':'a','ldrdrulurdru':'a','ldrdrurdru':'a','luldrdrurd':'a','rululdrdrululd':'b','ldlururdldlu':'b','rdrurdld':'b','ldrurdldlu':'b','ldrurdld':'b','rdrurdldluld':'b','rdrurdldlu':'y','rululdrurdldlu':'b','ruldrdrulu':'b','rululdrdrululd':'b','ruldrdrululd':'b','ldluldrdru':'c','luldrdru':'c','ldrdru':'c','ldrdruldrd':'d','luldrdruldrdru':'d','luldrdrulurd':'d','rululdrdru':'e','rdrululdrdru':'e','rdrululdrdrulu':'e','ruldrdrululdru':'f','rululdrdrululdru':'f','luldrdruldlu':'g','luldrdrurdldluru':'g','luldrdrurdldluld':'g','ldrdruldlu':'g','luldrdrurdldlu':'g','rululdrdrurdru':'h','ldlururd':'h','ldrurd':'n','rurdru':'n','rululdrurdru':'h','ruldrurd':'h','ld':'i','ldrd':'i','rd':'i','rdld':'i','ruldluru':'j','rurdldluru':'j','ruldlu':'j','ldruldrdru':'k','ldruldlurdru':'k','ldlururdldrdru':'k','rdruldrdru':'k','rdruldrd':'k','rululdrd':'l','ruldluldrdru':'l','rululdrdru':'l','ruldru':'l','rurdrurdrurdld':'m','rurdldlururdrurdru':'m','ldrurdlururdld':'m','rdrurdrurdldru':'m','rdrurdrurd':'m','rdrurdldlururdld':'m','rurdrurdru':'n','rdrurdldrurdru':'n','ruldrurdld':'n','rurdldlururd':'n','rurdldrurdldrdru':'n','rdldrdrurd':'n','rurdldlururdld':'n','luldrdrulu':'o','ldrdrulu':'o','rdrululd':'o','ldrdrululd':'o','lururdld':'p','rulururdldlu':'p','rurdlururdld':'p','rdrulururdldlu':'p','rurdldrurd':'n','ldlururdld':'p','luldrdruldru':'q','luldrdruldru':'q','ldrdrululdru':'q','luldrdrululdrdru':'q','rurdluru':'r','rdldlururd':'r','rululdrdrurdru':'r','rdlururd':'r','rurdldlururd':'r','luldrdrurdldlu':'s','luldrdldlu':'s','rdluldrdldlu':'s','ldrdld':'s','luldrdrurdldlu':'s','luldruldrdru':'t','luldluruldrdrurd':'t','rdrurdru':'u','rurdrurd':'u','rurdrululdrdru':'u','rurdruldrdru':'u','rdru':'v','rdrululdrd':'v','rdrurdru':'w','ldrurdru':'w','rdrurdrulu':'w','rdruldrdrululd':'w','rdldruldrdru':'x','rurdldruldrdru':'x','rdldrurdldrd':'x','rdrurdldluru':'y','rdruldrdldluru':'y','rurdrurdldluru':'y','rurdruldlu':'y','rurdruldru':'y','ruldru':'z','ruldrurd':'z','rurdldrdru':'z','rdldrd':'z'}
s = socket.socket()         # Create a socket object
host = '192.168.3.189' # Get local machine name
port = 12346 
def findlet(curlet):
	global letter
	if curlet:
		print curlet
		try:nowltr = letter[curlet]
		except:pass
		'''	print "coudnt Find Do you want to add ?"+str(curlet)
			if( 'y' == input()):
				print "Enter:"
				rel=input()
				curlett="'"+str(curlet)+"'"
				letter.setdefault(curlett,rel)
			else:
				print "Not adding~!"

		if (nowltr== 'a' or 'd' or 'q' or 'h' or 'n' or 'p' or 'b' ) and (len(stri) > 1):
			checkadv(stri)
		print curlet,nowltr
		print "is it correct:?"
		opt = input()
		if (opt == 'n'):
			print "which is ur char?"
			new=input()
			letter[curlet] = new
		
		addfile('letters',nowltr)
		nowltr=""	'''	
		
def putpad(strin):
	global curen
	if len(strin)>1:
			for x in lettr:
				if x == '|':
					findlet(curen,stri)
					curen = ""
				else:
					curen= curen+x
	
#Drawing				
def readpad(seqnc):
	global mos
	mos=pickle.loads(seqnc)
	for i in range(0,len(mos)-4,2):
		if((mos[i]>mos[i+2]) and (mos[i+1] <= mos[i+3])):
			if (lettr[len(lettr) - 1 ] != 'ld'):
				lettr.append('ld')
		elif ((mos[i]<mos[i+2]) and (mos[i+1] <= mos[i+3])):
			if (lettr[len(lettr) - 1 ]!='rd'):
				lettr.append('rd')
		elif ((mos[i]<mos[i+2]) and (mos[i+1] >= mos[i+3])):
			if (lettr[len(lettr) - 1 ]!='ru'):
				lettr.append('ru')
		elif ((mos[i]>mos[i+2]) and (mos[i+1] >= mos[i+3])):
			if (lettr[len(lettr) - 1 ]!='lu'):
				lettr.append('lu')
		putpad(mos)       
# Reserve a port for your service.

global s,host,port
s.bind((host, port))        # Bind to the port
s.listen(5)  
print "demo"               # Now wait for client connection.

c, addr = s.accept()     # Establish connection with client.
print 'Got connection from', addr

while True:
   seqnc=c.recv(1024)
   if len(seqnc)>0:
        print seqnc
        readpad(seqnc)
c.close()  


