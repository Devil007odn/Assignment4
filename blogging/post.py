import datetime

class Post():
    ''' class that represents a post '''

    def __init__(self, post_code, post_title, post_text):
        ''' constructs a post '''
        self.post_code = post_code
        self.post_title = post_title
        self.post_text = post_text
        now = datetime.datetime.now()
        self.creation_time = now
        self.update_time = now

    def update(self, new_post_title, new_post_text):
        ''' update post post_title and post_text '''
        self.post_title = new_post_title
        self.post_text = new_post_text
        self.update_time = datetime.datetime.now()	

    def __eq__(self, other):
        ''' checks whether this post is the same as other post '''
        return self.post_code == other.post_code and self.post_title == other.post_title and self.post_text == other.post_text

    def __str__(self):
        ''' converts the post object to a string representation '''
        return str(self.post_code) + "; " + str(self.creation_time) + "; " + str(self.update_time) + "\n" + str(self.post_title) + "\n\n" + self.post_text

    def __repr__(self):
        ''' converts the post object to a string representation for debugging '''
        return "Post(%r, %r, %r,\n%r,\n\n%r\n)" % (self.post_code, self.creation_time, self.update_time, self.post_title, self.post_text)