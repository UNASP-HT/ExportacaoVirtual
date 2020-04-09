import csv
import codecs
import io
import logging
from datetime import datetime


credentials = {}
fileGroup = []
fileEnroll = []

'''
                        Arquivo de configuração
    (Antes do : acontece a identificação do curso se é AD = Administração)

'''
logging.basicConfig(filename='LogPython.log', level=logging.DEBUG)
logger = logging.getLogger(__name__)
try:

    with open('UNASPVIRTUAL.txt', 'r') as f:
        for line in f:
            # nome do grupo é igual ao que se encontra no unasp Virtual
            curso, nameGroup, cursoEad = line.strip().split(':')
            # Cria um vetor de importação
            credentials[curso] = [nameGroup, cursoEad]

    with open('ENROLL.CSV') as csvfile:  # Le arquivo .csv
        readCSV = csv.reader(csvfile, delimiter=',')
        next(readCSV)
        for row in readCSV:
            # Verifica se ele pertence ao grupo do curso EAD CV-MP
            AddLineENROLL = True
            if(row[1] in credentials):
                if(row[3] == 'student' and row[0] != 'delete'):
                    # Nome do grupo que é extraido do arquivo de configuração
                    nameOfGroup = credentials[row[1]][0]
                    # sigla do curso a ser importado extraido ...
                    initialsCourse = credentials[row[1]][1]

                    lineArquivoGroup = "{},{},{},{}".format(
                        row[0], initialsCourse, row[2], nameOfGroup)
                    lineArquivoENROLL = "{},{},{},{}".format(
                        row[0], initialsCourse, row[2], row[3])

                    fileGroup.append(lineArquivoGroup)
                else:
                    AddLineENROLL = False

            else:
                lineArquivoENROLL = "{},{},{},{}".format(
                    row[0], row[1], row[2], row[3])
            # Essa lógica foi feita para não adicionar o DELETE nas inscrições e membros de grupo
            if(AddLineENROLL):
                fileEnroll.append(lineArquivoENROLL)

            # seleciona coluna que tem o código da disciplina e verificar de qual curso
            # o Row[1] e a informação do curso em código como  HT_AD_AC_2A
            # importante que a abreviação do curso deve ficar na segunda posição

    csvfile = "3_group_members.csv"

    with open(csvfile, "w") as text_file:
        text_file.writelines('action,coursekey,userkey,groupkey\n')
        for f in fileGroup:
            text_file.writelines(f+'\n')

    csvfile = "2_ENROLL_Python.csv"

    with open(csvfile, "w") as text_file:
        text_file.writelines('action,coursekey,userkey,rolekey\n')
        for f in fileEnroll:
            text_file.writelines(f+'\n')

    path = 'USERS.CSV'

    # read input file
    with codecs.open(path, 'r', encoding='latin-1') as file:
        lines = file.read()

    # write output file
    with codecs.open('1_UserPython.CSV', 'w', encoding='utf_8_sig') as file:
        file.write(lines)

    logger.debug(str(datetime.today()) + ' - Files successfully ')
except Exception as e:
    logger.error(str(datetime.today()) +
                 ' - Failed to convert files: ' + str(e))
