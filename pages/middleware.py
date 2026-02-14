from .models import Visit

class VisitTrackingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Process request BEFORE view
        
        # Filter unwanted paths to avoid database bloat
        # Exclude static files, admin, health checks, and favicon
        path = request.path
        if (not path.startswith('/static/') and 
           not path.startswith('/admin/') and 
           not path.startswith('/health/') and 
           path != '/favicon.ico'):
            
            # Anonymize IP for GDPR compliance
            ip = self.get_client_ip(request)
            anon_ip = self.anonymize_ip(ip)

            # Fire and forget (in a real high-load system, use celery or async)
            try:
                Visit.objects.create(
                    path=path[:255], # Truncate if necessary
                    method=request.method,
                    user_agent=request.META.get('HTTP_USER_AGENT', '')[:1000] if request.META.get('HTTP_USER_AGENT') else '',
                    ip_address_anonymized=anon_ip,
                    referer=request.META.get('HTTP_REFERER', '')[:1000] if request.META.get('HTTP_REFERER') else ''
                )
            except Exception:
                # Do not crash the site if logging fails
                pass

        response = self.get_response(request)
        return response

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    def anonymize_ip(self, ip):
        if not ip:
            return None
        if ':' in ip: # IPv6
            # Keep first 3 groups roughly (simplified)
            # IPv6 standard anonymization is often /48 or /64. 
            # Keeping first 3 parts (groups) depends on representation.
            # Let's just keep first 2 blocks to be safe
            parts = ip.split(':')
            if len(parts) > 2:
                return ':'.join(parts[:2]) + '::XXXX'
            return ip
        else: # IPv4
            # Zero out last octet
            parts = ip.split('.')
            if len(parts) == 4:
                return '.'.join(parts[:3]) + '.0'
            return ip
