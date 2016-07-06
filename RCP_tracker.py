#!/usr/bin/env python2
import urllib
# import beautifulsoup4 for html understanding
import bs4
# Import smtplib for the actual sending function
import smtplib
# import time so we can pause
import time
# import random so we can not pause regularly
import random
# 
from tablestuff import checkprinttable,checkifupdate,findNom
import numpy as np
import pickle

GMAIL_USERNAME = # enter an email 
recipient =  # enter some more emails
# first grab the averages you want from tables
# CONG


# cong
f = open('/home/user/PredictIt/CONGtableforpython','r')
CONGtable = pickle.load(f)
f.close()
numCONGpolls = len(CONGtable)
curravgCONG=float(CONGtable[1][3])
# Pres
f = open('/home/user/PredictIt/PREStableforpython','r')
PREStable = pickle.load(f)
f.close()
numPRESpolls = len(PREStable)
curravgPRES=float(PREStable[1][3])
# direction
f = open('/home/user/PredictIt/Dirtableforpython','r')
Dirtable = pickle.load(f)
f.close()
curravgDir = float(Dirtable[1][3])
numDirpolls = len(Dirtable)
startseconds = int(time.time())
# TvC
f = open('/home/user/PredictIt/TvCtableforpython','r')
TvCtable = pickle.load(f)
f.close()
numTvCpolls = len(TvCtable)
currdiffTvC=TvCtable[1][6]

##
f = open('/home/user/PredictIt/ClintonFavorableforpython','r')
ClintonFavorabletable = pickle.load(f)
f.close()
numClintonFavorablepolls = len(ClintonFavorabletable)
currClintonFavorable=float(ClintonFavorabletable[1][3])
##
f = open('/home/user/PredictIt/TrumpFavorableforpython','r')
TrumpFavorabletable = pickle.load(f)
f.close()
numTrumpFavorablepolls = len(TrumpFavorabletable)
currTrumpFavorable=float(TrumpFavorabletable[1][3])


while (startseconds+55) > int(time.time()):
	# Second, compare to prest	
	# RCP CONGRESS CHECK
	result, table = checkprinttable('http://www.realclearpolitics.com/epolls/other/congressional_job_approval-903.html',1)
	curravgCONG,CONGtable = checkifupdate(result,CONGtable,float(result[1][3]),curravgCONG,"RCP CONG has updated",GMAIL_USERNAME,recipient,table,'http://www.realclearpolitics.com/epolls/other/congressional_job_approval-903.html')
	f = open('/home/user/PredictIt//CONGtableforpython','r+')
	pickle.dump(CONGtable,f)
	f.close()
	# RCP CONGRESS END

	# RCP PRESIDENT CHECK	
	result, table = checkprinttable('http://www.realclearpolitics.com/epolls/other/president_obama_job_approval-1044.html',1)
	curravgPRES,PREStable = checkifupdate(result,PREStable,float(result[1][3]),curravgPRES,'RCP Pres has updated',GMAIL_USERNAME,recipient,table,'http://www.realclearpolitics.com/epolls/other/president_obama_job_approval-1044.html')
	f = open('/home/user/PredictIt/PREStableforpython','r+')
	pickle.dump(PREStable,f)
	f.close()
	# RCP RESIDENT end


	# RCP DOC CHECK	
	result, table = checkprinttable('http://www.realclearpolitics.com/epolls/other/direction_of_country-902.html',1)
	curravgDir,Dirtable = checkifupdate(result,Dirtable,float(result[1][3]),curravgDir,'RCP DOC has updated',GMAIL_USERNAME,recipient,table,'http://www.realclearpolitics.com/epolls/other/direction_of_country-902.html')
	f = open('/home/user/PredictIt/Dirtableforpython','r+')
	pickle.dump(Dirtable,f)
	f.close()
	# RCP DOC end
	
	
	# RCP TvC CHECK	
	result, table = checkprinttable('http://www.realclearpolitics.com/epolls/2016/president/us/general_election_trump_vs_clinton-5491.html',2)
	currdiffTvC,TvCtable = checkifupdate(result,TvCtable,(result[1][6]),currdiffTvC,'RCP Trump vs Clinton has updated',GMAIL_USERNAME,recipient,table,'http://www.realclearpolitics.com/epolls/2016/president/us/general_election_trump_vs_clinton-5491.html')
	f = open('/home/user/PredictIt/TvCtableforpython','r+')
	pickle.dump(TvCtable,f)
	f.close()
	# RCP TvC end

	# Clinton Favorable Check 
	result, table = checkprinttable('http://www.realclearpolitics.com/epolls/other/clinton_favorableunfavorable-1131.html',2)
	currClintonFavorable,ClintonFavorabletable = checkifupdate(result,ClintonFavorabletable,float(result[1][3]),currClintonFavorable,'RCP Clinton Fav has updated',GMAIL_USERNAME,recipient,table,'http://www.realclearpolitics.com/epolls/other/clinton_favorableunfavorable-1131.html')
	f = open('/home/user/PredictIt/ClintonFavorableforpython','r+')
	pickle.dump(ClintonFavorabletable,f)
	f.close()
	# Clinton Favorable Check END

	# TRUMP Favorable Check 
	result, table = checkprinttable('http://www.realclearpolitics.com/epolls/other/trump_favorableunfavorable-5493.html',2)
	currTrumpFavorable,TrumpFavorabletable = checkifupdate(result,TrumpFavorabletable,float(result[1][3]),currTrumpFavorable,'RCP Trump Fav has updated',GMAIL_USERNAME,recipient,table,'http://www.realclearpolitics.com/epolls/other/trump_favorableunfavorable-5493.html')
	f = open('/home/user/PredictIt/TrumpFavorableforpython','r+')
	pickle.dump(TrumpFavorabletable,f)
	f.close()
	# TRUMP Favorable Check END
	
	
	time.sleep(15+random.random()*1)
