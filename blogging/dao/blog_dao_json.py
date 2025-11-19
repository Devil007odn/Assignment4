import json
import os
from blogging.dao.blog_dao import BlogDAO
from blogging.blog import Blog
from blogging.configuration import Configuration
from blogging.dao.blog_encoder import BlogEncoder
from blogging.dao.blog_decoder import BlogDecoder
from blogging.exception.illegal_operation_exception import IllegalOperationException

class BlogDAOJSON(BlogDAO):
    '''
    Concrete implementation of BlogDAO that uses JSON for persistence.
    Handles all CRUD operations for Blog objects with automatic file saving.
    '''

    def __init__(self):
        '''
        Initialize the BlogDAOJSON.
        Loads existing blogs from file if autosave is enabled.
        '''
        self.autosave = Configuration.autosave
        self.blogs = {}
        
        # Load blogs from file if autosave is enabled
        if self.autosave:
            self.load_blogs()

    def load_blogs(self):
        ''' Load blogs from JSON file. Handles file not found and decode errors. '''
        if self.autosave and os.path.exists(Configuration.blogs_file):
            try:
                with open(Configuration.blogs_file, 'r') as json_file:
                    blogs_list = json.load(json_file)
                    for blog_dict in blogs_list:
                        blog = Blog(
                            blog_dict['id'],
                            blog_dict['name'], 
                            blog_dict['url'],
                            blog_dict['email']
                        )
                        self.blogs[blog.id] = blog
            except (FileNotFoundError, json.JSONDecodeError):
                # If file doesn't exist or is invalid, start with empty blogs
                self.blogs = {}

    def save_blogs(self):
        ''' Save blogs to JSON file if autosave is enabled '''
        if self.autosave:
            blogs_list = []
            for blog in self.blogs.values():
                blogs_list.append({
                    'id': blog.id,
                    'name': blog.name,
                    'url': blog.url,
                    'email': blog.email
                })
            
            # Ensure directory exists
            os.makedirs(os.path.dirname(Configuration.blogs_file), exist_ok=True)
            
            with open(Configuration.blogs_file, 'w') as json_file:
                json.dump(blogs_list, json_file, indent=2)

    def search_blog(self, blog_id):
        ''' search a blog by blog_id '''
        return self.blogs.get(blog_id)

    def create_blog(self, blog):
        ''' create a new blog '''
        if blog.id in self.blogs:
            return False
        self.blogs[blog.id] = blog
        self.save_blogs()
        return True

    def retrieve_blogs(self, search_term):
        ''' retrieve blogs that match search_term '''
        matching_blogs = []
        for blog in self.blogs.values():
            if search_term in blog.name:
                matching_blogs.append(blog)
        return matching_blogs

    def update_blog(self, blog_id, blog):
        ''' update an existing blog '''
        if blog_id not in self.blogs:
            return False
        self.blogs[blog_id] = blog
        self.save_blogs()
        return True

    def delete_blog(self, blog_id):
        ''' delete a blog '''
        if blog_id not in self.blogs:
            return False
        del self.blogs[blog_id]
        self.save_blogs()
        return True

    def list_blogs(self):
        ''' list all blogs '''
        return list(self.blogs.values())