import random
import math

#To generate random prime less than N
def randPrime(N):
	primes = []
	for q in range(2,N+1):
		if(isPrime(q)):
			primes.append(q)
	return primes[random.randint(0,len(primes)-1)]

# To check if a number is prime
def isPrime(q):
	if(q > 1):
		for i in range(2, int(math.sqrt(q)) + 1):
			if (q % i == 0):
				return False
		return True
	else:
		return False

#pattern matching
# here log x refers log to the base 2
def randPatternMatch(eps,p,x):# O((m+n) log (m/eps)) time, O(logm + log(m/eps) + k) space
	N = findN(eps,len(p)) # O(log m)  
	q = randPrime(N) #ignoring time complexity
	return modPatternMatch(q,p,x) # O((m+n) log (m/eps)) time, O(logm + logN + k) = O(logm + log(m/eps) + k) space
                                # why N = O(m/eps) -
                                # log N <= 4 * a * a ; where a = m/eps * log26;  also a = O(m/eps) ; 
                                # thus O(log N) = O(log (4 * a^2)) = O(log a) = O(log (m/eps)) 

#pattern matching with wildcard
def randPatternMatchWildcard(eps,p,x):# O((m+n) log (m/eps)) time, O(logm + log(m/eps)+ k) space
	N = findN(eps,len(p))# O(log m) 
	q = randPrime(N)#ignoring time complexity
	return modPatternMatchWildcard(q,p,x) # O((m+n) log (m/eps)) time, O(logm + logN + k) = O(log m + log(m/eps) + k) space
                                        # why N = O(m/eps) -
                                        # log N <= 4 * a * a ; where a = m/eps * log26;  also a = O(m/eps) ; 
                                        # thus O(log N) = O(log (4 * a^2)) = O(log a) = O(log (m/eps)) 
# return appropriate N that satisfies the error bounds


def findN(eps,m): # for logic of finding N, refer to explanation at end of code
    print(m/eps * math.log(26,2)) 
    if (m < 4):
        return findN(eps,4) 
    else:
        return math.ceil(4 * m / eps* math.log(26,2) * math.log(m/eps * math.log(26,2),2)) 


# Return sorted list of starting indices where p matches x
def modPatternMatch(q,p,x): # takes O(k + logn + logq) space, 
                            # time taken is O((m + n)log q)  

    m,n = len(p),len(x)   # n,m take log n and log m bits which is O(log n) as m <= n
    if ( m <= 0): return [] # edge cases
    if (n < m) : return [] # edge cases

    i = 0 # takes log m bits which is O(logn) as m <= n
    hash_p = 0  # f(p) mod q ; takes log q bits
    power = 1  # power is equal to 26 ^ (m-1) mod q , takes log q bits

    # using horner's method for computing the polynomial f(p) mod q in O(m log q) time 
    for i in range(m):   # takes O(m log q) time , i takes log m  bits which is O(logn) as m <= n
        hash_p = (hash_p * 26 + ord(p[i]) - 65) % q    
    # computing power, takes O(m * log q) time , i takes log m  bits which is O(logn) as m <= n
    for i in range(m-1):
        power = (power * 26 ) % q   

    ans = [] # final answer list, takes O(k) space
    j = 0 # takes logn bits 
    hash_x = (ord(x[0]) - 65) % q   # to store f(x[i..(i + m − 1)]) mod q, takes logq bits
    for i in range(0,m): #takes O(m log q) time , i takes log m  bits which is O(logn) as m <= n
        hash_x = (hash_x * 26 + ord(x[i]) - 65) % q  # computing f(x[0..( m − 1)]) mod q 
    if (hash_x == hash_p): ans.append(0) # checking for index 0

    while (j + m  < n ): # O(n log q) time 
        hash_x = ((hash_x - (ord(x[j]) - 65) * power) * 26 + (ord(x[j+m]) - 65)) % q # O(log q), computing 
                # f(x[i + 1..(i + m)]) mod q, using f(x[i..(i + m − 1)]) mod q .  
        if (hash_x == hash_p): ans.append(j+1)  # O(log q), checking for index j+1
            # we can do this, as we already have checked for index 0, and in each iteration we check for index j+1
        # above, we check if hash_p is equal to f(x[j + 1 ..(j + m )]) mod q, using the value of f(x[j..(j + m − 1)]) mod q
        # if it is, we append j+1 as we were checking for index j+1
        j += 1 
    
    return ans 

	

