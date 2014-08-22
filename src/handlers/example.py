
"""
Example handler module
"""

import base
class ExampleHandler(base.BaseHandler):
    """Example handler class"""

    def initialize(self):
         self.foo = "It works!"

    def get(self):
        """Example Handler"""
        self.write(self.foo)

