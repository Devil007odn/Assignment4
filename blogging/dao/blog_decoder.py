import json
from blogging.blog import Blog

class BlogDecoder(json.JSONDecoder):
    ''' Custom JSON decoder for Blog objects '''
    
    def __init__(self, *args, **kwargs):
        super().__init__(object_hook=self.object_hook, *args, **kwargs)
    
    def object_hook(self, dict):
        if '__type__' in dict and dict['__type__'] == 'Blog':
            return Blog(dict['id'], dict['name'], dict['url'], dict['email'])
        return dict