#importations
from math import sin, cos, radians, pi, sqrt
from direct.gui.OnscreenText import OnscreenText
from direct.showbase.ShowBase import ShowBase
from pandac.PandaModules import *
#montrer le graphe de scene et le taux de rafraichissement
loadPrcFileData("", "want-directtools #t")
loadPrcFileData("", "show-frame-rate-meter #t") # let me see the frames per second
import direct.directbase.DirectStart
import math
from direct.task import Task
from panda3d.core import WindowProperties
global old_pos

props = WindowProperties()
props.setCursorHidden(True) 
base.win.requestProperties(props)
base.setBackgroundColor(0.5,0.6,0.9)

groupeNP = render.attachNewNode("All")

#COFFRE
coffre = render.attachNewNode("chest_node")
body = loader.loadModel('chest')
body.setScale(5,5,5)
body.setPos(80,80,0.001)
body.setH(180)
body.reparentTo(coffre)

#PERSO (Main + camera)
perso = render.attachNewNode("perso")
perso.reparentTo(groupeNP)
lantern = loader.loadModel('lantern')
lantern.setScale(1,1,1)
lantern.reparentTo(camera)
main = loader.loadModel('hand')
main.reparentTo(camera)

#Skysphere
skysphere = loader.loadModel("SkySphere.bam")
skysphere.setBin('background', 1)
skysphere.setDepthWrite(0) 
skysphere.reparentTo(render)


#Positionner la camera.
camera.setPos(0, 0, 12)
#camera.lookAt(1, 1, 0)
camera.reparentTo(perso)
lantern.setY(9)
lantern.setX(2)
lantern.setZ(-2)
lantern.setH(300)
main.setPos(lantern.getX()-0.1, lantern.getY(), lantern.getZ()+0.7)
main.setH(-50)

#lanterne
plight = PointLight('plight')
plight.setColor(VBase4(1, 1, 0.5, 1))
plnp = render.attachNewNode(plight)
plnp.reparentTo(camera)
plnp.setY(9)
plnp.setX(2)
plnp.setZ(-2)
render.setLight(plnp)
#plight.setAttenuation(Point3(0, 0, 0.001))
perso.setPos(-80,-80,0)

persoSphereEnglobante = lantern.getChild(0).getBounds()
center = persoSphereEnglobante.getCenter()
radius = persoSphereEnglobante.getRadius()
radius = radius/3
persoCollisions = CollisionSphere(center, radius)
persoNP = lantern.attachNewNode(CollisionNode('cperso'))
persoNP.node().addSolid(persoCollisions)
persoCollisions2 = CollisionBox((-80,-80,5),2,2,2)
persoNP.node().addSolid(persoCollisions2)



###PLACEMENT DES MURS VIA BOUCLES###
medium_v = [0,1] #id des murs verticaux pour les tourner correctement
small_v = [3,4,6]
giant_v = [0,1,6,7]

walls = render.attachNewNode("walls")
wallsNP = walls.attachNewNode(CollisionNode('cwalls'))
giantwalls = [0 for i in range(0,8)]
giantCollisions = [0 for i in range(0,8)]
centers1 = {0 : [-100,50], 1 : [-100,-50], 2 : [-50,100], 3 : [50,100],4 : [-50,-100],5 : [50,-100],6 : [100,-50],7 : [100,50]}
for i in range(8):
        giantwalls[i] = loader.loadModel('wall_L')
        giantwalls[i].setPos( centers1[i][0], centers1[i][1], -4)
        giantwalls[i].setScale(10 , 10 , 8)
        if i in giant_v :
                giantwalls[i].setH(90)
                giantCollisions[i] =  CollisionBox((centers1[i][0], centers1[i][1], 5),5,60,10)
                wallsNP.node().addSolid(giantCollisions[i])
        else :
                giantCollisions[i] =  CollisionBox((centers1[i][0], centers1[i][1], 5),60,5,10)
                wallsNP.node().addSolid(giantCollisions[i])
        giantwalls[i].reparentTo(walls)

mediumwalls = [0 for i in range(0,4)]
mediumCollisions = [0 for i in range(0,4)]
centers2 = {0 : [-20,-60], 1 : [20,60], 2 : [60,-60], 3 : [-20,20]}
for i in range(4):
        mediumwalls[i] = loader.loadModel('wall_M')
        mediumwalls[i].setPos( centers2[i][0], centers2[i][1], -4)
        mediumwalls[i].setScale(20 , 10 , 8)
        if i in medium_v :
                mediumwalls[i].setH(90)
                mediumCollisions[i] =  CollisionBox((centers2[i][0], centers2[i][1], 5),5,49,10)
                wallsNP.node().addSolid(mediumCollisions[i])
        else :
                mediumCollisions[i] =  CollisionBox((centers2[i][0], centers2[i][1], 5),49,5,10)
                wallsNP.node().addSolid(mediumCollisions[i])
        mediumwalls[i].reparentTo(walls)


