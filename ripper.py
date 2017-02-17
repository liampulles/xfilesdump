#!/usr/bin/python
from subprocess import Popen, PIPE
import ast, barnes

#Get Barnes and noble info
#discs, episodes = barnes.barnesget(input("Barnes & Noble URL? "))

#Get info from disc as string
process = Popen(["lsdvd","/dev/sr0","-x","-Oy"], stdout=PIPE)
(output, err) = process.communicate()
exit_code = process.wait()

#Parse dictionary from string
dvdinfo = ast.literal_eval(output[8:].decode("utf-8"))

#Disc Info
discno = dvdinfo['title'].split('DISC')[1][0]
season = dvdinfo['title'].split('_S')[1][0]

titlecat(dvdinfo['title'][0])

def titlecat(titleset):
    #Is it an episode?
    if len(titleset['chapters']) > 6:
        return 'episode'

    #If not, have user profile:
    #1) International clip (episode)
    #2) Deleted Scene (episode)
    #3) Episode extra
    #4) Season extra
    #5) Irrelevant (don't keep)
    else:
        #Play in mpv
        print("Playing with MPV...")
        Popen(["mpv",'dvd://'+str(titleset['ix'])])
        print("Stopped Playing with MPV.")
        option = input("""
        Was that:
            1) An International clip
            2) A Deleted Scene
            3) An Episode extra
            4) A Season extra
            5) Irrelevant (don't keep)
        :""")
        print(option)
