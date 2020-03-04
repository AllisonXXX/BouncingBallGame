#------------------------------------------------------
#name: Syrine Matoussi, Anushree Goswami, Jingyu(Gin) Chen and Zhengfei Xia
#filename: boucingball.py
#date:12/9/2018
#description:bouncing ball game with multiple levels
#-------------------------------------------------

#importing all the modules we need so that we have access to their functions
from graphics import *
import time
from random import randint
import pygame
pygame.init()
pygame.mixer.music.load("fall.mp3")
pygame.mixer.music.play()

#setting up the width and height of the game's window
WIDTH = 500
HEIGHT = 500

#creating a window for the name with its name, width, and height
win = GraphWin("Final Project---Bouncing Ball Game", WIDTH, HEIGHT)
background = Image(Point(250,250), "ciel.gif")
background.draw(win)
class Failure_message:

    #defining the attributes of the failure message (text, size, style and colour)
    def __init__(self):
        self.message = Text(Point(WIDTH/2, 210), "You Lost...")
        self.message.setSize(30)
        self.message.setStyle("bold italic")
        self.message.setTextColor("Red")

    #drawing the failure message onto the window
    def draw(self, win):
        self.message.draw(win)
        
class Plate:
    #setting the height and width of the plate object
    height=480
    height1=500

    def __init__(self,width,width1):
        #creating the plate: rectangle shape, custom colour
        self.plate = Rectangle(Point(width, self.height1),Point(width1,self.height))
        self.plate.setFill(color_rgb(244,96,108))

    def draw(self,win):
        #drawing the plate onto the window
        self.plate.draw(win)

    def control(self):
        keyboard = win.checkKey()

        #when the user hits the left arrow key, the plate moves to the left
        if keyboard == "Left":
            self.plate.move(-25,0)

        #when the user hits the right arrow key, the plate moves to the right
        elif keyboard == "Right":
            self.plate.move(25,0)

        #when the user hits the escape key, the window closes
        elif keyboard == 27:
            win.close()  

class Ball:

    #setting up the size of the ball
    ball_type = "Blue Ball"
    radius = 12
    x = randint(10,WIDTH-10)
    y = radius
    DeltaX = 3
    DeltaY = 4
    plate = Plate(185,315)

    #creating the ball (circle shape) and colouring it blue
    def __init__(self,plate):
        self.plate = plate
        self.ball = Circle(Point(self.x,self.y),self.radius)
        self.ball.setFill("Blue")

    #drawing the ball onto the window
    def draw(self, win):
        self.ball.draw(win)

    #move function for the ball to move around the window
    def move(self,plate):
        self.plate = plate
        self.ball.move(self.DeltaX, self.DeltaY)

        #variables that hold the X and Y value of the ball at a given point
        xpos = self.ball.getCenter().getX()
        ypos = self.ball.getCenter().getY()

        #if part of the ball goes off the window on the left, right, or top,
        #flip the values around so the ball bounces back
        if (xpos > WIDTH-self.radius or
            xpos < self.radius):
            self.DeltaX = self.DeltaX * -1

        if (ypos > HEIGHT-self.radius-20 or
            ypos < self.radius):
            self.DeltaY = self.DeltaY * -1

        if (ypos == HEIGHT-self.radius-20):
            #if the ball touches the plate, bounce back up
            if (xpos >= plate.plate.getP1().getX() and
                xpos <= plate.plate.getP2().getX()):
                self.DeltaY = self.DeltaY * -1
                if  abs(self.DeltaY)<7:
                    self.DeltaY =self.DeltaY*1.08
                    self.DeltaX =self.DeltaX*1.08             
                
class Bonus:
    def __init__(self, loc):
        """ Takes in a Point(x,y) for loc """

        self.circle = Circle(Point(loc.getX(),loc.getY()),20)
        self.circle.setFill("Pink")
        
        p1 = Point(loc.getX()+20, loc.getY())
        p2 = Point(loc.getX()+35, loc.getY()+20)
        p3 = Point(loc.getX()+35, loc.getY()-20)
        self.tri1 = Polygon(p1, p2, p3)
        self.tri1.setFill("Pink")

        p4 = Point(loc.getX()-20, loc.getY())
        p5 = Point(loc.getX()-35, loc.getY()-20)
        p6 = Point(loc.getX()-35, loc.getY()+20)
        self.tri2 = Polygon(p4, p5, p6) 
        self.tri2 = Polygon(p4, p5, p6)
        self.tri2.setFill("Pink")
        
    def draw(self, win):
        #draws the bonus circle and triangles on the window
        self.circle.draw(win)
        self.tri1.draw(win)
        self.tri2.draw(win)
        
    def undraw(self):
        #removes the bonus circle and triangles from the window
        self.circle.undraw()
        self.tri1.undraw()
        self.tri2.undraw()

