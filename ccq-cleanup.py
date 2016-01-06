from os import mkdir, listdir

INDICATOR = "8"
INDICATOR_INDEX = 72
TYPE = 20
RESPONSE = "1"
INFO = "2"
NAME_START = 40
NAME_LENGTH = 20
CN_START = 63
CN_END = 67
CN_TO_IND_LEN = 4
END_LENGTH = 6
SEMESTER_START = 60
SEMESTER_END = 62

def get_term():
    return raw_input("Input term code: ")

def clean_file(term, filename):
    newFileString = ""
    badIndicators = 0
    badSemesters = 0
    with open(term + "/" + filename) as datfile:
        for line in datfile.readlines():
            if line[TYPE] == RESPONSE:
                newFileString += line
            elif line[TYPE] == INFO:
                newFileString += clean_line(term, line, filename)
                if bad_indicator(line): badIndicators += 1
                if bad_semester(term, line): badSemesters += 1
            else:
                errMsg = 'Sheet type indicator "{}" is invalid'
                raise ValueError(errMsg.format(line[TYPE]))
    return newFileString, badIndicators, badSemesters

def clean_line(term, line, filename):
    check_course_num(line, filename)
    return line[:NAME_START] + " "*NAME_LENGTH + term[1:] + \
           line[CN_START:CN_END+1] + " "*CN_TO_IND_LEN + INDICATOR + \
           " "*END_LENGTH + "\n"

def check_course_num(line, filename):
    
    def print_err(filename, course_num):
        print 'Course number error in file, {}, course number, {}'.format(
            filename, course_num)
        return None
        
    course_num = line[CN_START:CN_END+1]
    first = True
    for c in course_num:
        if first and c not in ["0", "1"]:
            print_err(filename, course_num)
            break
        if c in [" ", "*"]:
            print_err(filename, course_num)
            break
        first = False
    return None

def bad_indicator(line):
    if line[INDICATOR_INDEX] != INDICATOR:
        return True
    else:
        return False

def bad_semester(term, line):
    if line[SEMESTER_START:SEMESTER_END+1] != term[1:]:
        return True
    else:
        return False

def write_cleaned_file(target, filename, fileString):
    with open(target + filename, "w") as datfile:
        datfile.write(fileString + chr(26))
    return None

if __name__ == '__main__':
    term = get_term()
    targetDir = term + "/cleaned/"
    mkdir(targetDir)
    badIndicators = 0
    badSemesters = 0
    for f in listdir(term):
        if f[-4:].upper() != ".DAT":
            continue
        else:
            cleanedFile, bInd, bSem = clean_file(term, f)
            write_cleaned_file(targetDir, f, cleanedFile)
            badIndicators += bInd
            badSemesters += bSem
            
    print "Corrected {} bad indicators and {} bad semester codes.".format(
        badIndicators, badSemesters)
    raw_input("Press ENTER to exit.")
