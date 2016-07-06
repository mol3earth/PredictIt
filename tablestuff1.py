import urllib
# import beautifulsoup4 for html understanding
import bs4
# Import smtplib for the actual sending function
import smtplib
# for scraping
import requests
import json 
from datetime import date,datetime,timedelta

def checkprinttable(weblink,switch):
	webpage = urllib.urlopen(weblink)
	webpage = webpage.read()
	bswebpage = bs4.BeautifulSoup(webpage, "html.parser")
	table = bswebpage.find(lambda tag: tag.name=='table' )
	allrows = table.findAll(lambda tag: tag.name=='tr')
	result =[]
	doheads= switch - 1
	for row in allrows:
		result.append([])
		if doheads == 1:
			allheads = row.findAll('th')
			for head in allheads:
				thestrings = [unicode(s) for s in head.findAll(text=True)]
				thetext = ''.join(thestrings[0])
				result[-1].append(thetext)
				doheads = 0
				
		allcols = row.findAll('td')
		for col in allcols:
			thestrings = [unicode(s) for s in col.findAll(text=True)]
			if thestrings != []:
				thetext = ''.join(thestrings[0])
				result[-1].append(thetext)
			else:
				thetext = '--'
				result[-1].append(thetext)
					
					
	# print whole damn thing...
	if switch == 2:
		for nested_list in result:
			print nested_list[0][0:6],'\t\t',nested_list[1][0:5],'\t'.join(nested_list[2:-1])
	if switch == 1:
		# print only the impoortant columns for pres and cong
		for row in result:
			if len(row) != 0:
				print row[0][0:6],'\t\t',row[1],'\t',row[3]
			
	return result, table
	
def checkifupdate(newtable,currtable,newavg,curravg,texttoprint,GMAIL_USERNAME,recipient,table2send,url):
	updated=0
	
	tabletext = ''
	avgtext = ''
	if len(newtable)>0:
		if len(newtable)!=len(currtable):
			updated=1
			tabletext = ' &  n Polls from ' + str(len(currtable)-2) + ' to ' + str(len(newtable)-2)
		
		else:
			for i in range(1, len(newtable)):
				if newtable[i][0].find(currtable[i][0])!=0:
					updated=1
					tabletext = tabletext + str(newtable[i][0][0:len(newtable[i][0])/2]) 
				elif newtable[i][1].find(currtable[i][1])!=0:
					updated=1
					tabletext = tabletext + str(newtable[i][0][0:len(newtable[i][0])/2]) 
														
					
	
	if newavg!=curravg:
		updated=1
		avgtext = ' avg from ' + str(curravg) + ' to ' + str(newavg)
			
	if updated:			
		email_subject = texttoprint + avgtext + tabletext
		gmailerwTable(email_subject,url,recipient,str(table2send))
	return newavg,newtable

#def findrecentpolls(table,daterange)
	
	#for i in range(1, len(table)):
		#if table[i][1].find()!=0:
			#updated=1
			#tabletext = tabletext + str(newtable[i][0][0:len(newtable[i][0])/2]) 
		#elif newtable[i][1].find(currtable[i][1])!=0:
			#updated=1
			#tabletext = tabletext + str(newtable[i][0][0:len(newtable[i][0])/2]) 
	
	

def findNom(table,name,recipient,url):
	k=0
	curravg = []
	for header in table[0]:
		if header.find(name)!=-1:
			curravg = float(table[1][k])
		k=k+1
	
	if curravg == []:
		email_subject = name + ' has dropped from average!'
		gmailer(email_subject,url,recipient)
	
	return curravg
	
def ishtmlcontentchanged(url,oldhtml,email_subject,recipient):
	go = 0
	html=urllib.urlopen(url)
	newhtml = html.read()
	if newhtml!=oldhtml:
		email_subject = 'AP-Gfk released something'
		gmailer(email_subject,url,recipient)	

	return newhtml
	
def finddate(url,datestr,numoccur,str2email,switch,recipient):
	go=0
	htmlthing = urllib.urlopen(url)
	htmlthing = htmlthing.read()
	if switch == 0: # quinn & monmouth & wapo & wapo2
		if htmlthing.count(datestr)>numoccur: 
			pollupdate = "%s for a total of %s polls" % (str2email,str(numoccur+1))
			go = 1
	elif switch == 1: # ras
		if htmlthing.find(datestr)>numoccur:
			if datestr[0] == 'N':
				idx = htmlthing.find(datestr)
				pollupdate = "%s %s" % (str2email,htmlthing[idx+73:idx+76])
			else:
				pollupdate = "%s %s" % (str2email,htmlthing[7948:7950])
			go = 1
	elif switch == 2:# reut
		if htmlthing.find(datestr)==-1: 
			if url.find('huff'):
				pollupdate = str2email
			elif url.find('reut'):
				pollupdate = "%s %s" % (str2email,htmlthing[44:49])
			go = 1
	elif switch == 3: #gallup
		if htmlthing.count(datestr)>0:
			lc = htmlthing.find(datestr)
			pollupdate = "%s %s" % (str2email,htmlthing[lc+18:lc+27])
			go = 1
	elif switch == 4: # see if num of previous occurrs is same as now
		if htmlthing.count(datestr)!=numoccur: 
			pollupdate = "%s changed from %s to %s" % (str2email,str(numoccur),str(htmlthing.count(datestr)))
			numoccur = htmlthing.count(datestr)
			go = 1
	
	if go:
		pollupdate
		print(pollupdate)
				
		# Send the mail
		gmailer(pollupdate,url,recipient)	
		
		print(pollupdate)
		itwent=1
	else:
		itwent=0
		
	return itwent, numoccur
	
	
