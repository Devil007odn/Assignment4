import json
from blogging.blog import Blog

class BlogEncoder(json.JSONEncoder):
    ''' Custom JSON encoder for Blog objects '''
    
    def default(self, obj):
        if isinstance(obj, Blog):
            # Create a serializable representation without the post_dao
            return {
                '__type__': 'Blog',
                'id': obj.id,
                'name': obj.name,
                'url': obj.url,
                'email': obj.email
                # Note: We don't serialize posts here, they're handled separately
            }
        return super().default(obj)