smallwalls = [0 for i in range(0,8)]
smallCollisions = [0 for i in range(0,8)]
centers3 = {0 : [-80,-60], 1 : [-80,-20], 2 : [-80,60], 3 : [-20,80], 4 : [20,0], 5 : [40,20], 6 : [60,0], 7 : [80,60]}
for i in range(8):
        smallwalls[i] = loader.loadModel('wall_S')
        smallwalls[i].setPos( centers3[i][0], centers3[i][1], -4)
        smallwalls[i].setScale(20 , 10 , 8)
        if i in small_v :
                smallwalls[i].setH(90)
                smallCollisions[i] =  CollisionBox((centers3[i][0], centers3[i][1], 5),5,25,10)
                wallsNP.node().addSolid(smallCollisions[i])
        else :
                smallCollisions[i] =  CollisionBox((centers3[i][0], centers3[i][1], 5),25,5,10)
                wallsNP.node().addSolid(smallCollisions[i])
        smallwalls[i].reparentTo(walls)
        
########################################

###Sol
sol1 = loader.loadModel('finalmod')
sol1.setPos(0,0,0)
sol1.setScale(9,9,2)
sol1.reparentTo(groupeNP)
#Le sol 2 sert a simuler un horizon via les trous dans les murs
sol2 = loader.loadModel('finalmod')
sol2.setPos(0,0,-5)
sol2.setScale(200,200,2)
sol2.reparentTo(groupeNP)

### COLLISION HANDLER ###
pusher = CollisionHandlerPusher()
pusher.addCollider(persoNP, perso)
traverser = CollisionTraverser('traverser')
traverser.addCollider(persoNP, pusher)
base.cTrav = traverser


#### TEXTE ####
instructions1 = OnscreenText(text = 'Use ZQSD to move', pos = (0, -0.10), scale = 0.09)
instructions2 = OnscreenText(text = 'Move the mouse to turn the camera', pos = (0, -0.20), scale = 0.09)
instructions3 = OnscreenText(text = "Hold 'echap' to pause", pos = (0, -0.30), scale = 0.09)
instructions4 = OnscreenText(text = 'Please enlarge the screen for a better experience :)', pos = (0, -0.40), scale = 0.09)
objective_text = OnscreenText(text = 'Find the treasure chest !', pos = (0, 0.5), scale = 0.12)
lost = OnscreenText(text = 'LOST', pos = (0, 0), scale = 0.6)
lost.hide()

keyMap = {"z" : False, "q" : False, "s" : False, "d" : False, "collision" : False}
tools = {"escape": False, "pause_text" : False, "lose": False, "win":True}

def setKeys(button, boole):
        keyMap[button] = boole

def setTools(button, boole):
                tools[button] = boole

def collisionEvenement(message):
        setKeys("collision", True)

def collisionEvenement2(message):
        setKeys("collision", False)

def skysphereTask(task):
    skysphere.setPos(base.camera, 0, 0, 0)
    return task.cont

def light_animation(task):
        time = task.time
        if time == 0 :
                return task.cont
        timerad = radians(time*200)
        parameterR = sin(timerad)*5*5
        #Animer la lumiere pour donner l'impression d'une flamme
        if int(time)%6 == 0:
                time2 = radians(time*400)
        elif int(time)%10 == 0:
                time2 = radians(time*300)
        elif int(time)%9 == 0:
                time2 = radians(time*900)
        elif int(time)%2 == 0:
                time2 = radians(time*200)
        else :
                time2 = radians(time*500)
                
        red = min(max(abs(cos(time2)),0.75),0.8)
        green = min(max(abs(cos(time2)),0.75),0.8)
        blue = green/2
        plight.setColor(VBase4(red, green, blue, 1))

        if keyMap["z"] or keyMap["s"] :
                lantern.setR(parameterR)
        elif not keyMap["z"] and not keyMap["s"] :
                if lantern.getR() != 0:
                        lantern.setR(lantern.getR()/1.5)
                
        return task.cont
taskMgr.add(light_animation, "Light Animation")

def win_lose(task):
        if tools["lose"] == True:
                counter.hide()
                lost.show()
        return task.cont
taskMgr.add(win_lose, "Win - Lose Events")

