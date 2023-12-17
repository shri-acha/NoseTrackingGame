import pygame,random,math
import pygame.camera,pygame.image
import cv2
pygame.init()
HEIGHT,WIDTH = 800,800
win = pygame.display.set_mode((HEIGHT,WIDTH))
pygame.display.set_caption("Nose Tracking Game")
clock = pygame.time.Clock()
run = True;
nose_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_mcs_nose.xml")

#Camera stuff
camera = cv2.VideoCapture(0)
#end
def randPos():
    posRand = (random.randint(200,600)//50 * 50 ,random.randint(200,600)//50 * 50)
    return posRand;

class Sprite(pygame.sprite.Sprite):
    def __init__(self,healthUser,colorUser,posUser):
        self.healthUser = healthUser
        self.colorUser = colorUser
        self.posUser = posUser
        super().__init__()

    def draw(self,window,nosePos):
        self.posUser = nosePos
        pygame.draw.circle(window,color=self.colorUser,center=nosePos,radius=5)

    def move(self,key):   
        if(key == pygame.K_w):
                self.posUser = (self.posUser[0],self.posUser[1] - 50)
        if(key == pygame.K_s):
            self.posUser = (self.posUser[0],self.posUser[1] +  50)
        if(key == pygame.K_a):
            self.posUser = (self.posUser[0]-50,self.posUser[1])
        if(key == pygame.K_d):
            self.posUser = (self.posUser[0]+50,self.posUser[1])


class nonInteractive:
    def __init__(self,randomPos = (200,200)):
        self.randomPos= randomPos;
        
    def lines(self,win,pos1,pos2,pos3):
        pygame.draw.lines(win,(255,255,255),False,[pos1,pos2,pos3],3)

    def spaceRect(self,win,touch=False):
        if touch:
            self.randomPos = randPos();
        pygame.draw.rect(win,(255,255,255),pygame.Rect((WIDTH/2-self.randomPos[0]/2)//50 * 50,(HEIGHT/2-self.randomPos[1]/2)//50 * 50,self.randomPos[0]//50 * 50,self.randomPos[1]//50 * 50),2)
        return (self.randomPos[0],self.randomPos[1])
class Food:

    def __init__(self,tempVar=tuple(),foodPos=(HEIGHT/2,WIDTH/2)):
        self.foodPos = foodPos;
        self.tempVar = tempVar;

    def randPos(self):
        posRand = (random.randint(WIDTH//2-self.tempVar[0]//2 + 50 ,WIDTH//2 + self.tempVar[0]//2 -50 )//50 * 50,random.randint(HEIGHT//2 - self.tempVar[1]//2 + 50,HEIGHT//2 + self.tempVar[1]//2 - 50 )//50 * 50)
        return posRand;

    def draw(self,window,touch=False):
        if touch == True:
            self.foodPos =self.randPos();
        pygame.draw.circle(window,color=(0,255,255),center=((self.foodPos[0]),(self.foodPos[1])),radius=5) 


snake = Sprite(50,(255,0,0),(HEIGHT/2+50,WIDTH/2+50));
apple = Food();
edge1 = nonInteractive()
edge2 = nonInteractive()
edge3 = nonInteractive()
edge4 = nonInteractive()
spaceRect = nonInteractive()
while (run):
    clock.tick(60)#it's for the fps
    win.fill((0,0,0))#fills with colour everytime it updates
    #camera stuff
    ret,fram = camera.read()
    resized_frame = cv2.resize(fram,(600,600))
    resized_frame =cv2.rotate(resized_frame,cv2.ROTATE_90_COUNTERCLOCKWISE)
    image_surface = pygame.surfarray.make_surface(resized_frame)
    fram = cv2.flip(fram,1)
    frame = cv2.resize(fram, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA)
    gray = cv2.cvtColor(fram, cv2.COLOR_BGR2GRAY)
    nose_rects = nose_cascade.detectMultiScale(gray, 1.3, 5)
    win.blit(image_surface,[100,100])
    #end
    for (x,y,w,h) in nose_rects:
        snake.draw(win,(x//50 * 50+150,y//50 * 50+200))
    edge1.lines(win,(100,200),(100,100),(200,100))
    edge2.lines(win,(100,600),(100,700),(200,700))
    edge3.lines(win,(600,700),(700,700),(700,600))
    edge4.lines(win,(600,100),(700,100),(700,200))


    print(snake.posUser,apple.foodPos,spaceRect.randomPos)
    if(snake.posUser == apple.foodPos):
        apple.tempVar = spaceRect.spaceRect(win,True)
        apple.draw(win,True)
    else:
        apple.tempVar = spaceRect.spaceRect(win)
        apple.draw(win)


    
    
    pygame.display.flip() 
    
    for event in pygame.event.get(): #takes a list and iterates through all the type of event and if any is a type "pygame.QUIT"(yes it is a type of data,when a pygame window is intended to be closed),shuts down the program.
        if event.type == pygame.QUIT:
            run = False   
        if event.type == pygame.KEYDOWN:
            snake.move(event.key)