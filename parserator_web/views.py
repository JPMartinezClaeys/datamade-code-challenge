import usaddress
from typing import Tuple, Dict
from django.views.generic import TemplateView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework.exceptions import ParseError
import logging

# Logging configuration
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


class Home(TemplateView):
    template_name = "parserator_web/index.html"


class AddressParse(APIView):
    renderer_classes = [JSONRenderer]

    def get(self, request) -> Response:
        # TODO: Flesh out this method to parse an address string using the
        # parse() method and return the parsed components to the frontend.

        # Obtain request from search
        address = request.query_params.get("address", "")
        if not address:
            logging.info(f"Address not received")
            return Response({"error": "No address provided"}, status=400)

        # Parse input address
        try:
            address_componenets, address_type = self.parse(address)
        except usaaddress.RepeatedLabelError as e:
            logging.info(f"Parsing address {address} not succesful: {e}")
            return Response({"error": f"{str(e)}"}, status=400)
        except Excepection as e:
            logging.info(f"Parsing address {address} not succesful: {e}")
            return Response({"error": f"{str(e)}"}, status=400)

        # Compile results
        data = {
            "input_string": address,
            "address_components": address_components,
            "address_type": address_type,
        }

        return Response(data)

    def parse(self, address: str) -> Tuple[Dict, str]:
        # TODO: Implement this method to return the parsed components of a
        # given address using usaddress: https://github.com/datamade/usaddress
        try:
            address_components, address_type = usaddress.tag(address)
            return address_components, address_type
        except Exception as e:
            logging.info(f"Parsing address {address} not succesful: {e}")
