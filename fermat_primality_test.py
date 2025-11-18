import random

def fermat_primality_test(n, k=5):
	# If the number is less than 2, it is not prime
	if n <= 1:
		return False, 0.0
	
	# If the number is 2 or 3, it's prime
	if n <= 3:
		return True, 1.0
	
	# If the number is even or divisible by 3, it's not prime
	if n % 2 == 0 or n % 3 == 0:
		return False, 0.0
	
	# Count the number of successful Fermat tests
	passed_tests = 0
	
	# Perform the Fermat Primality Test 'k' times
	for _ in range(k):
		# Pick a random integer a, where 1 < a < n-1
		a = random.randint(2, n-2)
		
		# Check if a^(n-1) % n == 1 using modular exponentiation
		if pow(a, n-1, n) == 1:  # uses binary exponentiation algorithm
			passed_tests += 1  # Increment count if test passed

	# Calculate the probability based on the number of successful tests
	probability = passed_tests / k
	
	# If passed all tests, it is likely prime
	if passed_tests == k:
		return True, probability
	else:
		return False, probability

# Example usage
n = 7
is_prime, prob = fermat_primality_test(n, k=500)

if is_prime:
	print(f"{n} is probably prime with a probability of {prob:.4f}.")
else:
	print(f"{n} is definitely not prime. Probability of primality: {prob:.4f}.")
