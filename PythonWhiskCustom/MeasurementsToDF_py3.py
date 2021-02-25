import subprocess, sys
import os
import pickle


def MeasurementsToDataframe(InputPath, **kwargs):

    if 'Env' in kwargs:
        environment  = kwargs.get('Env')
    else:
        environment = 'WhiskPython'

    if 'folder' in kwargs:
        ProgramPath = os.path.dirname( kwargs.get("folder") ) 
    else:
        ProgramPath = os.path.dirname(os.path.abspath("__filename__"))
    

    print(ProgramPath)

    CMD = os.path.join(ProgramPath,"Python2SubCall.cmd")

    python3_command = r"{} {} {} {}".format(CMD,ProgramPath,InputPath,environment)
    print(python3_command)

    process = subprocess.Popen(python3_command.split(), stdout=subprocess.PIPE)

    output, error = process.communicate()  # receive output from the python2 scrip
    output = output.decode().rstrip()
    
    output = InputPath + ".pck"
    print(f" output is : {output} ,  error is : {error}")

    with open(output, 'rb') as f:
        data = pickle.load(f, encoding='latin1')
        return data
    
def RunWhiskOnVideo(InputPath, **kwargs):
    
    if 'folder' in kwargs:
        ProgramPath = os.path.dirname( kwargs.get("folder") ) 
    else:
        ProgramPath = os.path.dirname(os.path.abspath("__filename__"))
    
    
    wiskpath = os.path.join ( os.path.dirname( ProgramPath ), r"Installs\WhiskerTracking-win\bin" )
    
    CMD = os.path.join(ProgramPath,"WhiskCall.cmd")
    
    face = kwargs.get("face", "right") 
    pxmm = kwargs.get("pxmm", 0.025)
    whisk = "-1"
     
    python3_command = f"{CMD} {wiskpath} {InputPath} {face} {pxmm} {whisk}"
    
    
    
    
    process = subprocess.Popen(python3_command, shell=True, stdout=subprocess.PIPE)
    print(f"About to process : {InputPath} with parameters : {face}, {pxmm}, {whisk}")
    print(f"Commande : \n{python3_command}")
    
    for line in iter(process.stdout.readline, b''):  # replace '' with b'' for Python 3
         sys.stdout.write(line)
    
    #output, error = process.communicate()  # receive output from the python2 scrip
    #output = output.decode().rstrip()
    #print(output,error)

    # with open(output, 'rb') as f:
    #     data = pickle.load(f, encoding='latin1')
    #     return data
    
if __name__ == "__main__":
    
    InputPath = r"E:\DATA\BehavioralVideos\Whisker_Video\Whisker_Closeup\Expect_1\Mouse25\200303_VSD2\Mouse25_2020-03-03T11.52.22"
    
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
    
    data = MeasurementsToDataframe(InputPath)
    
    