class Score:
    current_score = 0
    """Calculte scores"""

    def __init__(self):
        #creates the score label on the top right of the window
        self.scoreLabel = Text(Point(430, 25), ("Score:", self.current_score))
        self.scoreLabel.setSize(20)
        self.scoreLabel.setTextColor("Yellow")     

    def store_score(self):
        #opens the best scores document, writes the new best score onto it, closes it
        file=open("bestscore.txt","a")
        file.write("\n"+str(self.current_score))
        file.close()
        
    def change_score(self, win):
        #opens the best score file as a read-file
        file = open("bestscore.txt","r")
        scores = file.read()

        #splits the data on the file, each on a new line
        score_list = scores.split("\n")

        #adds the current score to the beginning of the list and then closes the file
        self.current_score = int(score_list[-1])
        file.close()

        #score label updated with the current score each time it increases
        self.scoreLabel = Text(Point(430,25), ("Score:", self.current_score))
        self.scoreLabel.setSize(20)
        self.scoreLabel.setTextColor("Yellow")
        self.scoreLabel.draw(win)

    def draw(self, win):
        #drawing the score label onto the window
        self.scoreLabel.draw(win)

    def undraw(self):
        #removing the score label onto the window
        self.scoreLabel.undraw()

    def Bestscore(self):
        #opens the best scores document, writes the new best score onto it, closes it
        file=open("highscore.txt","r")

        #reads the file and then closes it
        score = file.read()
        file.close()

        #stores the highest score value from the file as "best_score"
        best_score = int(score)

        #if the current score is higher than the best score, best score becomes the current score,
        #and the best score is updated and written into the best score file
        if self.current_score > best_score:
           best_score = self.current_score
           new_score=str(best_score)
           file=open("highscore.txt","w")
           file.write(new_score)
           file.close()
        self.scoreLabel = Text(Point(250,250), ("Highest_score:", best_score))
        self.scoreLabel.setSize(20)
        self.scoreLabel.setTextColor("Red")
        self.scoreLabel.draw(win)

class Button1(Rectangle):
    #when the user clicks on the rectangle, it goes to level 1
    def onClick(self):
        level1()
          
class Button2(Rectangle):
    #when the user clicks on the rectangle, it goes to practice mode
    def onClick(self):
        practice()

class Button3(Rectangle):
    #when the user clicks on the rectangle, it goes to level 2
    def onClick(self):
        level2()

class Button4(Rectangle):
    #when the user clicks on the rectangle, it goes to level 3
    def onClick(self):
        level3()    
        
def practice():

    #setting up and then drawing an image onto the window
    background = Image(Point(250,250), "sky.gif")
    background.draw(win)
    name = "blue ball"

    #tells user it's on practice mode:
    levelLabel = Text(Point(250,25), ("Practice mode"))
    levelLabel.setSize(30)
    levelLabel.setTextColor("White")
    levelLabel.draw(win)

    #when the user presses the button, the window switches to the home page
    level1 = False

    #placement of the button and drawing it onto the window
    level1Button = Button1(Point(400, 40), Point(460, 80))
    level1Button.draw(win)
    level1Button_message = Text(Point(430, 60), "Level 1")
    level1Button_message.setSize(20)
    level1Button_message.setTextColor("White")
    level1Button_message.draw(win)

    #creating a plate object and then drawing it onto the window
    plate = Plate(185,315)
    plate.draw(win)

    #creating a ball object and then drawing it onto the window
    ball = Ball(plate)
    ball.draw(win)

    #creating a score object and then drawing it onto the window
    score = Score()
    score.draw(win)

    while True:
        ball.move(plate)
        plate.control()   

        #the user won't lose even the plate doesn't catch the ball and
        #the score will only chaged when the plate catches the ball   
        if (ball.ball.getCenter().getY() == HEIGHT-ball.radius-20):
            if (ball.ball.getCenter().getX() >= plate.plate.getP1().getX() and
                ball.ball.getCenter().getX() <= plate.plate.getP2().getX()):
                    score.undraw()
                    score.current_score += 10
                    score.store_score()
                    score.change_score(win)

        if (level1 == False):
            #Check to see if user clicked somewhere
            mousePt = win.checkMouse()
            if mousePt is not None:
                # Check if their click was within the x range of the button
                if level1Button.getP1().getX() < mousePt.getX():
                    # Check if their click was within the y range of the button
                    if level1Button.getP1().getY() < mousePt.getY() < level1Button.getP2().getY():
                        level1Button.onClick()
                        level1 = True
                    
