import subprocess
import pickle
import pandas as pd

import sys, os

GLOBpath = os.path.abspath(__file__)
GLOBdir_path = os.path.dirname(GLOBpath)

def MeasurementsToDataframe(InputPath, **kwargs):

    if 'Env' in kwargs:
        environment  = kwargs.get('Env')
    else:
        environment = 'WhiskPython'

    if 'folder' in kwargs:
        ProgramPath = os.path.dirname( kwargs.get("folder") ) 
    else:
        ProgramPath = GLOBdir_path
    

    print(ProgramPath)

    CMD = os.path.join(ProgramPath,"WhiskMeasure_wrapper.cmd")

    python3_command = r"{} {} {} {}".format(CMD,ProgramPath,InputPath,environment)
    print(python3_command)

    process = subprocess.Popen(python3_command.split(), stdout=subprocess.PIPE)

    output, error = process.communicate()  # receive output from the python2 scrip
    output = output.decode().rstrip()
    
    output = InputPath + "#measurements.pickles"
    print(f" output is : {output} ,  error is : {error}")

    with open(output, 'rb') as f:
        data = pickle.load(f, encoding='latin1')
        return data
		
def WhiskersToDataframe(InputPath, **kwargs):

    if 'Env' in kwargs:
        environment  = kwargs.get('Env')
    else:
        environment = 'WhiskPython'

    if 'folder' in kwargs:
        ProgramPath = os.path.dirname( kwargs.get("folder") ) 
    else:
        ProgramPath = GLOBdir_path
    
    CMD = os.path.join(ProgramPath,"WhiskWhiskers_wrapper.cmd")

    python3_command = r"{} {} {} {}".format(CMD,ProgramPath,InputPath,environment)
    print(python3_command)

    process = subprocess.Popen(python3_command.split(), stdout=subprocess.PIPE)

    output, error = process.communicate()  # receive output from the python2 scrip
    output = output.decode().rstrip()
    
    output = InputPath + "#whiskers.pickles"
    print(f" output is : {output} ,  error is : {error}")
    data = pd.read_pickle(output)
    
    return data
    
def RunWhiskOnVideo(InputPath, **kwargs):
    
    if 'folder' in kwargs:
        ProgramPath = os.path.dirname( kwargs.get("folder") ) 
    else:
        ProgramPath = GLOBdir_path
    
    InputPath = os.path.splitext(InputPath)[0]
    
    
    wiskpath = os.path.join ( ProgramPath, "bin" )
    
    CMD = os.path.join(ProgramPath,"WhiskCMD_wrapper.cmd")
    
    face = kwargs.get("face", "top") 
    pxmm = kwargs.get("pxmm", 0.025)
    whisk = kwargs.get("expectedw", "-1")
     
    python3_command = f"{CMD} {wiskpath} {InputPath} {face} {pxmm} {whisk}"
    
    
    
    
    process = subprocess.Popen(python3_command, shell=True, stdout=subprocess.PIPE)
    print(f"About to process : {InputPath} with parameters : {face}, {pxmm}, {whisk}")
    print(f"Commande : \n{python3_command}")
    
    output, error = process.communicate()  # receive output from the python2 scrip
    output = output.decode().rstrip()
    
    #for line in iter(process.stdout.readline, b''):  # replace '' with b'' for Python 3
    #     sys.stdout.write(line)
    
    #output, error = process.communicate()  # receive output from the python2 scrip
    #output = output.decode().rstrip()
    #print(output,error)

    # with open(output, 'rb') as f:
    #     data = pickle.load(f, encoding='latin1')
    #     return data
    
def LoadVibrissae(InputPath):

    InputPath = os.path.splitext(InputPath)[0]
    measures = MeasurementsToDataframe(InputPath)
    whisks =WhiskersToDataframe(InputPath)
    return MergeWhiskersResults(whisks,measures)

def MergeWhiskersResults(whiskers,measure):
        
    dfwhiskers = pd.DataFrame(data=whiskers)
    dfmeasure = pd.DataFrame(data=measure)
    #dfwhiskers.rename(columns={'time':  'frame'}, inplace = True)
    #dfmeasure.rename(columns={'label':  'TEST'}, inplace = True)
    #display(dfwhiskers)
    
    merged = pd.concat([dfwhiskers, dfmeasure], axis = 1)
    #newindex2 = merged.index.rename(('time',  'id'), inplace = True)
    #merged.set_index(newindex2, inplace = True)
    
    merged.index.rename(('time',  'id'),inplace = True)#.reset_index(inplace = True)
    #display(merged)
    #merged.set_index(('time',  'id'), inplace = True)
    return merged
    
if __name__ == "__main__":
    
    InputPath = r"C:\Users\Timothe\Desktop\Testzone\Mouse29_2020-06-25T10.47.48"
    
    #RunWhiskOnVideo(InputPath)
        
    # ProgramPath = r"C:\Users\Timothe\NasgoyaveOC\Professionnel\TheseUNIC\Scripts\Python\Librairies_Tim\LibrairieWhisk\PythonWhiskCustom"
    # wiskpath = r"C:\Users\Timothe\NasgoyaveOC\Professionnel\TheseUNIC\Scripts\Python\Librairies_Tim\LibrairieWhisk\Installs\WhiskerTracking-win\bin"
    # 
    # face = "right"
    # pxmm = "0.025"
    # whisk = "-1"
    # CMD = os.path.join(ProgramPath,"WhiskCall.cmd")
    
    # python3_command = f"{CMD} {wiskpath} {InputPath} {face} {pxmm} {whisk}"

    # #process = subprocess.Popen(python3_command.split(), shell=False, stdout=subprocess.PIPE)
    # process = subprocess.Popen(python3_command, shell=True, stdout=subprocess.PIPE)
    
    # for line in iter(process.stdout.readline, b''):  # replace '' with b'' for Python 3
    #     sys.stdout.write(line)
    
    #output, error = process.communicate()
    #print(output,error)
    
    #RunWhiskOnVideo(InputPath)
    
    measures = MeasurementsToDataframe(InputPath)
    whiskers = WhiskersToDataframe(InputPath)
    
    