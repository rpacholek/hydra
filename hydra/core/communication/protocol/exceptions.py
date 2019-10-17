class NodeConnectionException(Exception):
    pass


class AuthenthicationException(NodeConnectionException):
    pass


class ExchangeException(NodeConnectionException):
    pass


class NegotiationException(NodeConnectionException):
    pass
