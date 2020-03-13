class FlaskRequest:
    requestId = ""
    typeInterrogations = []
    matchingRule = {}

    def __init__(self, requestId, typeInterrogations, matchingRule):
        self.requestId = requestId
        self.matchingRule = matchingRule
        self.typeInterrogations = typeInterrogations
