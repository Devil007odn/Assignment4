import json
from blogging.blog import Blog

class BlogEncoder(json.JSONEncoder):
    ''' Custom JSON encoder for Blog objects '''
    
    def default(self, blog_obj):
        if isinstance(blog_obj, Blog):
            # Create a serializable representation without the post_dao
            return {
                '__type__': 'Blog',
                'id': blog_obj.id,
                'name': blog_obj.name,
                'url': blog_obj.url,
                'email': blog_obj.email
                # Note: We don't serialize posts here, they're handled separately
            }
        return super().default(blog_obj)