
import requests
import json
from datetime import datetime as dt

#Python class to work with a FHIR Patient resource end-point
class Patient:

	def __init__(self, mrn, domain="JHH", url=r"http://jhmw-mig-app-01:9002/epic_query"):
		self.url = url
		payload = {}
		payload['pid'] = mrn
		payload['domain'] = domain

		try:
			r = requests.get(self.url, params=payload)
			patient = r.json()
			
			#Parse FHIR JSON response and assign to our class variables
			self.dob = patient['birthDate']
			self.family = patient['name']['family']
			self.given = patient['name']['given']
			self.identifier = patient['identifier']
			self.gender = patient['gender']
			
			if 'suffix' in patient['name'].keys():
				self.suffix =  patient['name']['suffix']
			else:
				self.suffix = ''
		except Exception as e:
			print e

	def __str__(self):
		name = self.family + ", " + self.given
		if len(self.suffix) > 0:
			name = name + " " + self.suffix
		return name.upper()

	@property
	def dob(self):
	    return self._dob
		
	@property
	def family(self):
	    return self._family

	@property
	def given(self):
	    return self._given

	@property
	def gender(self):
	    return self._gender
	
	def formatDOB(self, format="%d-%b-%Y"):
		#Need to deal with EPIC patients with birthdays in 19th century
		#since they cause errors when passed to strptime
		if self.dob.split("-")[0].startswith("18"):
			dob_formatted = "01-Jan-1871"
		else:
			dob_formatted = dt.strptime(self.dob, "%Y-%m-%d")
			dob_formatted = dt.strftime(dob_formatted, format)

		return dob_formatted.upper()

	def getPIDbyDomain(self, domain):
		for pid in self.identifier:
			if pid['assigner']['reference'] == domain:
				return pid['value']

	#Returns dict of linked identifiers with domain as the key			
	def getPIDlist(self):
		pidlist = {}
		for pid in self.identifier:
			domain = pid['assigner']['reference']
			pidlist[domain] = pid['value']

		return pidlist