def level1():
    #deletes all preexisting text
    win.delete("all")

    #setting up and then drawing an image onto the window
    background = Image(Point(250,250), "ciel.gif")
    background.draw(win)

    #creating and drawing the "Level 2!" message on the window 
    message = Text(Point(WIDTH/2, HEIGHT/2), "Level 1!")
    message.setSize(20)
    message.setStyle("bold italic")
    message.setTextColor("White")
    message.draw(win)

    #lets the window "lag" for 1 second
    time.sleep(2.5)

    #deletes all preexisting text
    win.delete("all")

    #setting up and then drawing an image onto the window
    background = Image(Point(250,250), "stars.gif")
    background.draw(win)
    name = "blue ball"

    #display level:
    levelLabel = Text(Point(250,25), ("Level 1"))
    levelLabel.setSize(30)
    levelLabel.setTextColor("White")
    levelLabel.draw(win)

    #creating a plate object and then drawing it onto the window
    plate = Plate(185,315)
    plate.draw(win)

    #creating a ball object and then drawing it onto the window
    ball = Ball(plate)
    ball.draw(win)

    #creating a score object and then drawing it onto the window
    score = Score()
    score.draw(win)

    level1 = False

    while ball.ball.getCenter().getY() <= HEIGHT-20-ball.radius:
        ball.move(plate)
        plate.control()

        #makes sure the failure message appears on the window
        if (ball.ball.getCenter().getY() == HEIGHT - ball.radius-20 and
            (ball.ball.getCenter().getX() < plate.plate.getP1().getX() or
             ball.ball.getCenter().getX() > plate.plate.getP2().getX())):
            ball.ball.move(ball.DeltaX,ball.DeltaY)
            message = Failure_message()
            message.draw(win)
            #display best score:
            score.Bestscore()

            #placement of the button and drawing it onto the window
            level1Button = Button1(Point(200, 270), Point(300, 310))
            level1Button.draw(win)
            level1Button_message = Text(Point(250, 290), "Try Again")
            level1Button_message.setSize(20)
            level1Button_message.setStyle("bold italic")
            level1Button_message.setTextColor("White")
            level1Button_message.draw(win)
            
        #if a part of the ball touches the plate   
        if (ball.ball.getCenter().getY() == HEIGHT-ball.radius-20):
            if (ball.ball.getCenter().getX() >= plate.plate.getP1().getX() and
                ball.ball.getCenter().getX() <= plate.plate.getP2().getX()):

                    #re-draws the score onto the window and updates the current score value (+10 points)
                    score.undraw()
                    score.current_score += 10
                    score.store_score()
                    score.change_score(win)

        # if score is 40, transfer to level 2
        if score.current_score == 60:
            level2()
            break

    while (level1 == False):
        #Check to see if user clicked somewhere
        mousePt = win.checkMouse()
        if mousePt is not None:
            # Check if their click was within the x range of the button
            if level1Button.getP1().getX() < mousePt.getX():
                # Check if their click was within the y range of the button
                if level1Button.getP1().getY() < mousePt.getY() < level1Button.getP2().getY():
                    level1Button.onClick()
                    level1 = True

