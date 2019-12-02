from project.recipes.routes import recipes_blueprint
from project.repository.protocol_repository import *
from project.model.type_interrogation import *
from project.repository.protocol_repository import *
class ProtocolController:

    def grab_missing_data(self):
        # flaskRequest = FlaskRequest(request['requestId'], request['typeInterrogations'], request['matchingRule'])
        protocolRepo = ProtocolRepository()
        return protocolRepo.send_response_to_server()