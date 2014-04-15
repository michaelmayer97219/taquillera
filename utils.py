def convert_strings_to_unicode(d):
	if not isinstance(d, dict):
		if isinstance(d, str):
			replace = d.decode('utf-8')
			return replace
		else:
			return d
	return dict((k, convert_strings_to_unicode(v)) 
		for k, v in d.items())