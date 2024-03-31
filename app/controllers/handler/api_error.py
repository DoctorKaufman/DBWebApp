from datetime import datetime


class APIError:
    def __init__(self, status_code, errors=None):
        if errors is None:
            errors = []
        self.status_code = status_code
        # self.message = message
        self.errors = errors
        self.timestamp = datetime.now()

    def serialize(self):
        return {
            'timestamp': self.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
            'status-code': self.status_code,
            # 'message': self.message,
            'errors': self.errors
        }
