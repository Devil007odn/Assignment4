import pickle
import os
from blogging.dao.post_dao import PostDAO
from blogging.configuration import Configuration

class PostDAOPickle(PostDAO):
    '''
    Concrete implementation of PostDAO that uses Pickle for persistence.
    Each blog's posts are stored in separate binary files.
    '''

    def __init__(self, blog):
        '''
        Initialize the PostDAOPickle for a specific blog.
        
        Args:
            blog: The blog object that owns these posts
        '''
        self.autosave = Configuration.autosave
        self.blog = blog
        self.posts = []
        self.counter = 0
        
        # Load posts from file if autosave is enabled
        if self.autosave:
            self.load_posts()

    def get_record_file_path(self):
        ''' Get the file path for this blog's posts '''
        filename = f"{self.blog.id}{Configuration.records_extension}"
        return os.path.join(Configuration.records_path, filename)

    def load_posts(self):
        '''
        Load posts from the blog's record file.
        Updates the counter to maintain proper post code sequencing.
        '''
        try:
            file_path = self.get_record_file_path()
            if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
                with open(file_path, 'rb') as f:
                    loaded_posts = pickle.load(f)
                    if loaded_posts is not None:  # Ensure we don't get None
                        self.posts = loaded_posts
                        # Update counter to ensure new posts get proper codes
                        if self.posts:
                            self.counter = max(post.code for post in self.posts)
        except (FileNotFoundError, pickle.PickleError, EOFError, AttributeError):
            # Handle corrupted or missing files by starting fresh
            self.posts = []
            self.counter = 0

    def save_posts(self):
        ''' Save posts to pickle file '''
        
        if self.autosave:
            try:
                os.makedirs(Configuration.records_path, exist_ok=True)
                file_path = self.get_record_file_path()
                with open(file_path, 'wb') as f:
                    pickle.dump(self.posts, f)
            except Exception as e:
                print(f"Error saving posts: {e}")

    def search_post(self, key):
        ''' search a post by key '''
        for post in self.posts:
            if post.code == key:
                return post
        return None

    def create_post(self, post):
        ''' create a new post '''
        self.posts.append(post)
        self.counter = max(self.counter, post.code)
        self.save_posts()
        return True

    def retrieve_posts(self, search_string):
        ''' retrieve posts that match search string '''
        result = []
        for post in self.posts:
            if search_string in post.title or search_string in post.text:
                result.append(post)
        return result

    def update_post(self, key, new_title, new_text):
        ''' update an existing post '''
        post = self.search_post(key)
        if not post:
            return False
        post.update(new_title, new_text)
        self.save_posts()
        return True

    def delete_post(self, key):
        ''' delete a post '''
        for i, post in enumerate(self.posts):
            if post.code == key:
                del self.posts[i]
                self.save_posts()
                return True
        return False

    def list_posts(self):
        ''' list all posts (most recent first) '''
        return list(reversed(self.posts))