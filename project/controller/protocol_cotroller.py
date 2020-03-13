from project.repository.protocol_repository import *


class ProtocolController:

    def grab_missing_data(self):
        # flaskRequest = FlaskRequest(request['requestId'], request['typeInterrogations'], request['matchingRule'])
        protocolRepo = ProtocolRepository()
        return protocolRepo.send_response_to_server()
