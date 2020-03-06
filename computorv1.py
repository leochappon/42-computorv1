import sys

def minuses_handler(expressions):
	while "" in expressions:
		expressions.remove("")

	i = 0
	while i < len(expressions):
		if expressions[i] == '-':
			if i + 1 < len(expressions) and expressions[i+1]:
				if expressions[i+1][0] == '-':
					expressions[i+1] = expressions[i+1][1:]
				else:
					expressions[i+1] = '-' + expressions[i+1]
			del expressions[i]
		elif expressions[i] == "":
			del expressions[i]
		else:
			i += 1

	return expressions

def split_equation(equation):
	expressions_left, expressions_right = equation.split('=', 1)

	expressions_left = expressions_left.split('+')
	expressions_right = expressions_right.split('+')

	expressions_left = minuses_handler(expressions_left)
	expressions_right = minuses_handler(expressions_right)

	if not expressions_left or not expressions_right:
		sys.exit("Equation is incomplete")

	for i, e in enumerate(expressions_right):
		if '-' not in e:
			expressions_right[i] = '-' + expressions_right[i]
		else:
			expressions_right[i] = expressions_right[i].replace('-', '')

	expressions = expressions_left + expressions_right

	return expressions

def natural_translation(expressions):
	for i, e in enumerate(expressions):
		if 'X' not in e:
			expressions[i] = expressions[i] + '*X^0'
		if 'X' == e[0]:
			expressions[i] = '1*' + expressions[i]
		elif '-' == e[0] and 'X' == e[1]:
			expressions[i] = expressions[i][0] + '1*' + expressions[i][1:]
		if e[-1] == 'X':
			expressions[i] = expressions[i] + '^1'

	return expressions

def check_expressions_format(expressions):
	for e in expressions:
		i = 0
		dot = 0
		while i < len(e) and e[i] != '*' and (e[i] == '-' or e[i].isdigit() or e[i] == '.'):
			if e[i] == '.':
				dot += 1
			i += 1
		if i - 1 < 0 or (not e[i-1].isdigit() and e[i-1] != '.') or dot >= 2:
			break
		if e[i] == '*':
			i += 1
		else:
			break
		if e[i] == 'X':
			i += 1
		else:
			break
		if e[i] == '^':
			i += 1
		else:
			break
		if i >= len(e) or not e[i].isdigit():
			break
		while i < len(e) and e[i].isdigit():
			i += 1
		if i < len(e):
			break
	else:
		return

	sys.exit("Error on equation format")

def check_exponents_format(expressions):
	for i, e in enumerate(expressions):
		index = e.find('^') + 1
		expressions[i] = e[:index] + str(int(e[index:]))

	return expressions

def get_exponents(expressions):
	exponents = []

	for e in expressions:
		i = e.find('^') + 1
		exponents.append(int(e[i:]))

	exponents = sorted(list(set(exponents)))

	return(exponents)

def get_coefficients(expressions, exponents):
	coefficients = []

	for i in range(len(exponents)):
		coefficient = 0
		for e in expressions:
			index = e.find("*X^" + str(exponents[i]))
			if index > 0:
				coefficient += float(e[:index])
		if coefficient.is_integer():
			coefficient = int(coefficient)
		coefficients.append(coefficient)

	return coefficients

def absolute(nbr):
	return nbr if nbr >= 0 else -nbr

def reduce_equation_form(expo_coef, simplified):
	reduced_form = ""

	for key, value in reversed(list(expo_coef.items())):
		if not reduced_form and value < 0:
			reduced_form += "-"
		elif reduced_form:
			if value < 0:
				reduced_form += " - "
			else:
				reduced_form += " + "
		if simplified == 0:
			reduced_form += str(absolute(value)) + " * X^" + str(key)
		else:
			if key > 0 and absolute(value) == 1:
				reduced_form += "X"
			else:
				reduced_form += str(absolute(value))
				if key > 0:
					reduced_form += " * X" 
			if key > 1:
				reduced_form += "^" + str(key)

	reduced_form += " = 0"

	return reduced_form

def get_discriminant(a, b, c):
	return b ** 2 - 4 * a * c

def solve_quadratic_equation(a, b, c, discriminant):
	discriminant_sqrt = discriminant ** (1.0 /2)

	solution_1 = (-b - discriminant_sqrt) / (2 * a)
	solution_2 = (-b + discriminant_sqrt) / (2 * a)

	print("Quadratic formula:")
	if discriminant < 0:
		print("({}-√{}i)/{}".format(-b, -discriminant, 2 * a))
		print("({}+√{}i)/{}".format(-b, -discriminant, 2 * a))
	elif discriminant == 0:
		print("{}/{}".format(-b, 2 * a))
	else:
		print("({}-√{})/{}".format(-b, discriminant, 2 * a))
		print("({}+√{})/{}".format(-b, discriminant, 2 * a))

	if discriminant >= 0:
		if solution_1.is_integer():
			solution_1 = int(solution_1)
		if solution_2.is_integer():
			solution_2 = int(solution_2)

	return solution_1, solution_2

def main():
	if len(sys.argv) != 2:
		sys.exit("One argument is required")
	elif sys.argv[1].count('=') != 1:
		sys.exit("One '=' is required")

	equation = sys.argv[1]
	equation = "".join(equation.split())
	equation = equation.replace('-', '+-')
	equation = equation.replace('x', 'X')

	if equation.find('X') == -1:
		sys.exit("Unknown 'X' is missing in the equation")

	expressions = split_equation(equation)
	expressions = natural_translation(expressions)

	check_expressions_format(expressions)
	check_exponents_format(expressions)

	exponents = get_exponents(expressions)
	coefficients = get_coefficients(expressions, exponents)

	if all(e == 0 for e in coefficients):
		sys.exit("Any real number is a possible solution")

	expo_coef = dict(zip(exponents, coefficients))
	expo_coef = {key:val for key, val in expo_coef.items() if val != 0}

	polynomial_degree = max(expo_coef)

	if polynomial_degree == 0:
		sys.exit("There is no possible solution")

	reduced_form = reduce_equation_form(expo_coef, 0)
	simplified_form = reduce_equation_form(expo_coef, 1)

	print("Reduced form : {}".format(reduced_form))
	if reduced_form != simplified_form:
		print("Simplified form : {}".format(simplified_form))
	print("Polynomial degree: {}".format(polynomial_degree))

	a = expo_coef.get(2, 0)
	b = expo_coef.get(1, 0)
	c = expo_coef.get(0, 0)

	if polynomial_degree == 1:
		result = -c / b
		print("The solution is:")
		if result.is_integer():
			result = int(result)
		else:
			if b < 0:
				b = -b
				c = -c
			print("{}/{}".format(-c, b))
			print("or")
		print(result)
	elif polynomial_degree == 2:
		discriminant = get_discriminant(a, b, c)
		print("Discriminant: {}".format(discriminant))
		solution_1, solution_2 = solve_quadratic_equation(a, b, c, discriminant)
		if discriminant != 0:
			if discriminant > 0:
				print("Discriminant is strictly positive, the two solutions are:")
			elif discriminant < 0:
				print("Discriminant is strictly negative, the two solutions are:")
			print(solution_1)
		else:
			print("Discriminant is equal to zero, the solution is:")
		print(solution_2)
	elif polynomial_degree > 2:
		print("The polynomial degree is strictly greater than 2, I can't solve.")

if __name__ == "__main__":
	main()
