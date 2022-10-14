from playsound import playsound
import time
import random
from tkinter import *
from tkinter.filedialog import askopenfilename, asksaveasfilename


##setting up the initial pattern
pattern = [['O' for i in range(16)]for i in range(6)]


class Pad(Button):
    def __init__(self,sound,beat, *args, **kwargs):
        """
        :param sound: what sound is this button controlling
        :param beat: what beat is this button on
        :param args: unspecefied number of non key word arguments
        :param kwargs: unspecefied number of key word arguments
        """
        Button.__init__(self, *args, **kwargs)
        self.sound = sound
        self.beat = int(beat)

    def hit(self,sound,beat):
        """
        :param sound: what sound is this playing(taken as an index in reference to the main pattern)
        :param beat: on what beat is this playing(taken as an index in reference to the main pattern)
        """
        if pattern[sound][beat] == 'O':
            pattern[sound][beat] = 'X'
            self.configure(text='X')
            #### activate the light on this beat
            Lights[beat].activate()
            ###check if light is active
            if Lights[beat].is_on() == True:
                Lights[beat].configure(bg='#F58E8E')
        elif pattern[sound][beat] == 'X':
            pattern[sound][beat] = '2'
            self.configure(text='2')
        elif pattern[sound][beat] == '2':
            pattern[sound][beat] = '4'
            self.configure(text='4')
        elif pattern[sound][beat] == '4':
            pattern[sound][beat] = 'A'
            self.configure(text='A')
        elif pattern[sound][beat] == 'A':
            pattern[sound][beat] = 'B'
            self.configure(text='B')
        elif pattern[sound][beat] == 'B':
            pattern[sound][beat] = '?'
            self.configure(text='?')
        elif pattern[sound][beat] == '?':
            pattern[sound][beat] = 'O'
            self.configure(text='O')
            #### deactivate the light on this beat
            Lights[beat].deactivate()
            ###check if light is active
            if Lights[beat].is_on() == False:
                Lights[beat].configure(bg='#FFEA9B')

    def __str__(self):
        return self.sound + str(self.beat)

class Track(Button):
    def __init__(self,name,sound,track, *args, **kwargs):
        """
        :param sound: what sound is this button controlling
        :param beat: what beat is this button on
        :param args: unspecefied number of non key word arguments
        :param kwargs: unspecefied number of key word arguments
        """
        Button.__init__(self, *args, **kwargs)
        self.sound = '1'
        self.track = int(track)
        self.name = str(name)

    def get_sound(self):
        return self.sound
    def change_sound(self,new):
        self.sound = new
    def switch(self):
        if self.get_sound() == '1':
            self.change_sound('2')
            self.configure(text =(self.name+' '+(self.get_sound())))
        elif self.get_sound() == '2':
            self.change_sound('3')
            self.configure(text =(self.name+' '+(self.get_sound())))
        elif self.get_sound() == '3':
            self.change_sound('1')
            self.configure(text =(self.name+' '+(self.get_sound())))

    def __str__(self):
        return self.name

class Light(Label):
    def __init__(self,active,beat, *args, **kwargs):
        """
        :param beat: what beat is this light on
        :param args: unspecefied number of non key word arguments
        :param kwargs: unspecefied number of key word arguments
        """
        super().__init__( *args, **kwargs)
        self.beat = int(beat)
        self.active = False

    def activate(self):
        """
        turns active to true
        """
        self.active = True

    def deactivate(self):
        """
        turns active to false, only if the entire column is empty
        """
        count = 0
        for i in pattern:
            if pattern[count][self.beat] == 'X' or pattern[count][self.beat] == '?'or \
                    pattern[count][self.beat] == '2'or pattern[count][self.beat] == '4'\
                    or pattern[count][self.beat] == 'A' or pattern[count][self.beat] == 'B':
                return
            count += 1
        self.active = False

    def is_on(self):
        """
        :return: returns true if light is active, otherwise returns false
        """
        return self.active