# in progress here 
def doordonot(url,datestr,numoccur,str2email,switch,docall,dodocall,numdo,str2print,switchtwo):	
	
	if switchtwo == 0:
		if docall == 1:
			try:
				diditgo=finddate(url,datestr,numdo,str2email,switch)
				numdo += diditgo
			except:
				print str2print
				pass	
				
	elif switchtwo == 1:
		if docall & dodocall:
			try:
				diditgo=finddate(url,datestr,numdo,str2email,switch)
				docall-=diditgo
				if diditgo:
					dodocall=0
			except:
				print str2print
				pass
				
	elif switchtwo == 2:
		if docall == 1:
			try:
				diditgo=finddate(url,datestr,docall,str2email,switch)
				if diditgo:
					numdo += 1
					url = "%s%s" % ('http://www.ipsos-na.com/download/pr.aspx?id=',str(doreutnum2))
			except:
				print str2print
				pass	
				
def gmailerwTable(email_subject,url,recipient,table2send):	
		# make this input? nah
		GMAIL_USERNAME = GmailUname
		
		# for some fun printing to screen
		print '*****************************************************'
		print '         ' + email_subject
		
		print '*****************************************************'
		# do this stuff ...
		session = smtplib.SMTP('smtp.gmail.com', 587)
		session.ehlo()
		session.starttls()
		session.login(GMAIL_USERNAME, GmailPassword)
		# create the headers from specified things, and variables
		
		headers = "\r\n".join(["from: " + GMAIL_USERNAME,
                      "subject: " + email_subject,
                      "to: " + ''.join(recipient), #recipient,
                      "mime-version: 1.0",
                      "content-type: text/html"])
		# body_of_email can be plaintext or html!                    
		content = headers + '\n\n' + url + '\n' + table2send
		# finally send it
		session.sendmail(GMAIL_USERNAME, recipient, content)

def gmailer(email_subject,url,recipient):
	
		# make this input? nah
		GMAIL_USERNAME = GmailUname
		
		# for some fun printing to screen
		print '*****************************************************'
		print '         ' + email_subject
		
		print '*****************************************************'
		# do this stuff ...
		session = smtplib.SMTP('smtp.gmail.com', 587)
		session.ehlo()
		session.starttls()
		session.login(GMAIL_USERNAME, GmailPassword)
		# create the headers from specified things, and variables
		
		headers = "\r\n".join(["from: " + GMAIL_USERNAME,
                      "subject: " + email_subject,
                      "to: " + ''.join(recipient), #recipient,
                      "mime-version: 1.0",
                      "content-type: text/html"])
		# body_of_email can be plaintext or html!                    
		content = headers + '\n\n' + url 
		# finally send it
		session.sendmail(GMAIL_USERNAME, recipient, content)

def findall(p, s):
    '''Yields all the positions of
    the pattern p in the string s.'''
    result = []
    i = s.find(p)
    while i != -1:
		result.append([])
		result[-1] = i
		i = s.find(p, i+1)
    
    return result


