#-*- coding:utf-8 -*-
'''
author : zhaohua 
date : July 17, 2016
discription : A spider used to catch master student's grades.
version : 0.2
python version : 2.7
'''
import urllib
import urllib2
import cookielib
import re
import string
import sys
import getpass
class NwpuGradeSpider:
	'''
	A spider used to catch master student's grades.
	Applyed to old version of system(student entranced before 2016)
	'''
	def __init__(self):
		reload(sys)
		sys.setdefaultencoding('gb2312')
		self.loginUrl1 = 'http://222.24.211.70:7001/grsadmin/jsp/studentLogin_DoctorHelper.jsp'
		self.loginUrl2 = 'http://222.24.211.70:7001/grsadmin/servlet/studentLogin'
		self.resultUrl = 'http://222.24.211.70:7001/grsadmin/servlet/studentMain'
		self.postDataViewGrade = urllib.urlencode({
			'MAIN_TYPE': '3',
			'MAIN_SUB_ACTION': 'LL',
			'MAIN_NEXT_ACTION': '',
			'MAIN_PURPOSE': '/jsp/student_JhBrow.jsp'
		})

		self.cookie = cookielib.CookieJar()    
		self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cookie)) 
		self.gradeHtml = ''
		self.userName = raw_input('Input your student id :')
		self.password = getpass.getpass('Input your password :')

		self.postDataLogin = urllib.urlencode({
			'TYPE': 'AUTH',
			'glnj': '',
			'USER': self.userName,
			'PASSWORD': self.password,
			'But1.x': '28',
			'But1.y': '5'	
		})

		self.requiredCourseEvg = 0;
		self.electiveCourseEvg = 0;


	def init(self):
		try :
			loginReq1 = urllib2.Request(url = self.loginUrl1, data = self.postDataLogin);
			result = self.opener.open(loginReq1)
			# print result.info()
			loginReq2 = urllib2.Request(url = self.loginUrl2, data = self.postDataLogin);
			result = self.opener.open(loginReq2)
			viewGrageReq = urllib2.Request(url = self.resultUrl, data = self.postDataViewGrade)

		except Exception , he:
			print 'Exception while login....'
			if hasattr(he, 'code'):
				print 'Error code : ', e.code
			if hasattr(he, 'reason'):
				print 'Error reason: ', e.reason
		try : 
			self.gradeHtml = self.opener.open(viewGrageReq).read().decode('gb2312')
		except Exception, ue:
			print 'Exception while getting grades....'
			if hasattr(ue, 'code'):
				print 'Error code : ', e.code
			if hasattr(ue, 'reason'):
				print 'Error reason: ', e.reason
		self.dealGradeHtml(self.gradeHtml)



	def dealGradeHtml(self, html):
		grage_items = re.findall('<TR>.*?<TD width.*?><div.*?>(.*?)</div></TD>.*?<TD width.*?><div.*?>(.*?)</div></TD>.*?<TD width.*?><div.*?>(.*?)</div></TD>.*?<TD width.*?><div.*?>(.*?)</div></TD>.*?<TD width.*?><div.*?>(.*?)</div></TD>.*?<TD width.*?><div.*?>(.*?)</div></TD>.*?<TD width.*?><div.*?>(.*?)</div></TD>.*?</TR>', html, re.S)
		reSelectType = r'<font color=red >(.*?)</font>'
		self.grades = []
		for single_grage_line in grage_items:
			gradeLineShow = ''
			grade = []
			for item in single_grage_line :
				item = item.strip()
				selected = re.findall(reSelectType, item, re.S)
				if len(selected) != 0:
					item = selected[0]
				grade.append(item.encode('UTF-8'))
				gradeLineShow = gradeLineShow + ' ' + item
			print gradeLineShow
			self.grades.append(grade)
			# print grade
		self.saveGrades(self.grades)
		self.calAvgGrade(self.grades)

	def saveGrades(self, grades):
		gradeFileName = 'grade_' + self.userName;
		gradeFile = open(gradeFileName, 'wb')
		for grade in grades:
			outputLine = self.align(grade[0], 20) + self.align(grade[1], 20) + self.align(grade[2], 10) + self.align(grade[3], 10) + self.align(grade[4], 10) \
				+ self.align(grade[5], 10) + self.align(grade[6], 10)
			gradeFile.writelines(outputLine + '\n')
		gradeFile.close()

	def calAvgGrade(self, grades) :
		''' 计算平均分 '''
		cntRequiredCourse = 0
		cntElectiveCourse = 0
		sumRequiredGrade = 0
		sumElectiveGrade = 0
		for grade in grades :
			if len(grade[0]) > 6:
				continue
			try :
				curGrade = string.atof(grade[5])
			except Exception, e:
				print grade[1].decode('utf-8') + (' has no score yet.')
			else :
				if grade[2] == '学位必修课':
					# print 'required course : ', grade[1]
					cntRequiredCourse += string.atof(grade[4])
					sumRequiredGrade += curGrade * string.atof(grade[4])
				elif grade[2] == '学位选修课':
					# print 'eletive course : ', grade[1]
					cntElectiveCourse += string.atof(grade[4])
					sumElectiveGrade += curGrade * string.atof(grade[4])
		try :
			self.requiredCourseEvg = sumRequiredGrade / cntRequiredCourse
			self.electiveCourseEvg = sumElectiveGrade / cntElectiveCourse
		except Exception, e:
			print 'Incorrect student id or password!'
			return 


		print 'Weighted average points of required couses is  : ' , self.requiredCourseEvg
		print 'Weighted average points of elective couses is  : ' , self.electiveCourseEvg

	def align(self, inputString, length=0):  
		'''
		汉字对齐
		'''
		if length == 0:
			return inputString
		slen = len(inputString)
		re = inputString
		cnt = 3
		slen /= cnt
		placeholder = '  ' 
		if isinstance(inputString,str):
		 	placeholder = ' '
		else :
			slen 
		 	placeholder = '　'
		while slen < length:
			re += placeholder
			slen += 1
		return re


mNwpuGradeSpider = NwpuGradeSpider()
mNwpuGradeSpider.init()
raw_input('Press any key to exit...')

