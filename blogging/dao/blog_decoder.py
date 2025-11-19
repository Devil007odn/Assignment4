import json
from blogging.blog import Blog

class BlogDecoder(json.JSONDecoder):
    ''' Custom JSON decoder for Blog objects '''
    
    def __init__(self, *args, **kwargs):
        super().__init__(object_hook=self.object_hook, *args, **kwargs)
    
    def object_hook(self, data_dict):
        if '__type__' in data_dict and data_dict['__type__'] == 'Blog':
            return Blog(data_dict['id'], data_dict['name'], data_dict['url'], data_dict['email'])
        return data_dict