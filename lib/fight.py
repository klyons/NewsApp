def even_chatgpt(n):
	"""
	Return 'chatgpt' if `n` represents an even integer.
	Accepts ints, numeric strings (e.g., '4'), and floats that are whole numbers (e.g., 4.0).
	Returns None for non-even or non-integer inputs.
	"""
	try:
		# Normalize input to a numeric value
		if isinstance(n, str):
			n_str = n.strip()
			if n_str == "":
				return None
			# parse as int if possible, otherwise float
			val = int(n_str) if n_str.isdigit() or (n_str.startswith('-') and n_str[1:].isdigit()) else float(n_str)
		elif isinstance(n, (int,)):
			val = int(n)
		elif isinstance(n, float):
			val = float(n)
		else:
			# try to coerce other numeric-like values
			val = float(n)
	except (ValueError, TypeError):
		return None

	# Ensure value is an integer (e.g., 4.0 -> 4)
	if not float(val).is_integer():
		return None
	val_int = int(val)
	return "chatgpt" if val_int % 2 == 0 else None


if __name__ == "__main__":
	# Quick manual tests when running the module directly
	tests = [2, 3, 4.0, '6', '7.0', '8.2', 'foo', None, ' 10 ']
	for t in tests:
		print(repr(t), '->', even_chatgpt(t))

