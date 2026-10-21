import sys, requests
print(requests.get(sys.argv[1]).text[:10])
