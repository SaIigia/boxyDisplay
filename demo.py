import pytest, boxydisplay, sys, time, random



# * Boxception - untinended feature
# sA= s.AddBox(78,14,1,1)
# sB=sA.AddBox(76,12,1,1)
# sC=sB.AddBox(74,10,1,1)
# sD=sC.AddBox(72,8,1,1)
# sE=sD.AddBox(70,6,1,1)
# sF=sE.AddBox(68,4,1,1)
# sG=sF.AddBox(66,2,1,1)

# sF.UpdateScreenData(noFlush=True)
# sG.UpdateScreenData(noFlush=True)
# sE.UpdateScreenData(noFlush=True)
# sD.UpdateScreenData(noFlush=True)
# sC.UpdateScreenData(noFlush=True)
# sB.UpdateScreenData(noFlush=True)
# sA.UpdateScreenData(noFlush=True)



# * animate box going through screen
s=boxydisplay.Screen(80,16,'2')
sB=s.AddBox(2, 2, 1, 1)
for i in range(1, 14):
     # Change boxcharacter set type each line
     # blocks=str(random.randint(1,4))
     # s.Blocks=blocks
     # sB.Blocks=blocks
    for j in range(1, 78):
        sB.Position=(j,i)
        s.UpdateScreenData()
        s.DrawScreen()
        time.sleep(0.01)

# * animate dividors going through screen
s=boxydisplay.Screen(80,16,'2')
sDHor=s.AddDividor('hor', yPos=1)
sDVer=s.AddDividor('ver', xPos=1)
s.UpdateScreenData(noFlush=True)
s.DrawScreen()
for i in range(1, 15):
    for j in range(1, 78):
        sDHor.Position=(None, i)
        sDVer.Position=(j, None)
        s.UpdateScreenData()
        s.DrawScreen()
        time.sleep(0.01)
