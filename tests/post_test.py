from unittest import TestCase
from unittest import main
from blogging.post import Post
import datetime

class PostTest(TestCase):
	def setUp(self):
		self.post = Post(1, "Starting my journey", "Once upon a time\nThere was a kid...")

	def test_eq(self):
		same_post = Post(1, "Starting my journey", "Once upon a time\nThere was a kid...")
		different_post_1 = Post(2, "Starting my journey", "Once upon a time\nThere was a kid...")
		different_post_2 = Post(1, "Finishing my journey", "Once upon a time\nThere was a kid...")
		different_post_3 = Post(1, "Starting my journey", "And that was it.\nEnd of story.")
		self.assertTrue(self.post == self.post)
		self.assertTrue(self.post == same_post)
		self.assertFalse(self.post == different_post_1)
		self.assertFalse(self.post == different_post_2)
		self.assertFalse(self.post == different_post_3)

	def test_str(self):
		same_post = Post(1, "Starting my journey", "Once upon a time\nThere was a kid...")
		different_post_1 = Post(2, "Starting my journey", "Once upon a time\nThere was a kid...")
		different_post_2 = Post(1, "Finishing my journey", "Once upon a time\nThere was a kid...")
		different_post_3 = Post(1, "Starting my journey", "And that was it.\nEnd of story.")
		self.assertEqual("1; " + str(self.post.creation_time) + "; " + str(self.post.update_time) \
		+ "\nStarting my journey"+ "\n\nOnce upon a time\nThere was a kid...", str(self.post))
		self.assertEqual("1; " + str(self.post.creation_time) + "; " + str(self.post.update_time) \
		+ "\nStarting my journey"+ "\n\nOnce upon a time\nThere was a kid...", str(same_post))
		self.assertEqual("2; " + str(self.post.creation_time) + "; " + str(self.post.update_time) \
		+ "\nStarting my journey"+ "\n\nOnce upon a time\nThere was a kid...", str(different_post_1))
		self.assertEqual("1; " + str(self.post.creation_time) + "; " + str(self.post.update_time) \
		+ "\nFinishing my journey"+ "\n\nOnce upon a time\nThere was a kid...", str(different_post_2))
		self.assertEqual("1; " + str(self.post.creation_time) + "; " + str(self.post.update_time) \
		+ "\nStarting my journey"+ "\n\nAnd that was it.\nEnd of story.", str(different_post_3))
		self.assertEqual(str(same_post), str(self.post))
		self.assertNotEqual(str(different_post_1), str(self.post))
		self.assertNotEqual(str(different_post_2), str(self.post))
		self.assertNotEqual(str(different_post_3), str(self.post))

	def test_repr(self):
		same_post = Post(1, "Starting my journey", "Once upon a time\nThere was a kid...")
		different_post_1 = Post(2, "Starting my journey", "Once upon a time\nThere was a kid...")
		different_post_2 = Post(1, "Finishing my journey", "Once upon a time\nThere was a kid...")
		different_post_3 = Post(1, "Starting my journey", "And that was it.\nEnd of story.")
		self.assertEqual("Post(1, " + repr(self.post.creation_time) + ", " + repr(self.post.update_time) + ",\n" \
		+ "'Starting my journey'" + ",\n\n" + r"'Once upon a time\nThere was a kid...'" + "\n)", repr(self.post))
		self.assertEqual("Post(1, " + repr(same_post.creation_time) + ", " + repr(same_post.update_time) + ",\n" \
		+ "'Starting my journey'" + ",\n\n" + r"'Once upon a time\nThere was a kid...'" + "\n)", repr(same_post))
		self.assertEqual("Post(2, " + repr(different_post_1.creation_time) + ", " + repr(different_post_1.update_time) + ",\n" \
		+ "'Starting my journey'" + ",\n\n" + r"'Once upon a time\nThere was a kid...'" + "\n)", repr(different_post_1))
		self.assertEqual("Post(1, " + repr(different_post_2.creation_time) + ", " + repr(different_post_2.update_time) + ",\n" \
		+ "'Finishing my journey'" + ",\n\n" + r"'Once upon a time\nThere was a kid...'" + "\n)", repr(different_post_2))
		self.assertEqual("Post(1, " + repr(different_post_3.creation_time) + ", " + repr(different_post_3.update_time) + ",\n" \
		+ "'Starting my journey'" + ",\n\n" + r"'And that was it.\nEnd of story.'" + "\n)", repr(different_post_3))
		self.assertEqual(repr(same_post), repr(self.post))
		self.assertNotEqual(repr(different_post_1), repr(self.post))
		self.assertNotEqual(repr(different_post_2), repr(self.post))
		self.assertNotEqual(repr(different_post_3), repr(self.post))

if __name__ == '__main__':
	unittest.main()