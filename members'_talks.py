# -*- coding: utf-8 -*-
"""members'_talks.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1VKZbDBTvzlR_VMcQmu_H2fQA5dC58j6y
"""

# import libraries
import mysql.connector
import sshtunnel
import pandas as pd
import numpy as np
import random
import time
from datetime import datetime, timedelta, time

# connect to mysql events table
sshtunnel.SSH_TIMEOUT = 5.0
sshtunnel.TUNNEL_TIMEOUT = 5.0

with sshtunnel.SSHTunnelForwarder(
    ('ssh.pythonanywhere.com'),
    ssh_username='Gymlab', ssh_password='B@s3C@mp!',
    remote_bind_address=('Gymlab.mysql.pythonanywhere-services.com', 3306)
) as tunnel:
    connection = mysql.connector.connect(
        user='Gymlab', password='B@s3C@mp!',
        host='127.0.0.1', port=tunnel.local_bind_port,
        database='Gymlab$pydb',
    )
    
    table = pd.read_sql('SELECT * FROM events', connection)
    
    connection.close()

# load events table remove null ids
table = table.dropna(how='any', subset=['member_id'])

# sort by check_in_timestamp - drop duplicate rows
table = table.sort_values('check_in_timestamp')
table = table.drop_duplicates(subset='check_in_timestamp', keep='first')

# convert timestamps to datetime
lst1 = []
lst2 = []
for timestamp in table.check_in_timestamp.values:
    newtime = timestamp + 60 * 60
    check_in = pd.Timestamp(timestamp,unit='s')
    check_out = pd.Timestamp(newtime,unit='s')
    lst1.append(check_in)
    lst2.append(check_out)
lst1 = np.asarray(lst1)
lst2 = np.asarray(lst2)

# dataframe containing member_id,date,check_in/out time
table['check_in'] = lst1
table['check_out'] = lst2
table = table[['member_id','check_in','check_out']]
table.member_id = table.member_id.values.astype(np.int64)
table = table.reset_index(drop=True)

# connect to mysql data_coach_availability table
sshtunnel.SSH_TIMEOUT = 5.0
sshtunnel.TUNNEL_TIMEOUT = 5.0

with sshtunnel.SSHTunnelForwarder(
    ('ssh.pythonanywhere.com'),
    ssh_username='Gymlab', ssh_password='B@s3C@mp!',
    remote_bind_address=('Gymlab.mysql.pythonanywhere-services.com', 3306)
) as tunnel:
    connection = mysql.connector.connect(
        user='Gymlab', password='B@s3C@mp!',
        host='127.0.0.1', port=tunnel.local_bind_port,
        database='Gymlab$pydb',
    )
    
    coach_availability = pd.read_sql('SELECT * FROM data_coach_availability', connection)
    
    connection.close()

# load coach_availability table
coach_availability = coach_availability

