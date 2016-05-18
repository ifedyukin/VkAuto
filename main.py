#!/usr/bin/env python
#coding: utf8

#####################################
##      Всё максимально убого      ##
#####################################


#####################################
##            imports              ##
#####################################
import vk
import re
import sys
import time
import random
import urllib
from termcolor import colored

#####################################
##            settings             ##
#####################################
token = 'token'
IdleMsg = 'Ожидание'
BotUn = '@bot'

#####################################
##           dictionary            ##
#####################################
Dictionary = [
				{'сообщение1'     			:['вариант1','вариант2']},
				{'сообщение2'  	   			:['вариант']},
			 ]

#####################################
##              api                ##
#####################################
session = vk.Session(access_token=token)
api = vk.API(session)

#####################################
##            contain              ##
#####################################
def contain(req):
	req = req.lower()
	for page in Dictionary:
		for find in page:
			if ' '+find == req[len(req)-len(find)-1:]:
				result = random.choice(page[find])
				return result
			elif find == req:
				result = random.choice(page[find])
				return result
			else:
				result = 0
			pass
		pass
	return result

#####################################
##           longPoll              ##
#####################################
def longPoll(ChatId):
	get = api.messages.getLongPollServer(use_ssl=0, need_pts=1)
	key = get['key']
	pts = get['pts']
	ts = get['ts']
	server = get['server']
	num = 0
	while num<1:
		print(colored(IdleMsg+'...','yellow'))
		dct = urllib.request.urlopen("http://"+server+"?act=a_check&key="+str(key)+"&ts="+str(ts)+"&wait=25&mode=2").read().decode('utf-8')
		req = eval(dct)
		ts=req['ts']
		try:
			req['updates'][0]
		except IndexError:
			time.sleep(1)
		else:
			for element in req['updates']:
				if element[0]==4 and RawId[0]=='-':
					MsID = element[1]
					MsGet = api.messages.getById(message_ids=MsID)
					MsTxt = MsGet[1]['body']
					try:
						MsGet[1]['fwd_messages']==''
					except KeyError:
						Reply = contain(MsTxt)
						if Reply!=0 and MsGet[1]['out']!=1:
							uid = MsGet[1]['uid']
							sender = api.users.get(user_ids=uid)
							if RawId[0]=='-':
								if element[5]==' ... ':
									chatName='ЛС'
								else:
									chatName=element[5]
									pass
								pass
							print(colored('Пользователь ','magenta')+sender[0]['first_name']+' '+sender[0]['last_name']+colored(' написал ('+chatName+'):','green'))
							print('> '+MsTxt)
							print(colored('Бот ','magenta')+colored('ответил: ','green'))
							print('> '+Reply)
							ChatId = element[3]
							if (ChatId-2000000000>0):
								api.messages.send(chat_id=ChatId-2000000000, message=BotUn+'> '+sender[0]['first_name']+', '+Reply)
								pass
							else: 
								api.messages.send(user_id=ChatId, message=BotUn+'> '+sender[0]['first_name']+', '+Reply)
								pass
							time.sleep(1)
						pass
					pass
					pass
				elif element[0]==4 and element[3]==ChatId:
					MsID = element[1]
					MsGet = api.messages.getById(message_ids=MsID)
					MsTxt = MsGet[1]['body']
					try:
						MsGet[1]['fwd_messages']==''
					except KeyError:
						Reply = contain(MsTxt)
						if Reply!=0 and MsGet[1]['out']!=1:
							uid = MsGet[1]['uid']
							sender = api.users.get(user_ids=uid)
							print(colored('Пользователь ','magenta')+sender[0]['first_name']+' '+sender[0]['last_name']+colored(' написал:','green'))
							print('> '+MsTxt)
							print(colored('Бот ','magenta')+colored('ответил: ','green'))
							print('> '+Reply)
							if RawId[0]=='+':
								api.messages.send(chat_id=ChatId-2000000000, forward_messages=MsID, message=BotUn+'> '+sender[0]['first_name']+', '+Reply)
								pass
							else: 
								api.messages.send(user_id=ChatId, message=BotUn+'> '+sender[0]['first_name']+', '+Reply)
								pass
							time.sleep(1)
						pass
					pass
				pass
			pass
		time.sleep(5)
		pass
	print(req)
	pass

#####################################
##               auth              ##
#####################################
def auth():
	try:
		api.users.get(user_ids=54850767)
	except BaseException:
		print(colored('\nОшибка авторизации!','red'))
		sys.exit()
	else:
		print(colored('Авторизация пройдена!','green'))
		pass

#####################################
##               main              ##
#####################################
try:
	#auth
	auth()
	#input
	RawId = input(colored('Введите ChatID (ID пользователя/+ID чата/- для всех чатов): ','yellow'))
	if RawId[0]=='+':
		ChatId=int(RawId)+2000000000
	elif RawId[0]=='-':
		ChatId = 'ALL'
	else:
		ChatId=int(RawId)
		pass
	#work
	if RawId[0]!='-':
		username=api.users.get(user_ids=ChatId)
		pass
	if RawId[0]!='+' and RawId[0]!='-':
		name = ' ('+username[0]['first_name']+' '+username[0]['last_name']+')'
	else:
		name =' chat'
	print(colored('ID: ','green')+str(ChatId)+name)
	longPoll(ChatId)
	pass
except BaseException:
	print(colored('\nНепредвиденная ошибка!','red'))
	sys.exit()