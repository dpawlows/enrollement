from matplotlib import pyplot as pp
from matplotlib import gridspec
from enrolled import *

plotsdir = 'plots/'
def plotMajorHist(students):
    data = DataLoader()
    terms = data.getUnique(students,'termID')
    terms.sort()
    numbers = []
    fig, ax = pp.subplots()
    width = 0.2
    ind = arange(len(terms))

    i=0
    colors = ['b','y','g']
    rects = []
    gs = gridspec.GridSpec(2,1,height_ratios=[3,1])
    ax0 = pp.subplot(gs[0])

    for major in majors:
        nmajor = []
        for term in terms:
            theseStudents = data.filter(students,termID=term)
            theseStudents = data.get(theseStudents,major1=major,major2=major)
            nmajor.append(len(theseStudents))

        rects.append(ax0.bar(ind+i*width,nmajor,width,color=colors[i]))
        i+=1
        numbers.append(nmajor)

    #Plot a histogram for each major over each term
    ax0.set_xticks(ind + (i*width)/2.)
    ax0.set_xticklabels(["" for term in terms])
    ax0.set_ylabel('Number of Students')
    ax0.legend(rects,majors)

    #Line plot for total students
    ax1 = pp.subplot(gs[1])
    termnumbers = [sum(inum) for inum in zip(*numbers)]
    sterms = [codeToTerm(s) for s in terms]
    ax1.plot(ind+(i*width)/2.,termnumbers,lw=2,color='m')
    ax1.set_xlim([0,max(ind)+1])
    ax1.set_xticks(ind + (i*width/2.))
    ax1.set_xticklabels(sterms)
    ax1.locator_params(axis='y',nbins=4)
    ax1.set_ylabel('Total Students')
    pp.savefig(plotsdir+'plot.png')

    maxstudents = max(termnumbers)

    diff = [(nterm - maxstudents)/float(maxstudents) for nterm in termnumbers]
    print 'Difference from max:\n'
    for iterm in range(len(terms)):
        print '{}: {}%'.format(terms[iterm],round(float(diff[iterm])*100))


inFiles = ['data/2011_2014.csv','data/2015_2016.csv']
students = readStudentFile(inFiles)
plotMajorHist(students)

data = DataLoader()
students = data.getUnique(students,'id')
# students = data.get(students,major1='PHY',major2='PHY',major1='ENGR',major2='ENGR',
    # major1='PHYR',major2='PHYR')
