# Request context utilities
from flask import g, has_request_context
from werkzeug.local import LocalProxy
import uuid
from datetime import datetime

# Request ID stored in request context
def _get_request_id():
    """Get request ID from request context"""
    if not has_request_context():
        return None
    if not hasattr(g, 'request_id'):
        g.request_id = str(uuid.uuid4())
    return g.request_id

# LocalProxy for request ID
request_id = LocalProxy(lambda: getattr(g, "request_id", None))

def get_request_context():
    """Get the current request context"""
    return g if has_request_context() else None

def set_request_metadata(key, value):
    """Store metadata in request context"""
    if not has_request_context():
        return
    if not hasattr(g, 'request_metadata'):
        g.request_metadata = {}
    g.request_metadata[key] = value

def get_request_metadata(key, default=None):
    """Retrieve metadata from request context"""
    if not has_request_context() or not hasattr(g, 'request_metadata'):
        return default
    return g.request_metadata.get(key, default)

def get_request_start_time():
    """Get request start time from context"""
    if not has_request_context():
        return None
    if not hasattr(g, 'request_start_time'):
        g.request_start_time = datetime.utcnow()
    return g.request_start_time

def get_request_duration():
    """Calculate request duration"""
    if not has_request_context() or not hasattr(g, 'request_start_time'):
        return None
    delta = datetime.utcnow() - g.request_start_time
    return delta.total_seconds()