## initializing GUI with TKinter
window = Tk()
window.rowconfigure(0,minsize=500,weight=1)
window.columnconfigure(0,minsize=500,weight=1)
frame = Frame(window,relief=RAISED,bg='#DCDCDC')
frame.grid(row=0,column=0,sticky='ns')
###setting up transport buttons
Start = Button(frame,width=5,height=5,text="Start",command=lambda:start()).grid(row=0,column=7,sticky='ew',padx=0,pady=0)
Loops = Scale(frame,label='Loops',from_=1,to=8,activebackground='#F58E8E')
Loops.grid(row=0,column=6,sticky='ew',padx=0,pady=0)
Speed = Scale(frame,label='Speed',from_=5,to=1,resolution=.5,activebackground='#F58E8E')
Speed.grid(row=0,column=4,columnspan=2,sticky='ew',padx=0,pady=0)



#Save and Open buttons/Functions
Save = Button(frame,width=5,height=5,text="Save",command=lambda:savefileas()).grid(row=0,column=9,sticky='ew',padx=0,pady=0)
Open = Button(frame,width=5,height=5,text="Open",command=lambda:open_file()).grid(row=0,column=10,sticky='ew',padx=0,pady=0)




#setting up instruction labels & FISHLOGO
photo = PhotoImage(file = "Fish.png")
photoimage = photo.subsample(3)
Fish = Label(frame,image=photoimage)
Fish.grid(row=0,column=2,columnspan=2)
X = Label(frame,text='X = Hit')
X.grid(row=0,column=15)
two = Label(frame,text='2 = Double')
two.grid(row=0,column=16)
O = Label(frame,text='O = Rest')
O.grid(row=0,column=14)
Z = Label(frame,text='Z = 50/50')
Z.grid(row=0,column=17)
###Track buttons
Kick = Track('Kick','1',0,frame,width=5,height=5,text="Kick 1",command= lambda :Kick.switch(),highlightbackground='#F58E8E')
Kick.grid(row=2,column=0)
Clap = Track('Clap','1',1,frame,width=5,height=5,text="Clap 1",command= lambda :Clap.switch(),highlightbackground='#F58E8E')
Clap.grid(row=3,column=0)
Hat = Track('Hat','1',2,frame,width=5,height=5,text="Hat 1",command= lambda :Hat.switch(),highlightbackground='#F58E8E')
Hat.grid(row=4,column=0)
Ride = Track('Ride','1',3,frame,width=5,height=5,text="Ride 1",command= lambda :Ride.switch(),highlightbackground='#F58E8E')
Ride.grid(row=5,column=0)
Rim = Track('Rim','1',4,frame,width=5,height=5,text="Rim 1",command= lambda :Rim.switch(),highlightbackground='#F58E8E')
Rim.grid(row=6,column=0)
FX = Track('FX','1',5,frame,width=5,height=5,text="FX 1",command= lambda :FX.switch(),highlightbackground='#F58E8E')
FX.grid(row=7,column=0)
###LIGHTS
Lights = [Light(False,i,frame,width=2,height=3,bg='#FFEA9B',relief=RAISED,) for i in range(16)]
count = 0
for light in Lights:
    light.grid(row=1,column=count +2,sticky='ew',padx=1,pady=1)
    count +=1




def beat(beat,inst,file,substep,seq):
    """
    :param beat: what beat of the pattern are we on
    :param inst: what instrument/track is being played
    :param file: file is used to retrieve the file name for the playsound method
    :param substep: substep is used for the double hit feature and is set to true for the substep step in each beat
    :return:
    """

    if pattern[inst][beat] == 'X'and substep == 1:
        #for 'X' the sound will just play on the first substep
        playsound(file, False)

    if pattern[inst][beat] == '?'and substep == 1:
        #for '?' we will assign x as either 1 or 0 and play the note based on this value
        x = random.randint(0, 1)
        if x == 0:
            playsound(file, False)
    if pattern[inst][beat] == 'A' and seq%2 == 1 and substep == 1:
        playsound(file, False)
    if pattern[inst][beat] == 'B' and seq%2 == 0 and substep == 1:
        playsound(file, False)
    if pattern[inst][beat] == '2'and (substep == 3 or substep==1):
        # for '2' we will play the sound only if it is the first or second step in the beat
        playsound(file, False)
    if pattern[inst][beat] == '4':
        # for '4' we will play the sound on each substep
        playsound(file, False)



