# -*- coding: utf-8 -*-
"""
Created on Thu Jun 18 15:35:05 2020


@author: Timothe
"""

from trace import Load_Whiskers
import pandas as pd
import os

def create_multi(df):
    multi= df.set_index(['time', 'id'], inplace=False)
    return multi 
    

def CreateWhiskPickles(path,**kwargs):
    
    wv = Load_Whiskers(path)
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
    name = os.path.basename(path).rstrip(".whiskers") + "#wiskers.pickles"
    print(outfolder,name)
    outpath = os.path.join(outfolder,name)
    result = create_multi(pd.DataFrame(FrameDict).T)
    
    result.to_pickle(outpath)
    
if __name__=='__main__':
    
    path = r'\\157.136.60.11\EqShulz\Timothe\BehavioralVideos\Whisker_Video\Whisker_Topview\Expect_1\Mouse25\200303_VSD2\Mouse25_2020-03-03T11.53.01.whiskers'
    CreateWhiskPickles(path,outfolder = r"C:\Users\Timothe\Desktop\Testzone" )
