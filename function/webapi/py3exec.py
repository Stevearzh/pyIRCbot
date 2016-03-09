import urllib.request
import json

py3URL = "http://www.pythontutor.com/web_exec_py3-1.py?raw_input_json=&options_json=%7B%22cumulative_mode%22%3Afalse%2C%22heap_primitives%22%3Afalse%2C%22show_only_outputs%22%3Afalse%2C%22py_crazy_mode%22%3Afalse%2C%22origin%22%3A%22opt-frontend.js%22%2C%22survey%22%3A%7B%22ver%22%3A%22v4%22%2C%22testing_group%22%3A%22a%22%7D%7D&diffs_json=&user_script="

def reply(string):
	try:
		response = urllib.request.urlopen(py3URL + urllib.request.quote(string.encode("utf8")))
		data = response.read()
		result = json.loads(data.decode("utf8"))
		result = result['trace'][-1]
		if "exception_msg" in result:
			finalResult = result['exception_msg']
		else:
			finalResult = result['stdout']
		if len(finalResult) == 0:
			finalResult = "<no output>"
		return finalResult
	except:
		return "玩坏掉了。"
