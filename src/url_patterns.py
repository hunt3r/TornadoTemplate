__author__ = 'hunterc1'
import handlers.example

url_patterns = [
    (r'/', handlers.example.ExampleHandler),
]