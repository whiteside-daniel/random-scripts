from icalendar import Calendar, Event, Alarm, vText, vRecur
from datetime import datetime
import pytz
import tempfile, os
timeZones = ["America/Los_Angeles","America/Phoenix","America/Chicago","America/New_York"]
pickupTimes = [8,19,20]
schedules = ["Standard","Affinity","7-Day"]
for tz in timeZones:
	tzSelect = tz
	for pt in pickupTimes:
		for sc in schedules:
			if(sc == "Standard"):
				dict = {'freq':'weekly','byday':['su','mo','tu','we','th']}
			if(sc == "Affinity"):
				dict = {'freq':'weekly','byday':['su','mo','tu','th','fr']}
			if(sc == "7-Day"):
				dict = {'freq':'weekly','byday':['su','mo','tu','we','th','fr','sa']}
			cal = Calendar()
			cal.add('prodid', '-//My calendar product//mxm.dk//')
			cal.add('version', '2.0')
			event = Event()
			event.add('summary', 'Valet Trash Reminder!')
			event.add('description' , 'Dont forget to put your trash out! After collection, remember to bring your container back inside.  If you experience any issue or have any further questions regarding valet trash pickup, please visit https://collectconnect.zohodesk.com/portal/ for more information.')
			event.add('rrule' , vRecur(dict))
			event.add('dtstart', datetime(2024,3,3,pt,0,0,tzinfo=pytz.timezone(tzSelect)))
			event.add('dtend', datetime(2024,3,3,pt,5,0,tzinfo=pytz.timezone(tzSelect)))
			event.add('dtstamp', datetime(2024,3,3,pt,10,0,tzinfo=pytz.timezone(tzSelect)))
			event.add('url' , 'https://collectconnect.zohodesk.com/portal/')
			event['trigger'] = '-PT15M'
			alarm = Alarm()
			alarm.add('action' , 'DISPLAY')
			alarm.add('description' , 'Valet Trash Reminder!')
			alarm['trigger'] = '-PT15M'
			event.add_component(alarm)
			cal.add_component(event)
			directory = tempfile.mktemp()
			if(pt == 8):
				timeString = '8AM'
			if(pt == 19):
				timeString = '7PM'
			if(pt == 20):
				timeString = '8PM'
			if(tz == "America/Los_Angeles"):
				tzString = 'PCT'
			if(tz == "America/Phoenix"):
				tzString = 'MST'
			if(tz == "America/Chicago"):
				tzString = 'CST'
			if(tz == "America/New_York"):
				tzString = 'EST'
			path = '/var/www/html/ics-files/' +sc+'-'+tzString+'-' +timeString + '.ics'
			f = open(path, 'wb')
			f.write(cal.to_ical())
			f.close()