# Return sorted list of starting indices where p matches x
def modPatternMatchWildcard(q,p,x): # takes overall O(logn + logq + k) space``
                                    # time taken is O((m + n)log q) 

    
    m,n = len(p),len(x)   # takes logm + logn bits which is O(logn) as m <= n 
    if (m <= 0): return [] # edge cases
    if (m > n): return [] # edge cases
    wildcard_index = 0 # index storing index of wildcard, takes log m bits which is O(logn) as m <= n
    hash_p = 0  # f(p) mod q ; takes log q bits
    power = 1  # power is equal to 26 ^ (m-1) mod q , takes log q bits
    power_wildcard = 1 # stores 26 ^ (m - wildcard_index - 1) mod q , takes log q bits
    for i in range(0,m) : # takes O(m) time , i takes log m  bits which is O(logn) as m <= n
        if p[i] == '?' : 
            wildcard_index = i 
            hash_p = (hash_p * 26 )% q # if we encounter wildcard, then we ignore it in calculation of f(p)mod q (act as if it is A).
            
        else:
            hash_p = (hash_p * 26 + (ord(p[i]) - 65) )% q  # using horner's method for computing the polynomial f(p) mod q in O(m) time 


    for i in range(m-1) : # computing power as defined above; O(m) time, i takes log m  bits which is O(logn) as m <= n
        power = (power * 26)% q
    
    for i in range(wildcard_index + 1,m):# computing power_wildcard as defined above; O(m) time, i takes log m  bits which is O(logn) as m <= n
        power_wildcard = (power_wildcard * 26 ) % q

    hash_x = 0 # to store f(x[i..(i + m − 1)]) mod q, takes logq bits
    ans = [] # final answer list, takes O(k) space
    for i in range(m): # takes O(m) time, i takes log m  bits which is O(logn) as m <= n
        if (i == wildcard_index): # whenever we compute f(x[i..(i + m − 1)]) mod q, we ignore the letter at the 
                                    # position wildcard_index(corresponding to wildcard), i.e treat it as A, 
                                    #Now, if this value is equal to hash_p, then we can conclude that the pattern 
                                    # has matched the m characters we are checking in the text, as the string 
                                    # x[i..(i + m − 1)] is same as p, with character at wildcard_index in both strings equal to 
                                    # A, and thus the remaining parts are same. thus we can conclude that except the position 
                                    # wildcard_index, all the characters match.
                                    
                                    
            hash_x = (hash_x * 26 ) % q # here we are computing f(x[0..( m − 1)]) mod q by ignoring wildcard character.
        else: 
            hash_x = (hash_x * 26 + (ord(x[i]) - 65) )% q  
    
    if (hash_x == hash_p) : ans.append(0)  # checking for index 0
    j = 0 # takes log n  bits
    while ( j + m  < n): # takes O(n log q) time 
        hash_x = ((hash_x - (ord(x[j]) - 65) * power) * 26 + (ord(x[j+m ]) - 65) + 26 * power_wildcard * (ord(x[j+wildcard_index]) - 65) - 
            power_wildcard*(ord(x[j + wildcard_index + 1]) - 65)) % q #checking for index j+1
            # O(log q), computing f(x[i + 1..(i + m)]) mod q, using f(x[i..(i + m − 1)]) mod q .
            # we can do this, as we already have checked for index 0, and in each iteration we check for index j+1
        # above, we check if hash_p is equal to f(x[j + 1 ..(j + m )]) mod q, using the value of f(x[j..(j + m − 1)]) mod q
        # if it is, we append j+1 as we were checking for index j+1
        if (hash_x == hash_p) : ans.append(j+1)   
        j += 1
    return ans 


# Logic of choosing N- 
# Denote probability of event A by pr(A) 
# Let v be x[i + 1..(i + m)]. Here log x is log to the base 2
# Then pr(f(p) mod q = f(v) mod q, f(p) != f(v)) = pr(q is a prime factor of abs(f(p) – f(v)), d > 0) 
# Now, let d = abs(f(p) – f(v)) 
# Total possible values of q = pi(n) 
# Thus, probability of choosing a prime factor of d = (no. of prime factors of d )/ pi(n) <= (log d)/pi(n) <= log (26^m) / pi(n) ,
# as 0 < d <= 26 ^ m. 
# Thus above probability <= m log(26) / pi(n) 
# Thus pr(f(p) mod q = f(v) mod q, d > 0) = pr(q is a prime factor of d, d > 0) <= m log(26) / pi(n) <= eps (given) 
# => pi(n) >= m/eps * log26 ; let a = m/eps * log26 

# Now we prove the following lemma – 
# if n >= 4* a * log(a) , then pi(n) >= a for all a >= 16
# Pf – 
# Pi( 4*a*loga ) >= 4* a* loga / 2 * log (4*a*loga)    (using the result given in assignment pdf)
# If 4* a* loga / 2 * log (4*a*loga)  >= a, then 
# 2 * log a >= log (4 * a * log a) (taking denominator to rhs) 
# => log (a^2) >= log (4 * a * log a) 
# => a^2 >= 4 * a * log a    (log x is increasing function) 
# => a >= 4 * log a ; 
# This result is true for all a >= 16. QED 

# Now, as pi(n) >= m/eps * log26, we set n = 4* a * log(a) (from above lemma), 
# where a = m/eps * log26. This is valid only when m/eps * log26 >= 16 
# i.e for all m >= 4 (eps <= 1 , log 26 = 4.7004).
# thus for m = 0,1,2,3 we find findN(eps,4) as that is an upper bound for n for these values of m. 















	
