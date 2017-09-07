import urllib3
import certifi
import rsa
import json

#basic request
url = "http://www.google.com"
http = urllib3.PoolManager()
result = http.request('GET',url)
print(result.data)


#target requst
#rsa_pk_url = 'https://eclass.dongguk.edu/User.do?cmd=getRsaPublicKey'
rsa_pk_url = 'https://eclass.dongguk.edu/User.do'

#http 가 아니라 https 라서 인증서 오류나는듯. 관련지식 검색 필요
http = urllib3.PoolManager(cert_reqs="CERT_REQUIRED",ca_cert=certifi.where())
#http = urllib3.PoolManager()
#r = http.request('GET',rsa_pk_url,fields={'cmd':'getRsaPublicKey'})
#r = http.request_encode_url('GET',rsa_pk_url,fields={'cmd':'getRsaPublicKey'})
#print(r.data)

