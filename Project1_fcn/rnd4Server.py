from __future__ import print_function
import random
l=("+",'-','/','*')
def oper():
	m1=random.randrange(1,1000)
	m2=random.randrange(1,1000)
	l1=random.randrange(0,3)
	m3=l[l1]
	n=(str(m1)+m3+str(m2))
	# print(n)
	return n
	
# s=oper()
