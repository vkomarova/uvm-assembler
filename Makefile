run:
	python3 src/assembler.py tests/spec_test.json program.bin --test

test:
	python3 -m unittest discover -s tests -v
