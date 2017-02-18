#!/usr/bin/python
from subprocess import Popen, call, PIPE
import ast, barnes, os, shutil

def titlecat(track):
    #Is it an episode?
    if len(track['chapter']) > 6:
        print("Episode!")
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
        call(["mpv",'dvdread://'+str(track['ix'])])
        print("Stopped Playing with MPV.")
        option = input("""
        Was that:
            1) An International clip
            2) A Deleted Scene
            3) An Episode extra
            4) A Season extra
            5) Irrelevant (don't keep)
        :""")
        if (option == 1):
            return 'international_clip'
        elif (option == 2):
            return 'deleted_scene'
        elif (option == 3):
            return 'episode_extra'
        elif (option == 4):
            return 'season_extra'
        elif (option == 5):
            return 'irrelevant'
        return 'irrelevent'

def gettitle(title,outdir,name):
    #make directory
    if not os.path.exists(outdir+r'/temp'):
        os.makedirs(outdir+r'/temp')

    #rip title
    call(["dvdbackup",'-t',str(title),'--input=/dev/sr0','--output='+outdir+r'/temp'])
    vobs = []
    for root, dirs, files in os.walk(outdir+r'/temp'):
        for file in files:
            if file.endswith('.VOB'):
                vobs += [os.path.join(root,file)]
    vobs.sort()
    print(vobs)
    dest = open(outdir+r'/'+name+'.VOB','wb')
    for i in vobs:
        shutil.copyfileobj(open(i,'rb'), dest)
    dest.close()
    shutil.rmtree(outdir+r'/temp')

def getlocname(disc,discno,episodes,season,intclipsep,delscenep,t,option):
    if option == 'episode':
        #index?
        index = t['ix']-1
        #find episode info in discs
        episodeinfo = disc['episodes'][index]
        #Create name
        ident = 'S'+'{num:02d}'.format(num=season)+'E'+'{num:02d}'.format(num=episodeinfo['number'])
        name = ident+' - '+episodeinfo['title']
        #Specify location
        loc = 'Episodes/'+name
        return loc, name
    if option == 'international_clip':
        #find offset of episode in disc
        off = intclipsep[discno-1] - episodes.find(discno-1)
        #get episode info
        episodeinfo = disc['episodes'][off]
        ident = 'S'+'{num:02d}'.format(num=season)+'E'+'{num:02d}'.format(num=episodeinfo['number'])
        #get language
        lang = t['audio'][0]['language']
        name = lang
        loc = 'Episodes/'+ident+' - '+episodeinfo['title']+'/International Clips'
        return loc, name
    if option == 'deleted_scene':
        #find offset of episode in disc
        off = intclipsep[discno-1] - episodes.find(discno-1)
        #get episode info
        episodeinfo = disc['episodes'][off]
        ident = 'S'+'{num:02d}'.format(num=season)+'E'+'{num:02d}'.format(num=episodeinfo['number'])

#Get Barnes and noble info
discs, episodes, intclipsep, delscenep = barnes.barnesget(input("Barnes & Noble URL? "))

#Get info from disc as string
process = Popen(["lsdvd","/dev/sr0","-x","-Oy"], stdout=PIPE)
(output, err) = process.communicate()
exit_code = process.wait()

#Parse dictionary from string
dvdinfo = ast.literal_eval(output[8:].decode("utf-8"))

#Disc Info
discno = int(dvdinfo['title'].split('DISC')[1][0])
season = int(dvdinfo['title'].split('_S')[1][0])

#gettitle(1,'./xfilesout','S01E01 - Pilot')
for t in dvdinfo['track']:
    option = titlecat(t)
    if option != 'irrlevent':
        outdir, name = getlocname(discs[discno-1],discno,episodes,season,intclipsep,delscenep,t,option)
        print([outdir,name])
