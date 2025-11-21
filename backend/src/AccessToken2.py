import time
from agora_token_builder.AccessToken import AccessToken as BaseAccessToken, kJoinChannel, kPublishAudioStream, kPublishVideoStream, kPublishDataStream, kRtmLogin

class ServiceRtc:
    kPrivilegeJoinChannel = kJoinChannel
    kPrivilegePublishAudioStream = kPublishAudioStream
    kPrivilegePublishVideoStream = kPublishVideoStream
    kPrivilegePublishDataStream = kPublishDataStream
    
    def __init__(self, channel_name, uid):
        self.channel_name = channel_name
        self.uid = uid if uid != 0 else ""
        self.privileges = {}
    
    def add_privilege(self, privilege, expire):
        self.privileges[privilege] = expire

class ServiceRtm:
    kPrivilegeLogin = kRtmLogin
    
    def __init__(self, user_id):
        self.user_id = user_id
        self.privileges = {}
    
    def add_privilege(self, privilege, expire):
        self.privileges[privilege] = expire

class AccessToken:
    def __init__(self, app_id, app_certificate, expire):
        self.app_id = app_id
        self.app_certificate = app_certificate
        self.expire = expire
        self.services = []
    
    def add_service(self, service):
        self.services.append(service)
    
    def build(self):
        # Create base token - we'll use the first service for channel/user info
        if not self.services:
            raise ValueError("No services added to token")
        
        # Use the first RTC service for basic token info
        rtc_service = None
        rtm_service = None
        
        for service in self.services:
            if isinstance(service, ServiceRtc):
                rtc_service = service
            elif isinstance(service, ServiceRtm):
                rtm_service = service
        
        if rtc_service:
            token = BaseAccessToken(self.app_id, self.app_certificate, rtc_service.channel_name, rtc_service.uid)
        elif rtm_service:
            token = BaseAccessToken(self.app_id, self.app_certificate, "", rtm_service.user_id)
        else:
            raise ValueError("No valid service found")
        
        # Set token expiration
        token.ts = self.expire
        
        # Add all privileges from all services
        for service in self.services:
            for privilege, expire in service.privileges.items():
                token.addPrivilege(privilege, expire)
        
        return token.build()
