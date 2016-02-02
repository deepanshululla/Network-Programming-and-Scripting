#from __future__ import print_function

#r=raw_input("enter numbers ")

# print("starting program")
#cs5700spring2015 STATUS 933 - 8

def calc2(r):
	#print(r)
	n1=r.find('+')
	n2=r.find('-')
	n3=r.find('*')
	n4=r.find('/')
	lm=r.split()
	#print(lm)
	k1=int(lm[2])
	k2=int(lm[4])
	# print([n1,n2,n3,n4])
	if n1>=0:
		
		k3=str(k1+k2)
		
		# print(k3)
		# print("check 1")
		return k3
	elif n2>=0:
		
		k3=str(k1-k2)
		# print(k3)
		# print("check 2")
		return k3
	elif n3>=0:
		
		k3=str(k1*k2)
		# print(k3)
		# print("check 3")
		return k3
		
	elif n4>=0:
		k4=float(k1)/float(k2)
		k5=float(k1/k2)
		if k4==k5:
			k6=int(k4)
			k3=str(k6)
		else:
			k6=int(round(k4))
			k3=str(k6)
		return k3
		
		
# d=calc2(r)
# print(d)