def reutipsos_scrap(today,daysago,recipient,switch,oldsamplesize):
	
	# initialize output
	didridgo = 0
	samplesize = 0
	
	# make day a number
	day = today.day
	tomorrow = date.today() + timedelta(1)
	
	# original link
	#weblink = 'http://polling.reuters.com/api/1.4/polling/json/mean?dimension=CP1&timeseries=day&timeseries_columns=bucket-id,bucket-label,low,mean,high,count,weight,count-sum,weight-sum&daterange=20160210-20160222&account=trpoll&auth=1eeb6846e5f8be86'
	# %d : zero padded day of month
	# %m : zero padded month of year
	# %Y : four numeral year
	# %y : zero padded two numeral year
	if switch == 1:
		weblink = "%s%s%s%s%s" % ('http://polling.reuters.com/api/1.4/polling/json/mean?dimension=CP1&timeseries=day&timeseries_columns=bucket-id,bucket-label,low,mean,high,count,weight,count-sum,weight-sum&daterange=',datetime.strftime(daysago,'%Y%m%d'),'-',datetime.strftime(tomorrow,'%Y%m%d'),'&account=trpoll&auth=1eeb6846e5f8be86')
		c_index = 2
		switchsubj = "Reut-Ipsos: Right Direction tracker updated!"
	elif switch == 3:
		weblink = "%s%s%s%s%s" % ('http://polling.reuters.com/api/1.4/polling/json/mean?dimension=CP3&timeseries=day&timeseries_columns=bucket-id,bucket-label,low,mean,high,count,weight,count-sum,weight-sum&daterange=',datetime.strftime(daysago,'%Y%m%d'),'-',datetime.strftime(tomorrow,'%Y%m%d'),'&account=trpoll&auth=1eeb6846e5f8be86')
		c_index = 0
		switchsubj = "Reut-Ipsos: Presidential Approval tracker updated!"
	# everything else is same for both DIR, and PRES
	r = requests.get(weblink,headers={'accept': 'application/xml'})
	a = r.text
	# use loads for strings! (note the trailing 's')
	# load for dict
	a = json.loads(a)
	the_a_keys = a.keys()
	b = a[the_a_keys[1]]
	c = b.items()[3][1]
	# for Country Track:
	# c[0] is wrong direction results, c[1] is don't know, c[2] is RIGHT DIRECTION! (what we want)
	# for Presidential approval: 
	# c[0] is Approve, c[1] is Dissaprove, c[2] is dont know
	d = c[c_index]
	# grab the time series, that is, the plotted values for right direction, with date, mean, min, max, etc
	e = d['timeseries']
	# grab the values, there is some other dicts or whatever we don't want
	f = e['array']
	# grab the date, and convert it to out 
	
	lastdate = datetime.strptime(f[-1][1], '%Y-%m-%d')
	if lastdate.day == day:
		meanval = f[-1][3]
		samplesize = f[-1][-2]
		if samplesize != oldsamplesize:
			email_subject = switchsubj + ' Number is: ' + '%g, with a sample size of %g' % (meanval,samplesize)
			gmailer(email_subject,weblink,recipient)
			if samplesize > 1000:
				didridgo = 1
				print 'Sample size is sufficient'
			else:
				print 'Sample size looks too small, will keep trying'
	return didridgo, samplesize


def RasPlat(today,recipient):
	didgo = 0
	today.strftime('%A, %b')
	s = requests.Session()
	p = s.post("http://www.rasmussenreports.com/user/login/",data={'Login': RasUserName,'Password': RasPassword})
	p=s.get('http://www.rasmussenreports.com/platinum')
	mp = p.content
			# if we find the word of the day, go
	if mp.find(today.strftime('%A, %b'))>0: 
		# find the value 
		bs = bs4.BeautifulSoup(mp)
		table = bs.findAll(lambda tag: tag.name=='table')
		# located here in the secodn table
		allrows = table[1].findAll(lambda tag: tag.name=='tr')
		# located here in column 2 of row 2 of table 2
		col = allrows[1].findAll('td')[1]
		percent = str(col.findAll( text = True)[1]).split()[0]
		# construct the subject	
		email_subject = 'Ras Plat: ' + percent    
		gmailer(email_subject,'http://www.rasmussenreports.com/platinum',recipient)
		didgo = 1
	return didgo	
		
def RasStory(currstorydate,recipient):
	s = requests.Session()
	p = s.post("http://www.rasmussenreports.com/user/login/",data={'Login': RasUserName,'Password': RasPassword})
	p=s.get('http://www.rasmussenreports.com/platinum')
	mp = p.content
	bs = bs4.BeautifulSoup(mp, "html.parser")
	newdate = bs.div.find_all("div")[6].strong
	if currstorydate != newdate:
		storytitle =  bs.div.find_all("div")[6].find_all('a')[4].string[1:-1].encode('utf8')
		email_subject = 'New Ras Story: ' + storytitle    
		gmailer(email_subject,'http://www.rasmussenreports.com/platinum',recipient)
	return newdate
	
def RasDoc(url,recipient):
	DOCposted = 0
	s = requests.Session()
	p = s.post("http://www.rasmussenreports.com/user/login/",data={'Login': RasUserName,'Password': RasPassword})
	p=s.get(url)
	if p.text.find("Module not found") == -1:
		mp = p.content
		bs = bs4.BeautifulSoup(mp, "html.parser")
		email_subject = 'Ras DOC updated: '  + str(bs.find_all('tr')[15].find_all('td')[2].text)   
		gmailer(email_subject,url,recipient)
		DOCposted = 1
	return DOCposted

def findNBC(current,recipient):
	htmlthing = urllib.urlopen("http://www.nbcnews.com")
	bs = bs4.BeautifulSoup(htmlthing,"html.parser")
	newstory = bs.find("div", "media media_default").find('h3').text.encode('utf8')
	if newstory != current:
		storyurl = "http://www.nbcnews.com" + bs.find("div", "media media_default").find("a")['href'].encode('utf8')
		htmlthing = urllib.urlopen(storyurl)
		bs = bs4.BeautifulSoup(htmlthing,"html.parser")
		if bs.text.find('poll'):
			email_subject = 'New NBC Story: ' + newstory    
			gmailer(email_subject,storyurl,recipient)
	return newstory
		