def level2():
    #insert music
    pygame.mixer.music.load("bts.mp3")
    pygame.mixer.music.play()

    #deletes all preexisting text
    win.delete("all")

    #setting up and then drawing an image onto the window
    background = Image(Point(250,250), "ciel.gif")
    background.draw(win)

    #creating and drawing the "Level 2!" message on the window 
    message = Text(Point(WIDTH/2, HEIGHT/2), "Level 2!"+"\n"+"In this level, you'll be rewarded with extra points"+"\n"+"if the ball hits the candy!"+"\n"+"Candy will disappear after few seconds!")
    message.setSize(20)
    message.setStyle("bold italic")
    message.setTextColor("White")
    message.draw(win)

    #lets the window "lag" for 1 second
    time.sleep(4)

    #deletes all preexisting text
    win.delete("all")

    #setting up and then drawing an image onto the window
    background = Image(Point(250,250), "nature.gif")
    background.draw(win)

    #print level:
    levelLabel = Text(Point(250,25), ("Level 2"))
    levelLabel.setSize(30)
    levelLabel.setTextColor("Pink")
    levelLabel.draw(win)

    #lets the window "lag" for 1 second
    time.sleep(0.5)

    #creating a plate object and then drawing it onto the window
    #creating a ball object and then drawing it onto the window
    plate = Plate(200,300)
    plate.draw(win)
    ball = Ball(plate)
    ball.draw(win)

    #draw the bonus candy
    candy_x = randint(100,400)
    candy_y = randint(100,400)
    candy=Bonus(Point(candy_x,candy_y))
    candy.draw(win)
    numSeconds = 5
    startTime = time.time()

    #creating a score object and then drawing it onto the window
    score = Score()
    score.draw(win)

    level2 = False
    
    while ball.ball.getCenter().getY() <= HEIGHT-20-ball.radius:
        ball.move(plate)
        plate.control()
        
        #makes sure the failure message appears on the window
        if (ball.ball.getCenter().getY() == HEIGHT - ball.radius-20 and
            (ball.ball.getCenter().getX() < plate.plate.getP1().getX() or
             ball.ball.getCenter().getX() > plate.plate.getP2().getX())):
            ball.ball.move(ball.DeltaX,ball.DeltaY)
            message = Failure_message()
            message.draw(win)
            score.Bestscore()

            #placement of the button and drawing it onto the window
            level2Button = Button3(Point(200, 270), Point(300, 310))
            level2Button.draw(win)
            level2Button_message = Text(Point(250, 290), "Try Again")
            level2Button_message.setSize(20)
            level2Button_message.setStyle("bold italic")
            level2Button_message.setTextColor("White")
            level2Button_message.draw(win)

        #if a part of the ball touches the plate   
        if (ball.ball.getCenter().getY() == HEIGHT-ball.radius-20):
            if (ball.ball.getCenter().getX() >= plate.plate.getP1().getX() and
                ball.ball.getCenter().getX() <= plate.plate.getP2().getX()):

                    #re-draws the score onto the window and updates the current score value (+10 points)
                    score.undraw()
                    score.current_score += 10
                    score.store_score()
                    score.change_score(win)
     
        if (time.time()-numSeconds <= startTime):
            if ((candy_y-20 <= ball.ball.getCenter().getY() <= candy_y+20) and
                (candy_x-55 <= ball.ball.getCenter().getX() <= candy_x+55)):
                candy.undraw()
                score.undraw()
                score.current_score += 2
                score.store_score()
                score.change_score(win)

        if (time.time()-numSeconds > startTime):
            candy.undraw()

        if score.current_score >= 80:
            level3()
            break

    while (level2 == False):
        #Check to see if user clicked somewhere
        mousePt = win.checkMouse()
        if mousePt is not None:
            # Check if their click was within the x range of the button
            if level2Button.getP1().getX() < mousePt.getX():
                # Check if their click was within the y range of the button
                if level2Button.getP1().getY() < mousePt.getY() < level2Button.getP2().getY():
                    level2Button.onClick()
                    level2 = True

