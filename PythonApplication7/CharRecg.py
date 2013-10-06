codeword =['|']
code=''
word=""
import User_track
import math

letter= {'luldrdrulurdru':'a','luldrdrurdru':'a','ldrdrulurdru':'a','ldrdrurdru':'a','luldrdrurd':'a','rululdrdrululd':'b','ldlururdldlu':'b','rdrurdld':'b','ldrurdldlu':'b','ldrurdld':'b','rdrurdldluld':'b','rdrurdldlu':'y','rululdrurdldlu':'b','ruldrdrulu':'b','rululdrdrululd':'b','ruldrdrululd':'b','ldluldrdru':'c','luldrdru':'c','ldrdru':'c','ldrdruldrd':'d','luldrdruldrdru':'d','luldrdrulurd':'d','rululdrdru':'e','rdrululdrdru':'e','rdrululdrdrulu':'e','ruldrdrululdru':'f','rululdrdrululdru':'f','luldrdruldlu':'g','luldrdrurdldluru':'g','luldrdrurdldluld':'g','ldrdruldlu':'g','luldrdrurdldlu':'g','rululdrdrurdru':'h','ldlururd':'h','ldrurd':'n','rurdru':'n','rululdrurdru':'h','ruldrurd':'h','ld':'i','ldrd':'i','rd':'i','rdld':'i','ruldluru':'j','rurdldluru':'j','ruldlu':'j','ldruldrdru':'k','ldruldlurdru':'k','ldlururdldrdru':'k','rdruldrdru':'k','rdruldrd':'k','rululdrd':'l','ruldluldrdru':'l','rululdrdru':'l','ruldru':'l','rurdrurdrurdld':'m','rurdldlururdrurdru':'m','ldrurdlururdld':'m','rdrurdrurdldru':'m','rdrurdrurd':'m','rdrurdldlururdld':'m','rurdrurdru':'n','rdrurdldrurdru':'n','ruldrurdld':'n','rurdldlururd':'n','rurdldrurdldrdru':'n','rdldrdrurd':'n','rurdldlururdld':'n','luldrdrulu':'o','ldrdrulu':'o','rdrululd':'o','ldrdrululd':'o','lururdld':'p','rulururdldlu':'p','rurdlururdld':'p','rdrulururdldlu':'p','rurdldrurd':'n','ldlururdld':'p','luldrdruldru':'q','luldrdruldru':'q','ldrdrululdru':'q','luldrdrululdrdru':'q','rurdluru':'r','rdldlururd':'r','rululdrdrurdru':'r','rdlururd':'r','rurdldlururd':'r','luldrdrurdldlu':'s','luldrdldlu':'s','rdluldrdldlu':'s','ldrdld':'s','luldrdrurdldlu':'s','luldruldrdru':'t','luldluruldrdrurd':'t','rdrurdru':'u','rurdrurd':'u','rurdrululdrdru':'u','rurdruldrdru':'u','rdru':'v','rdrululdrd':'v','rdrurdru':'w','ldrurdru':'w','rdrurdrulu':'w','rdruldrdrululd':'w','rdldruldrdru':'x','rurdldruldrdru':'x','rdldrurdldrd':'x','rdrurdldluru':'y','rdruldrdldluru':'y','rurdrurdldluru':'y','rurdruldlu':'y','rurdruldru':'y','ruldru':'z','ruldrurd':'z','rurdldrdru':'z','rdldrd':'z'}
def findlet(str):
   global letter
   User_track.screen_draw(str,500,200)
   #print "string "+str
   #print letter[str]
def ptptdist(p0, p1):
		dx = abs(p0[0] - p1[0])
		dy = abs(p0[1] - p1[1])
		return math.sqrt(dx**2 + dy**2 )
def findletter(mos):
    global codeword,word
    if len(mos)>0:
        k=2
        try:
            for i in range(0,len(mos)-4,2):
                            
                if((mos[i]>mos[i+2]) and (mos[i+1] <= mos[i+3])):
                    if (codeword[len(codeword) - 1 ] != 'ld')and (codeword[len(codeword) - 1 ] != 'ru'):
                        codeword.append('ld')
                elif ((mos[i]<mos[i+2]) and (mos[i+1] <= mos[i+3])) :
                    if (codeword[len(codeword) - 1 ]!='rd')and (codeword[len(codeword) - 1 ] != 'lu'):
                        codeword.append('rd')
                elif ((mos[i]<mos[i+2]) and (mos[i+1] >= mos[i+3])):
                    if (codeword[len(codeword) - 1 ]!='ru')and (codeword[len(codeword) - 1 ] != 'ld'):
                        codeword.append('ru')
                elif ((mos[i]>mos[i+2]) and (mos[i+1] >= mos[i+3])):
                    if (codeword[len(codeword) - 1 ]!='lu')and (codeword[len(codeword) - 1 ] != 'rd'):
                        codeword.append('lu')
        except:pass
        if (codeword[-1]) != '|':
            codeword.append('|')
        
        code=putpad(mos,codeword)
    letter_cord = []
def putpad(stri,code):
		curen=""
		if len(code)>1:
				for x in code:
					if x == '|':
						findlet(curen)
						curen = ""
					else:
						curen= curen+x
		return curen