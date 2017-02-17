#Banres and Noble functions module
import urllib.request

def barnesget(url):
    page = urllib.request.urlopen(url).read().decode("utf-8")

    #start = page.find(r'<h2>Scene Index</h2>')
    #line = page.find(r'<article>',start)
    #endline = page.find(r'</article>',line)
    rawchaps = page.split(r'<h2>Scene Index</h2>')[1].split('<article>')[1].split(r'</article>')[0][1:]
    chapslist = rawchaps.split('<br>')
    chapslist.pop()
    for i in chapslist:
        if i[0] == ' ':
            chapslist[chapslist.index(i)] = i[1:]
            i = i[1:]
        if i.find('[') != -1:
            chapslist[chapslist.index(i)] = i[0:i.find('[')-1]

    rawnames = page.split(r'<h2>Menu</h2>')[1].split('<article>')[1].split(r'</article>')[0][1:]
    nameslist = rawnames.split('<br>')
    nameslist2 = []
    for i in nameslist:
        if i.count(r'&nbsp; &nbsp;') == 1:
            nameslist2.append(i.split(r'&nbsp; &nbsp;')[1])
    nameslist = nameslist2
    #print(nameslist)

    discs = []
    episodes = []
    disc_count = 0
    ep_count = 0
    for i in chapslist:
        if i[0:4] == 'Disc':
            discs.append({'episodes':[]})
            disc_count = len(discs) - 1
        elif i[0:2] == '1.':
            discs[disc_count]['episodes'].append({})
            episodes.append(disc_count)
            ep_count = len(discs[disc_count]['episodes']) - 1
            discs[disc_count]['episodes'][ep_count]['number'] = len(episodes);
            discs[disc_count]['episodes'][ep_count]['title'] = nameslist[len(episodes)-1]
            discs[disc_count]['episodes'][ep_count]['chapters'] = []
            discs[disc_count]['episodes'][ep_count]['chapters'].append(i)
        else:
            discs[disc_count]['episodes'][ep_count]['chapters'].append(i)

    #print(discs)
    return discs, episodes