def level3():
    #insert music
    pygame.mixer.music.load("exo.mp3")
    pygame.mixer.music.play()
    
    win.delete("all")

    background = Image(Point(250,250), "ciel.gif")
    background.draw(win)

    message = Text(Point(WIDTH/2, HEIGHT/2), "Level 3!"+"\n"+"Please try your best to hold two balls with the plate!")
    message.setSize(20)

    message.setStyle("bold italic")
    message.setTextColor("White")
    message.draw(win)

    time.sleep(3)
    win.delete("all")

    background = Image(Point(250,250), "winter.gif")
    background.draw(win)

    #print level:
    levelLabel = Text(Point(250,25), ("Level 3"))
    levelLabel.setSize(30)
    levelLabel.setTextColor("Blue")
    levelLabel.draw(win)

    time.sleep(0.5)

    plate = Plate(185,315)
    plate.draw(win)

    #create two balls for users to play
    ball_1 = Ball(plate)
    ball_1.ball.setFill("Red")
    ball_1.DeltaX = 8
    ball_1.DeltaY = 6
    ball_1.x = randint(100,300)
    ball_1.draw(win)
    ball_2 = Ball(plate)
    ball_2.x = randint(300,400)
    ball_2.ball.setFill("Yellow")
    ball_2.draw(win)
                   
    score = Score()
    score.draw(win)

    level3 = False

    #if one ball falls down the screen, then the user loses
    while ((ball_1.ball.getCenter().getY() <= HEIGHT-20-ball_1.radius) and
           (ball_2.ball.getCenter().getY() <= HEIGHT-20-ball_2.radius)):
        ball_1.move(plate)
        ball_2.move(plate)
        plate.control()

        if (ball_1.ball.getCenter().getY() == HEIGHT - ball_1.radius-20):
            if (ball_1.ball.getCenter().getX() < plate.plate.getP1().getX() or
                ball_1.ball.getCenter().getX() > plate.plate.getP2().getX()):
                ball_1.ball.move(ball_1.DeltaX, ball_1.DeltaY)
                message = Failure_message()
                message.draw(win)
                score.Bestscore()

                #placement of the button and drawing it onto the window
                level3Button = Button4(Point(200, 270), Point(300, 310))
                level3Button.draw(win)
                level3Button_message = Text(Point(250, 290), "Try Again")
                level3Button_message.setSize(20)
                level3Button_message.setStyle("bold italic")
                level3Button_message.setTextColor("Blue")
                level3Button_message.draw(win)
       
        if (ball_2.ball.getCenter().getY() == HEIGHT - ball_2.radius-20):
            if (ball_2.ball.getCenter().getX() < plate.plate.getP1().getX() or
                ball_2.ball.getCenter().getX() > plate.plate.getP2().getX()):      
                ball_2.ball.move(ball_2.DeltaX, ball_2.DeltaY)
                message = Failure_message()
                message.draw(win)
                score.Bestscore()

                #placement of the button and drawing it onto the window
                level3Button = Button4(Point(200, 270), Point(300, 310))
                level3Button.draw(win)
                level3Button_message = Text(Point(250, 290), "Try Again")
                level3Button_message.setSize(20)
                level3Button_message.setStyle("bold italic")
                level3Button_message.setTextColor("Blue")
                level3Button_message.draw(win)
        
        if (ball_1.ball.getCenter().getY() == HEIGHT-ball_1.radius-20):
            if (ball_1.ball.getCenter().getX() >= plate.plate.getP1().getX() and
                ball_1.ball.getCenter().getX() <= plate.plate.getP2().getX()):
                score.undraw()
                score.current_score += 10
                score.store_score()
                score.change_score(win)

        if (ball_2.ball.getCenter().getY() == HEIGHT-ball_2.radius-20):
            if (ball_2.ball.getCenter().getX() >= plate.plate.getP1().getX() and
                ball_2.ball.getCenter().getX() <= plate.plate.getP2().getX()):
                score.undraw()
                score.current_score += 10
                score.store_score()
                score.change_score(win)

    while (level3 == False):
        #Check to see if user clicked somewhere
        mousePt = win.checkMouse()
        if mousePt is not None:
            # Check if their click was within the x range of the button
            if level3Button.getP1().getX() < mousePt.getX():
                # Check if their click was within the y range of the button
                if level3Button.getP1().getY() < mousePt.getY() < level3Button.getP2().getY():
                    level3Button.onClick()
                    level3 = True
                
def main():
    practice = False
    level1 = False
    level2 = False
    level3 = False
    
    #print instructions:
    instructions = Text(Point(250,250), ("Instructions:"+ "\n"+ "Use arrow keys to move left and right"+ "\n"+ "Click on the buttons in the home page to choose practice mode or levels"+ "\n"+ "Pracrtice mode is to practice your skills"+"\n"+"Enjoy your game"))
    instructions.setSize(16)
    instructions.setTextColor("Black")
    instructions.draw(win)
    time.sleep(5)
    instructions.undraw()
   
    #placement of the buttons and drawing them onto the window
    btn1 = Button1(Point(200,150), Point(300,200))
    btn2 = Button2(Point(200,250), Point(300,300))
    btn1.draw(win)
    btn2.draw(win)

    btn1_message = Text(Point(250, 175), "Level 1")
    btn1_message.setSize(20)
    btn1_message.setTextColor("Black")
    btn2_message = Text(Point(250, 275), "Practice")
    btn2_message.setSize(20)
    btn2_message.setTextColor("Black")

    btn1_message.draw(win)
    btn2_message.draw(win)
    
    while practice == False and level1 == False and level2 == False and level3 == False:
        # Check to see if user clicked somewhere
        mousePt = win.checkMouse()
        if mousePt is not None:

            # Check if their click was within the x range of the button
            if btn1.getP1().getX() < mousePt.getX() < btn1.getP2().getX():

                # Check if their click was within the y range of the button
                if btn1.getP1().getY() < mousePt.getY() < btn1.getP2().getY():
                    btn1.onClick()
                    level1 = True

                elif btn2.getP1().getY() < mousePt.getY() < btn2.getP2().getY():
                    btn2.onClick()
                    practice = True

#call the main function
if __name__ == "__main__":
    main()
