from glob import glob
from numpy import arange

majors = ('PHY','PHYR','ENGR')
class DataLoader:
    """Class for handling filtering data"""

    def get(self,data,**kwargs):
        '''Retrieves if any query matches kwargs (i.e. or)'''
        Data = []
        for key in kwargs:
            for d in data:
                if kwargs[key] == d[key]:
                    Data.append(d)

        return Data

    def filter(self,data,**kwargs):
        '''Retrieves if all querys match kwargs (i.e. and)'''
        Data = []

        for d in data:
            append = True
            for key in kwargs:
                if kwargs[key] != d[key]:
                    append = False
            if append:
                Data.append(d)

        return Data

    def all(self,data,key):
        # for key in kwargs:
        #     data = [d for d in data ]
        Data = [d[key] for d in data]
        return Data

    def getUnique(self,data,key):
        return list(set(self.all(data,key)))
        # for d in data:
        #     if data.key

def getHeaderIndices(header):
    indices = {
    'iLname' : header.index('LAST_NAME'),
    'iFname' : header.index('FIRST_NAME'),
    'iEmail' : header.index('EMAIL'),
    'iID' : header.index('ID'),
    'iMajor1' : header.index('MAJR_CODE'),
    'iMajor2' : header.index('SEC_MAJOR'),
    'iClass' : header.index('STUDENT_CLASE')
    }
    try:
        iTermID = header.index('Current TERM_CODE_KEY')
    except:
        try:
            iTermID = header.index('TERM_CODE_KEY')
        except:
            print 'Can find Term Code in CSV'
            exit(1)

    try:
        iTerm = header.index('Current TERM_DESC')
    except:
        try:
            iTerm = header.index('TERM_DESC')
        except:
            print 'Can find Term Code in CSV'
            exit(1)


    indices["iTermID"] = iTermID
    indices["iTerm"] =iTerm
    return indices

def codeToTerm(code):
    semestermap = {
        '10':'Fall',
        '20':'Winter',
        '30':'Summer',
        '40':'Summer'
    }

    # pdb.set_trace()
    semester = semestermap[code[-2:]]
    year = code[0:4] if semester != 'Fall' else str(int(code[0:4])-1)
    return semester+year

def readStudentFile(infiles):
    id = []
    students = []
    for inFile in infiles:
        file = glob(inFile)
        f = open(file[0],'rU')
        header = f.readline().split(',')
        indices = getHeaderIndices(header)
        for line in f:
            t = line.split(',')
            tempid = [t[indices['iID']],t[indices['iTermID']]]

            if tempid not in id:
                sc = t[indices['iClass']]
                sc = 'Masters' if sc.lower() == 'masters' or sc.lower() == 'ug degree pending' else sc

                students.append({'id':tempid[0],
                'lastName':t[indices['iLname']],
                'firstName':t[indices['iFname']],
                'email':t[indices['iEmail']],
                'termID':tempid[1],
                'term':t[indices['iTerm']],
                'major1':t[indices['iMajor1']],
                'major2':t[indices['iMajor2']],
                'academicClass':sc,

                })

                id.append(tempid)

    return students
