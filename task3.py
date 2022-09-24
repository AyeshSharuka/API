from fastapi import FastAPI,Path,HTTPException,status,Request
from typing import Optional
import uvicorn
import asyncio
from datetime import datetime
import schedule
import time
  


app=FastAPI()

loc_dict={"LOC_0123_F00" : "Configured,Down,Time" , "LOC_0123_F02":"status2", "LOC_0123_F03":"status3"}
 
direct_data={"LOC_0123_F01":"Time1,Direction1,North1,South1",
             "LOC_0123_F02":"Time2,Direction2,North2,South2",
             "LOC_0123_F03":"Time3,Direction3,North3,South3",
             "LOC_0123_F04":"Time4,Direction4,North4,South4",     
             
           }

status=[]
previous_data=[]




def read_data():
    current_time = datetime.now().strftime("%I:%M %p")
    try:        
        lines=[]
        file='sample_data.txt'
        f = open(file, 'r')
        for line in f:
            y=line.split(",")
            lines.append(y)
        return lines
    except:
        status.append(f"{current_time} : { f'File name >> {file}  not Found!!. Please Check Your File Name'}") 
        raise HTTPException(status_code=400,detail= f'File name >> {file}  not Found!!. Please Check Your File Name')



@app.get("/")
def main( ):
    return "Hello ! To use this app with interface  you can  use 'http://127.0.0.1:8000/docs' "
 
     
                     
@app.get("/Locations")
def locations():
    current_time = datetime.now().strftime("%I:%M %p")
    try:
        lines=read_data()
        for line in lines:
            if line[0]  in loc_dict.keys():
                status=loc_dict[line[0]]

                line.insert(3,status.split(","))

            else:
                line.insert(3,"Unknown Location or Not Configured")
        return (lines)
    except:
        status.append(f'{current_time} : {"Something went wrong with data file Check it again"}')
        raise HTTPException(status_code=400,detail="Something went wrong with data file Check it again")
 
     

@app.get("/Data/{Location_name}")
def Get_Location_DirectionData(Location_name:str=Path(None,description="Enter Valied type of Location name 'LOC_xxxxxxx_Fnn ' ")):
    current_time = datetime.now().strftime("%I:%M %p")
    global gt_loc_nme_out
    gt_loc_nme_out=Location_name
    if Location_name in direct_data.keys():
        previous_data.append(f"{current_time} : {f'Directions related to the  {Location_name} Location Execute Successful!'}")
        return direct_data[Location_name]
    else: 
        
        previous_data.append(f"{current_time} : {f'Directions related to the  {Location_name} Location  Not Found!'}")
        status.append(f"{current_time} : {f'Directions related to the  {Location_name} Location  Not Found!'}")
        raise HTTPException(status_code=404,detail= f'Directions related to the  {Location_name} Location  Not Found!')



@app.get("/PreviousData")
def get_previous():
    current_time = datetime.now().strftime("%I:%M %p")
    if len(previous_data)==0:
        previous_data.append (f"{current_time} : {'Execute Direction data  Search Function Before view Previous_data!!'}")
        status.append (f"{current_time} : {'Execute Direction data  Search Function Before View Previous_data!!'}")
        raise HTTPException(status_code=400,detail='Execute Direction data  Search Function Before view previous Data!!')
    else:
        return previous_data
 
        
    
@app.get("/REST_STATUS")
def catch_error():
    if len(status)!=0:
        return status
    else:
        return "Until Now No bugs  to report "


    
        
# def grab_data_5min():
#     if len(previous_data)==0:
#         return "No Data Found "
#     return Previous_data
     
# schedule.every(5).minutues.do(grab_data_5min)
  
# while True:
#     schedule.run_pending()
#     time.sleep(5)
        
        
        
     

 
     


        
