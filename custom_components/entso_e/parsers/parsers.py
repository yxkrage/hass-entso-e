from abc import ABC, abstractmethod
from requests import Response
import xml.etree.ElementTree as et


class EntsoeResponseParser(ABC):
    """Abstract class for parsing Entsoe responses."""

    def __init__(
        self,
        response: Response
    ) -> None:
        super().__init__()
        self.response = response

    @abstractmethod
    def parse_response(self) -> dict:
        pass

    @classmethod
    def parser_factory(cls, response: Response) -> 'EntsoeResponseParser':
        """Factory method to create parser based on response type."""
        if response.text[0] == '{':
            return EntsoeJSONParser(response)
        else:
            return EntsoeXMLParser(response)


class EntsoeXMLParser(EntsoeResponseParser):
    """Parses XML responses from Entsoe API."""

    CONST_XML_NS = 'xmlns'

    def parse_response(self):
        # Parse response body according to response type
        ret_key = 'message' # Tag to use in return structure
        if self.response.status_code == 401:
            ret = self._parse_response_401(self.response.text)

        elif self.response.status_code in [200, 400]:
            root = et.fromstring(self.response.text)
            ns, tag = root.tag[1:].split('}')  # Get NS from tag
            xml_ns = {self.CONST_XML_NS: ns}

            if tag == 'Publication_MarketDocument':
                ret = self._parse_response_publication_market_document(self.response.text, xml_ns)
                ret_key = "data"  # Update to 'data'. All other cases are 'message'
            elif tag == 'Acknowledgement_MarketDocument':
                ret = self._parse_response_acknowledgement_market_document(self.response.text, xml_ns)
            else:
                ret = {'text': f'Unknown response document type ({tag})'}
        else:
            ret = {'text': 'Unknown Error'}

        # Wrap and return response
        return {'http_status_code': self.response.status_code,
                ret_key: ret}


    def _parse_response_401(self, xml):
        root = et.fromstring(xml)
        return {'text': root.find('body').text}


    def _parse_response_acknowledgement_market_document(self, xml, xml_ns):
        root = et.fromstring(xml)
        return {'code': root.find(f"{self.CONST_XML_NS}:Reason/{self.CONST_XML_NS}:code", xml_ns).text,
                'text': root.find(f"{self.CONST_XML_NS}:Reason/{self.CONST_XML_NS}:text", xml_ns).text}


    def _parse_response_publication_market_document(self, xml, xml_ns):
        ret = {}

        root = et.fromstring(xml)
        interval_start = root.find(f"{self.CONST_XML_NS}:period.timeInterval/{self.CONST_XML_NS}:start", xml_ns).text
        interval_end = root.find(f"{self.CONST_XML_NS}:period.timeInterval/{self.CONST_XML_NS}:end", xml_ns).text
        ret["intervalStart"] = interval_start
        ret["intervalEnd"] = interval_end

        ts = root.findall(f"{self.CONST_XML_NS}:TimeSeries", xml_ns)
        ret_ts = []
        for t in ts:
            area = t.find(f"{self.CONST_XML_NS}:in_Domain.mRID", xml_ns).text
            currency = t.find(f"{self.CONST_XML_NS}:currency_Unit.name", xml_ns).text
            uom = t.find(f"{self.CONST_XML_NS}:price_Measure_Unit.name", xml_ns).text
            res = t.find(f"{self.CONST_XML_NS}:Period/{self.CONST_XML_NS}:resolution", xml_ns).text
            period_start = t.find(f"{self.CONST_XML_NS}:Period/{self.CONST_XML_NS}:timeInterval/{self.CONST_XML_NS}:start", xml_ns).text
            period_end = t.find(f"{self.CONST_XML_NS}:Period/{self.CONST_XML_NS}:timeInterval/{self.CONST_XML_NS}:end", xml_ns).text

            points = t.findall(f"{self.CONST_XML_NS}:Period/{self.CONST_XML_NS}:Point", xml_ns)
            ret_ps = []
            for p in points:
                pos = p.find(f"{self.CONST_XML_NS}:position", xml_ns).text
                price = p.find(f"{self.CONST_XML_NS}:price.amount", xml_ns).text
                ret_ps.append({"position": pos,
                            "price": price})

            ret_ts.append({"area": area,
                        "currency": currency,
                        "uom": uom,
                        "resolution": res,
                        "periodStart": period_start,
                        "periodEnd": period_end,
                        "points": ret_ps})

        ret["timeSeries"] = ret_ts
        return ret


class EntsoeJSONParser(EntsoeResponseParser):
    """Parses JSON responses from Entsoe API."""

    def parse_response(self):
        # Get Json response
        resp_json = self.response.json()
        
        # Parse response by status code
        status_code = resp_json.get('http_status_code', 0)

        if status_code == 0:
            return {'message': 'No status code in response'}

        elif status_code == 200:
            data = resp_json.get('data', None)
            if data is not None:
                return data
            
            error = resp_json.get('message', None)
            if error is not None:
                return {'message': error.get('text', 'Unknown Error')}

        elif status_code == 400:
            return {'message': resp_json.get('message', None).get('text', 'Unknown Error')}

        if status_code == 401:
            return {'message': resp_json.get('message', None).get('text', 'Unauthorized')}

        else:
            return {'message': 'Unknown Error'}