# develop talks_table
memberlist = []
newmemberlist = []
startlist = []
endlist = []
titlelist = []
start_time = datetime(2019,2,1,0,0,0) 
end_time = datetime(2019,2,28,0,0,0)
new_dt = coach_availability.start_dt > start_time
index_first_time_available = new_dt.values.argmax()
first_time_available = coach_availability.start_dt[index_first_time_available]
while first_time_available <= end_time:
    x = first_time_available >= table.check_in
    y = first_time_available <= table.check_out
    index_possible_members = np.where(x==y)
    possible_members = table.values[index_possible_members]
    start_talk_dt = first_time_available
    end_talk_dt = start_talk_dt + timedelta(minutes=10)
    if possible_members.shape[0] != 0:
        random_member = random.choice(possible_members)
        if random_member[0] not in memberlist:
            if start_talk_dt.date().weekday() in range(0,5):
                if ((start_talk_dt.time() >= time(9,0,0) and start_talk_dt.time() <= time(10,50,0)) or (start_talk_dt.time() >= time(18,0,0) and start_talk_dt.time() <= time(20,50,0))):
                    memberlist.append(random_member[0])
                    startlist.append(start_talk_dt)
                    endlist.append(end_talk_dt)
                    titlelist.append('talk')
                elif ((start_talk_dt.time() <= time(9,0,0) or start_talk_dt.time() >= time(10,50,0)) or (start_talk_dt.time() <= time(18,0,0) or start_talk_dt.time() >= time(20,50,0))):
                    memberlist.append(str(random_member[0])+' !')
                    startlist.append(start_talk_dt)
                    endlist.append(end_talk_dt)
                    titlelist.append('not working')
            elif start_talk_dt.date().weekday() in range(5,7):
                if (start_talk_dt.time() >= time(9,0,0) and start_talk_dt.time() <= time(11,50,0)):
                    memberlist.append(random_member[0])
                    startlist.append(start_talk_dt)
                    endlist.append(end_talk_dt)
                    titlelist.append('talk')
                elif (start_talk_dt.time() <= time(9,0,0) or start_talk_dt.time() >= time(11,50,0)):
                    memberlist.append(str(random_member[0])+' !')
                    startlist.append(start_talk_dt)
                    endlist.append(end_talk_dt)
                    titlelist.append('not working')
        else:
            if start_talk_dt.date().weekday() in range(0,5):
                if ((start_talk_dt.time() >= time(9,0,0) and start_talk_dt.time() <= time(10,50,0)) or (start_talk_dt.time() >= time(18,0,0) and start_talk_dt.time() <= time(20,50,0))):
                    memberlist.append(random_member[0])
                    startlist.append(start_talk_dt)
                    endlist.append(end_talk_dt)
                    titlelist.append('already talked')
                elif ((start_talk_dt.time() <= time(9,0,0) or start_talk_dt.time() >= time(10,50,0)) or (start_talk_dt.time() <= time(18,0,0) or start_talk_dt.time() >= time(20,50,0))):
                    memberlist.append(str(random_member[0])+' !')
                    startlist.append(start_talk_dt)
                    endlist.append(end_talk_dt)
                    titlelist.append('not working')
            elif start_talk_dt.date().weekday() in range(5,7):
                if (start_talk_dt.time() >= time(9,0,0) and start_talk_dt.time() <= time(11,50,0)):
                    memberlist.append(random_member[0])
                    startlist.append(start_talk_dt)
                    endlist.append(end_talk_dt)
                    titlelist.append('already talked')
                elif (start_talk_dt.time() <= time(9,0,0) and start_talk_dt.time() >= time(11,50,0)):
                    memberlist.append(str(random_member[0])+' !')
                    startlist.append(start_talk_dt)
                    endlist.append(end_talk_dt)
                    titlelist.append('not working')
    else:
        if start_talk_dt.date().weekday() in range(0,5):
            if ((start_talk_dt.time() >= time(9,0,0) and start_talk_dt.time() <= time(10,50,0)) or (start_talk_dt.time() >= time(18,0,0) and start_talk_dt.time() <= time(20,50,0))):  
                memberlist.append('no member available')
                startlist.append(start_talk_dt)
                endlist.append(end_talk_dt)
                titlelist.append('wait')
            elif ((start_talk_dt.time() <= time(9,0,0) or start_talk_dt.time() >= time(10,50,0)) or (start_talk_dt.time() <= time(18,0,0) or start_talk_dt.time() >= time(20,50,0))):
                memberlist.append('no member available')
                startlist.append(start_talk_dt)
                endlist.append(end_talk_dt)
                titlelist.append('not working')
        elif start_talk_dt.date().weekday() in range(5,7):
            if (start_talk_dt.time() >= time(9,0,0) and start_talk_dt.time() <= time(11,50,0)):
                memberlist.append('no member available')
                startlist.append(start_talk_dt)
                endlist.append(end_talk_dt)
                titlelist.append('wait')
            elif (start_talk_dt.time() <= time(9,0,0) and start_talk_dt.time() >= time(11,50,0)):
                memberlist.append('no member available')
                startlist.append(start_talk_dt)
                endlist.append(end_talk_dt)
                titlelist.append('not working')
    first_time_available = end_talk_dt
memberlist = np.asarray(memberlist)
startlist = np.asarray(startlist)
endlist = np.asarray(endlist)
titlelist = np.asarray(titlelist)
talks_table = pd.DataFrame()
talks_table['member_id'] = memberlist
talks_table['start_dt'] = startlist
talks_table['end_dt'] = endlist
talks_table['title'] = titlelist

# update talks_table
newmemberlist = []
startlist = []
endlist = []
titlelist = []
for member_id,start,end,title in zip(talks_table.member_id,talks_table.start_dt,talks_table.end_dt,talks_table.title):
    if ' !' in member_id:
        member_id = member_id.replace(' !','')
    newmemberlist.append(member_id)
    startlist.append(start)
    endlist.append(end)
    titlelist.append(title)
newmemberlist = np.asarray(newmemberlist)
startlist = np.asarray(startlist)
endlist = np.asarray(endlist)
titlelist = np.asarray(titlelist)
updated_talks_table = pd.DataFrame()
updated_talks_table['member_id'] = newmemberlist
updated_talks_table['start_dt'] = startlist
updated_talks_table['end_dt'] = endlist
updated_talks_table['title'] = titlelist