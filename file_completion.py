#! /usr/bin/env python3

import json, urllib.request, urllib.error,math,time,sys,subprocess

session = ''
statuses = ['waiting to check','checking','downloading','seeding','stopped']
def sendrequest(b):
	global session;
	try:
		req = urllib.request.Request(url='http://127.0.0.1:9091/transmission/rpc')
		req.add_header('X-Transmission-Session-Id',session)
		req.add_data(b)
		resp = urllib.request.urlopen(req)
		return json.loads(resp.read().decode('utf-8'))
	except urllib.error.HTTPError as e:
		if e.code == 409:
			session = e.info().get('X-Transmission-Session-Id')
			# print('Updated session id to "%s".\nRetrying.'%session)
			return sendrequest(b)
		else:
			raise

unfinished_old = None
completed_old = None
unfinished = None
completed = None
while True:
	j = json.dumps({
		'tag':'232',
		'method':'torrent-get',
		'arguments':{
			'fields':['id','name','status']
		}
	}).encode('utf-8')
	torrents = sendrequest(j)
	current_torrents = []
	unfinished_old = unfinished
	completed_old = completed
	unfinished = []
	completed = []
	if torrents['result']=='success':
		torrents = torrents['arguments']['torrents']
		for torrent in torrents:
			status = statuses[int(math.log(torrent['status'],2))]
			# print('<%d> %s (%s)'%(torrent['id'],torrent['name'],status))
			if status == 'downloading':
				current_torrents.append(torrent['id'])
		if len(current_torrents)>0:
			j = json.dumps({
				'tag':'9393',
				'method':'torrent-get',
				'arguments':{
					'ids':current_torrents,
					'fields':['files']
				}
			}).encode('utf-8')
			files = sendrequest(j)
			if files['result']=='success':
				files = files['arguments']['torrents'][0]['files']
				for file in files:
					done = '**'
					if file['bytesCompleted'] != file['length']:
						done = str(int(100*file['bytesCompleted']/file['length']))
						unfinished.append(file['name'])
					else:
						completed.append(file['name'])
					# print('<%s> %s'%(done,file['name']))
			else:
				pass
				#print(files)
	else:
		pass
		#print(torrents)
	if unfinished_old is not None and completed_old is not None:
		flag = False
		for file in unfinished_old:
			if file in completed:
				flag = True
				subprocess.call(['growlnotify','-n','Transmission Completion','-a','Transmission.app','-m',file,'-t','File completed'])
				# print('\nFINISHED: %s (%s)'%(file,time.strftime('%a, %d %b %Y %H:%M:%S',time.localtime())))
		if not flag:
			pass
			# print('.',end='')
			# sys.stdout.flush()
	time.sleep(2)
