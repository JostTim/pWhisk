import os
import pickle
from WhiskReadings import load_measurements

def Measurements_Py2toPickle(InputPath):
    
    
    data = load_measurements(InputPath)
    
    outputpath, outputname = os.path.split(InputPath)
    
    output = os.path.join(outputpath,outputname[0:-13] + ".pck")
    
    f = file(output, 'wb')
    pickle.dump(data, f)
    f.close
    
    print(output)
    return output

if __name__ == "__main__":
    pass
    
    