#GESTION DES DEPLACEMENTS AVEC ZQSD
def commandMove(task):
        dt = globalClock.getDt()
        if( dt > 0.20): 
                return task.cont
        if tools["escape"] == True :
                return task.cont
        if keyMap["collision"] == False:
            if keyMap["z"] == True :
                    perso.setY(perso, 20*dt)
            if keyMap["s"] == True :
                    perso.setY(perso, -20*dt)
            if keyMap["q"] == True :
                    perso.setX(perso, -20*dt)
            if keyMap["d"] == True :
                    perso.setX(perso, 20*dt)
        return task.cont
taskMgr.add(commandMove, "Move commands")

time = [182]
counter = OnscreenText(text = str(time[0]), pos = (0, 0.80), scale = 0.2, mayChange=1, fg = (1,1,1,1))
def time_counter(task):
        if tools["escape"] == False :
                dt = globalClock.getDt()
                time[0] -= dt
                counter.setText(str(int(time[0])))
        if time[0] <= 0:
                tools["lose"] = True
        return task.cont
taskMgr.add(time_counter, "Time Counter")

pause_text = OnscreenText(text = 'PAUSED', pos = (0, 0.1), scale = 0.4)
#BARRE DE MENU
def other_commands(task):
        time = task.time
        if task.time >= 15 :
                instructions1.hide()
                instructions2.hide()
                instructions3.hide()
                instructions4.hide()
                objective_text.hide()
        if tools["escape"] == True:
                instructions1.show()
                instructions2.show()
                instructions3.show()
                instructions4.show()
                objective_text.show()
                counter.hide()
                wallsNP.show()
                persoNP.show()
                props.setCursorHidden(False)
                base.win.requestProperties(props)
                pause_text.show()
        else :
                if task.time >= 15 :
                        instructions1.hide()
                        instructions2.hide()
                        instructions3.hide()
                        instructions4.hide()
                        objective_text.hide()
                wallsNP.hide()
                if time < 180:
                        counter.show()
                persoNP.hide()
                props.setCursorHidden(True)
                base.win.requestProperties(props)
                pause_text.hide()
        return task.cont
taskMgr.add(other_commands, "Other Commands")
         

#GESTION DE LA CAMERA AVEC LA SOURIS
def mouse_get(task):
        dt = globalClock.getDt()
        if( dt > 0.20): 
                return task.cont
        if tools["escape"] == True :
                return task.cont
        if base.mouseWatcherNode.hasMouse():
                mpos = base.mouseWatcherNode.getMouse()
                
                camH = perso.getH()
                camP = camera.getP()
                
                mousex = -mpos.getX()*25
                mousey = mpos.getY()*25
                perso.setH(camH + mousex)
                if camP + mousey < -90 :
                        camera.setP(-90)
                elif camP + mousey > 90 and camP + mousey < 180 :
                        camera.setP(90)
                else :
                        camera.setP(camP + mousey)
                base.win.movePointer(0, base.win.getXSize() / 2, base.win.getYSize() / 2)
        return task.cont
taskMgr.add(mouse_get, "Mouse")
taskMgr.add(skysphereTask, "SkySphere Task")

base.accept("d", setKeys, ["d", True])
base.accept("q", setKeys, ["q", True])
base.accept("s", setKeys, ["s", True])
base.accept("z", setKeys, ["z", True])
base.accept("d-up", setKeys, ["d", False])
base.accept("q-up", setKeys, ["q", False])
base.accept("s-up", setKeys, ["s", False])
base.accept("z-up", setKeys, ["z", False])
base.accept("escape", setTools, ["escape", True])
base.accept("escape-up", setTools, ["escape", False])
base.accept("cperso-into-cwalls", collisionEvenement)
base.accept("cperso-out-cwalls", collisionEvenement2)

print(taskMgr)

#DIRECTIONNAL LIGHT
lumiereDir = DirectionalLight('LumiereDirectionnelle')
lumiereDir.setColor(VBase4(0.2, 0.2, 0.2, 1))
lumiereDirNP = render.attachNewNode(lumiereDir)
lumiereDirNP.setHpr(90,-50,0)
#Eclairer tout le graphe de scene:
render.setLight(lumiereDirNP)

#AMBIENT LIGHT
alight = AmbientLight('alight')
alight.setColor(VBase4(0.1, 0.1, 0.1, 0.8))
alnp = render.attachNewNode(alight)
render.setLight(alnp)

# Enable the shader generator for the receiving nodes
render.setShaderAuto()

#lancer le graphe de scene
run()
