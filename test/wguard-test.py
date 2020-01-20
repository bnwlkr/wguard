import unittest
import sys
sys.path.append("..")
import wguard
from contextlib import contextmanager
from StringIO import StringIO

# https://stackoverflow.com/users/33732/rob-kennedy
@contextmanager
def captured_output():
	new_out = StringIO()
	old_out = sys.stdout
	try:
		sys.stdout = new_out
		yield sys.stdout
	finally:
		sys.stdout = old_out

class TestStringMethods(unittest.TestCase):
	
	def test_block(self):
		wguard.unblock("test.com")
		with captured_output() as out:
			wguard.block("test.com")
		output = out.getvalue().strip()
		self.assertEqual(output, "\x1b[92mBlocked test.com\x1b[0m")
		with captured_output() as out:
			wguard.block("test.com")
		output = out.getvalue().strip()
		self.assertEqual(output, "\x1b[94mtest.com is already blocked\x1b[0m")
	
	def test_unblock(self):
		wguard.block("test.com")
		with captured_output() as out:
			wguard.unblock("test.com")
		output = out.getvalue().strip()
		self.assertEqual(output, "\x1b[92mUnblocked test.com\x1b[0m")
		wguard.unblock("test.com")
		with captured_output() as out:
			wguard.unblock("test.com")
		output = out.getvalue().strip()
		self.assertEqual(output, "\x1b[94mwguard wasn't blocking test.com\x1b[0m")
		

if __name__ == "__main__":
	unittest.main()