def start():
    """
    :return: no return, function is executed by "Start" button as many times as indicated by the "Loop" scale
    at a speed indicated by the "Speed" scale
    """
    def each_beat(i,tracks,substep,seq):
        ###needs work
        count = 0

        for x in tracks:

            beat(i, count, str(x) + str(x.get_sound()) + '.wav', substep, seq)
            count+=1

    tracks = [Kick,Clap,Hat,Ride,Rim,FX]
    seq = 1
    for i in range(Loops.get()):
        for i in range (16):
            each_beat(i,tracks,1,seq)
            time.sleep(.5/Speed.get()/4)
            each_beat(i, tracks, 2, seq)
            time.sleep(.5 / Speed.get() / 4)
            each_beat(i, tracks, 3, seq)
            time.sleep(.5 / Speed.get() / 4)
            each_beat(i, tracks, 4, seq)
            time.sleep(.5 / Speed.get() / 4)
        seq +=1

def open_file():
    """Open a CSV file.
    reads data from the file to update pattern and recreate buttons
    """
    filepath = askopenfilename(
        filetypes=[("CSV Files", "*.csv"), ("All Files", "*.*")]
    )
    if not filepath:
        return
    # read the csv specified by filepath
    with open(filepath, mode="r", encoding="utf-8") as fp:
        p = fp.read(-1)
        count = 0
        inst = 0
        for i in pattern:
            #beat resets after each inst
            beat = 0
            for j in i:
                pattern[inst][beat] = p[count]
                #iterate through characters in the csv
                count+=1
                beat += 1
            ##iterate through the instruments
            inst += 1
        #recreating the buttons to reset X's and O's
        ###open_file continued
        create_buttons('Kicks', Kick, 0)
        create_buttons('Claps', Clap, 1)
        create_buttons('Hats', Hat, 2)
        create_buttons('Rides', Ride, 3)
        create_buttons('Rims', Rim, 4)
        create_buttons('FXs', FX, 5)
        ### check which lights should be activated given the new pattern
        for i in Lights:
            for j in pattern:
                for h in j:
                    if h == 'X' or h == '?' or h == '2'or h == '4'or h == 'A' or h == 'B':
                        i.activate()
                    else:
                        i.deactivate()
                    if i.is_on():
                        i.configure(bg='#F58E8E')
                    else:
                        i.configure(bg='#FFEA9B')
def savefileas():
    """Save the result in the user-selected file."""
    try:
        path = asksaveasfilename(
            filetypes=(("CSV files", "*.csv"), ("All files", "*.*")),
            title="Save as...",
        )
    except:
        return

    with open(path, 'w', newline='') as fp:
        for i in pattern:
            for j in i:
                fp.write(str(j))
        fp.close()
###creating the input buttons
def create_buttons(list,sound,num):
    """
    :param list: this makes the list of pads for the instrument
    :param sound: this is the name the code refers to when creating and updating pad objects
    :param num: this helps us to keep track of which drum sound this is so the buttons are placed correctly in the frame
    and so the proper section of the pattern is affected
    :return: this function creates 16 buttons which act as inputs for a given instruments section of the main pattern
    """
    ###setting up a bunch of identical buttons through iteration for further alteration
    list = [Pad(str(sound),0,frame,width=5,height=5,text="O",relief=RAISED,highlightbackground='white') for i in range(16)]
    count = 0
    for sound in list:
        sound.beat=count
        ## giving each button a different command which triggers the hit method in the Pad class
        sound.configure(command=lambda sound=sound :sound.hit(num,sound.beat))
        #checking the master pattern to determine starting position
        sound.configure(text=pattern[num][count])
        if count%4==0:
            sound.configure(highlightbackground='#FFEA9B')
        elif count%2==0:
            sound.configure(highlightbackground='lightgray')
        ###placing the button on the correct spot within the frame
        sound.grid(row=num+2,column=count+2,sticky='ew',padx=0,pady=0)
        count +=1

##creating the button objects
create_buttons('Kicks',Kick,0)
create_buttons('Claps',Clap,1)
create_buttons('Hats',Hat,2)
create_buttons('Rides',Ride,3)
create_buttons('Rims',Rim,4)
create_buttons('FXs',FX,5)

window.mainloop()




#Lev Roland-Kalb
#last updated: 5/7/2022