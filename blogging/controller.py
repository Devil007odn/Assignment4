import hashlib
import os
from blogging.blog import Blog
from blogging.post import Post
from blogging.configuration import Configuration
from blogging.dao.blog_dao_json import BlogDAOJSON
from blogging.exception.invalid_login_exception import InvalidLoginException
from blogging.exception.duplicate_login_exception import DuplicateLoginException
from blogging.exception.invalid_logout_exception import InvalidLogoutException
from blogging.exception.illegal_access_exception import IllegalAccessException
from blogging.exception.illegal_operation_exception import IllegalOperationException
from blogging.exception.no_current_blog_exception import NoCurrentBlogException

class Controller():
    ''' controller class that receives the system's operations '''

    def __init__(self, autosave=False):
        ''' construct a controller class '''
        self.autosave = autosave or Configuration.autosave
        
        self.users = {}
        
        # Load users from file if autosave is enabled
        if self.autosave:
            self.load_users()
        else:
            # Fallback to hardcoded users for testing
            self.users = {
                "user": "8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92",
                "ali": "6394ffec21517605c1b426d43e6fa7eb0cff606ded9c2956821c2c36bfee2810",
                "kala": "e5268ad137eec951a48a5e5da52558c7727aaa537c8b308b5e403e6b434e036e"
            }

        self.username = None
        self.password = None
        self.logged = False

        # Use BlogDAOJSON instead of direct dictionary
        self.blog_dao = BlogDAOJSON()
        self.current_blog = None

    def load_users(self):
        ''' Load users from users.txt file '''
        try:
            with open(Configuration.users_file, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and ',' in line:
                        username, password_hash = line.split(',', 1)
                        self.users[username] = password_hash
        except FileNotFoundError:
            # If file doesn't exist, use hardcoded as fallback
            self.users = {
                "user": "8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92",
                "ali": "6394ffec21517605c1b426d43e6fa7eb0cff606ded9c2956821c2c36bfee2810",
                "kala": "e5268ad137eec951a48a5e5da52558c7727aaa537c8b308b5e403e6b434e036e"
            }

    def login(self, username, password):
        ''' user logs in the system '''
        if self.logged:
            raise DuplicateLoginException("User already logged in")
        
        if username not in self.users:
            raise InvalidLoginException("Invalid username")
        
        # Hash the provided password and compare with stored hash
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        if password_hash != self.users[username]:
            raise InvalidLoginException("Invalid password")
            
        self.username = username
        self.password = password_hash
        self.logged = True
        return True

    def logout(self):
        ''' user logs out from the system '''
        if not self.logged:
            raise InvalidLogoutException("No user is currently logged in")
            
        self.username = None
        self.password = None
        self.logged = False
        self.current_blog = None
        return True

    def search_blog(self, id):
        ''' user searches a blog '''
        if not self.logged:
            raise IllegalAccessException("User must be logged in to search blogs")
            
        return self.blog_dao.search_blog(id)

    def create_blog(self, id, name, url, email):
        ''' user creates a blog '''
        if not self.logged:
            raise IllegalAccessException("User must be logged in to create blogs")
        
        blog = Blog(id, name, url, email)
        success = self.blog_dao.create_blog(blog)
        if not success:
            raise IllegalOperationException("Blog ID already exists")
        return blog

    def retrieve_blogs(self, name):
        ''' user retrieves the blogs that satisfy a search criterion '''
        if not self.logged:
            raise IllegalAccessException("User must be logged in to retrieve blogs")
            
        return self.blog_dao.retrieve_blogs(name)

    def update_blog(self, original_id, id, name, url, email):
        ''' user updates a blog '''
        if not self.logged:
            raise IllegalAccessException("User must be logged in to update blogs")
        
        blog = self.blog_dao.search_blog(original_id)
        if not blog:
            raise IllegalOperationException("Blog not found")
            
        if self.current_blog and blog == self.current_blog:
            raise IllegalOperationException("Cannot update current blog")
        
        # Update blog fields
        blog.name = name
        blog.url = url
        blog.email = email
        
        # Handle ID change
        if original_id != id:
            if self.blog_dao.search_blog(id):
                raise IllegalOperationException("New blog ID already exists")
            self.blog_dao.delete_blog(original_id)
            blog.id = id
            self.blog_dao.create_blog(blog)
        else:
            self.blog_dao.update_blog(original_id, blog)
            
        return True
            
    def delete_blog(self, id):
        ''' user deletes a blog '''
        if not self.logged:
            raise IllegalAccessException("User must be logged in to delete blogs")
            
        blog = self.blog_dao.search_blog(id)
        if not blog:
            raise IllegalOperationException("Blog not found")
            
        if self.current_blog and blog == self.current_blog:
            raise IllegalOperationException("Cannot delete current blog")
            
        return self.blog_dao.delete_blog(id)

    def list_blogs(self):
        ''' user lists all blogs '''
        if not self.logged:
            raise IllegalAccessException("User must be logged in to list blogs")
            
        return self.blog_dao.list_blogs()

    def set_current_blog(self, id):
        ''' user sets the current blog '''
        if not self.logged:
            raise IllegalAccessException("User must be logged in to set current blog")
            
        blog = self.blog_dao.search_blog(id)
        if not blog:
            raise IllegalOperationException("Blog not found")
            
        self.current_blog = blog
        return True

    def get_current_blog(self):
        ''' get the current blog '''
        if not self.logged:
            raise IllegalAccessException("User must be logged in to get current blog")
            
        return self.current_blog

    def unset_current_blog(self):
        ''' unset the current blog '''
        if not self.logged:
            raise IllegalAccessException("User must be logged in to unset current blog")
            
        self.current_blog = None
        return True

    def search_post(self, code):
        ''' user searches a post from the current blog '''
        if not self.logged:
            raise IllegalAccessException("User must be logged in to search posts")
            
        if not self.current_blog:
            raise NoCurrentBlogException("No current blog selected")
            
        return self.current_blog.search_post(code)

    def create_post(self, title, text):
        ''' user creates a post in the current blog '''
        if not self.logged:
            raise IllegalAccessException("User must be logged in to create posts")
            
        if not self.current_blog:
            raise NoCurrentBlogException("No current blog selected")
            
        return self.current_blog.create_post(title, text)

    def retrieve_posts(self, search_string):
        ''' user retrieves the posts from the current blog that satisfy a search string '''
        if not self.logged:
            raise IllegalAccessException("User must be logged in to retrieve posts")
            
        if not self.current_blog:
            raise NoCurrentBlogException("No current blog selected")
            
        return self.current_blog.retrieve_posts(search_string)

    def update_post(self, code, new_title, new_text):
        ''' user updates a post from the current blog '''
        if not self.logged:
            raise IllegalAccessException("User must be logged in to update posts")
            
        if not self.current_blog:
            raise NoCurrentBlogException("No current blog selected")
            
        return self.current_blog.update_post(code, new_title, new_text)

    def delete_post(self, code):
        ''' user deletes a post from the current blog '''
        if not self.logged:
            raise IllegalAccessException("User must be logged in to delete posts")
            
        if not self.current_blog:
            raise NoCurrentBlogException("No current blog selected")
            
        return self.current_blog.delete_post(code)

    def list_posts(self):
        ''' user lists all posts from the current blog '''
        if not self.logged:
            raise IllegalAccessException("User must be logged in to list posts")
            
        if not self.current_blog:
            raise NoCurrentBlogException("No current blog selected")
            
        return self.current_blog.list_posts()