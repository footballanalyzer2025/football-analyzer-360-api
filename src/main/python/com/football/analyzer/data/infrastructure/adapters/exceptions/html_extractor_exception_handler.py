class HTMLExtractorExceptionHandler:

    def __init__(self, successor=None):
        self.successor = successor

    def html_extractors_exception_handler(self, exception):
        if self.successor:
            self.successor.html_extractors_exception_handler(exception)
