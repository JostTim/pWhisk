import os
import numpy as np
import pandas as pd
import pickle
#sys.path.append(os.path.dirname(os.path.abspath("__filename__")))

from python import traj, trace


def Measurements_to_Pickle(InputPath):
    
    
    mesureinput = InputPath + ".measurements"
    data = load_measurements(mesureinput)
    
    outputpath, outputname = os.path.split(InputPath)
    
    output = os.path.join(outputpath,outputname + "#measurements.pickles")
    
    f = file(output, 'wb')
    pickle.dump(data, f)
    f.close
    return output



def load_measurements(measure_file):
    """Load measurements, such as curvature.

    The data is taken from traj.MeasurementsTable
    I had to guess at what the columns mean, based on example code in
    features() in python/summary.py

    The ordering of the result does not seem to match the ordering derived
    from *.whiskers. I suspect too-small whiskers are being moved after good
    whiskers. You must use 'frame' and 'wid' to line up with other data.
    For this reason I set the index to be 'frame' and 'wid' in this function.

    0 - "smask"? I think this may be a mask that is applied to filter out
        whiskers that are too small. This seems to affect the ordering of
        the results as well (good whiskers moved before bad).
    1 - frame
    2 - wid
    3 - path_length
    4 - median_score
    5 - the "root angle", I think the angle of a few samples around follicle
    6 - curvature
    7, 8 - follicle x and y
    9, 10 - tip x and y

    measure_file : string
        Path to *.measurements file from measure

    convert_to_int : if True, then convert 'frame' and 'wid' columns to int
    set_index : if True, then set index to ['frame', 'wid']
        Don't do this if you want to maintain the ordering of the columns

    Returns: DataFrame
        Has one row for each whisker segment.
        Columns: smask, frame, wid, path_length, score,
            angle, curv, fol_x, fol_y, tip_x, tip_y
        Then ['frame', 'wid'] are set to be the index (see above)
    """

    # Measurements filename cannot be unicode, for some reason
    tmt = traj.MeasurementsTable(str(measure_file))
    tmt_arr = tmt.asarray()
    tmtdf = pd.DataFrame(tmt_arr,
        columns=['label', 'frame', 'wid', 'length', 'score',
            'angle', 'curvature', 'fol_x', 'fol_y', 'tip_x', 'tip_y'])

    # Convert to float32.
    tmtdf = tmtdf.astype(np.float32)

    # Convert index to int32.
    for col in ['frame', 'wid']:
        tmtdf[col] = tmtdf[col].astype(np.int32)

    # Make index.
    tmtdf = tmtdf.set_index(['frame', 'wid'],
                            verify_integrity=True).sort_index()

    return tmtdf


def CreateWhiskPickles(path,**kwargs):
    
    whiskersinput = path + ".whiskers"
    wv = trace.Load_Whiskers(whiskersinput)
    indxx = ["time","id","x","y","thick","scores"]
    FrameDict = {}
    cnt = 0
    wvkeys = wv.keys()
    for i in wvkeys :
        subkeys = wv.get(i).keys()
        for j in subkeys:
            temp = wv.get(i).get(j)
            temp = [temp.time,temp.id,temp.x,temp.y,temp.thick,temp.scores]
            
            tempframe = pd.Series( temp , index = indxx)
            
            FrameDict.update( [ ( cnt , tempframe ) ] )
            cnt = cnt + 1 
    
    outfolder = kwargs.get( "outfolder" ,os.path.dirname(path))
    name = os.path.basename(path).rstrip(".whiskers") + "#whiskers.pickles"

    outpath = os.path.join(outfolder,name)
    result = create_multi(pd.DataFrame(FrameDict).T)
    result.to_pickle(outpath)
    #print("written pickle at " + outpath)
    
    return outpath

def create_multi(df):
    multi= df.set_index(['time', 'id'], inplace=False)
    return multi 
	
if __name__ == "__main__":
    path = r'\\157.136.60.11\EqShulz\Timothe\BehavioralVideos\Whisker_Video\Whisker_Topview\Expect_1\Mouse25\200303_VSD2\Mouse25_2020-03-03T11.53.01.whiskers'
    CreateWhiskPickles(path,outfolder = r"C:\Users\Timothe\Desktop\Testzone" )