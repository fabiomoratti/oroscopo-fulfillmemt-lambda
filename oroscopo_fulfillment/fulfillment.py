import json
import logging
import iso8601
import speech
from dialogflow_request import DialogflowRequest
from dialogflow_response import DialogflowResponse
from response import SimpleResponse

import intents

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
log_format = "[%(asctime)s] %(levelname)s [%(name)s.%(funcName)s:%(lineno)d] %(message)s",
logging.basicConfig(format=log_format)


def segno_zodiacale_f(req):
    res = DialogflowResponse()
    segno_zodiacale = req.get_parameter(intents.SegnoZodiacaleEntity.NAME)

    text = speech.oroscopo[segno_zodiacale]
    res.set_fulfillment_text(text)
    res.add(SimpleResponse(text, text))

    return res


def data_di_nascita_f(req):
    res = DialogflowResponse()
    data_string = req.get_parameter(intents.SystemEntities.date)
    data = iso8601.parse_date(data_string)

    text = "Non ho trovato il tuo segno!!!"
    if (data.month == 12 and data.day >= 22) or (data.month == 1 and data.day <= 19):
        text = \
            "il tuo segno e' {} e il tuo oroscsopo e': {}".format(intents.SegnoZodiacaleEntity.capricorno,
                                                                  speech.oroscopo[
                                                                      intents.SegnoZodiacaleEntity.capricorno])
    elif (data.month == 1 and data.day >= 20) or (data.month == 2 and data.day <= 17):
        text = \
            "il tuo segno e' {} e il tuo oroscsopo e': {}".format(intents.SegnoZodiacaleEntity.acquario,
                                                                  speech.oroscopo[
                                                                      intents.SegnoZodiacaleEntity.acquario])
    elif (data.month == 2 and data.day >= 18) or (data.month == 3 and data.day <= 19):
        text = \
            "il tuo segno e' {} e il tuo oroscsopo e': {}".format(intents.SegnoZodiacaleEntity.pesci,
                                                                  speech.oroscopo[
                                                                      intents.SegnoZodiacaleEntity.pesci])
    elif (data.month == 3 and data.day >= 20) or (data.month == 4 and data.day <= 19):
        text = \
            "il tuo segno e' {} e il tuo oroscsopo e': {}".format(intents.SegnoZodiacaleEntity.ariete,
                                                                  speech.oroscopo[
                                                                      intents.SegnoZodiacaleEntity.ariete])
    elif (data.month == 4 and data.day >= 20) or (data.month == 5 and data.day <= 20):
        text = \
            "il tuo segno e' {} e il tuo oroscsopo e': {}".format(intents.SegnoZodiacaleEntity.toro,
                                                                  speech.oroscopo[
                                                                      intents.SegnoZodiacaleEntity.toro])
    elif (data.month == 5 and data.day >= 21) or (data.month == 6 and data.day <= 20):
        text = \
            "il tuo segno e' {} e il tuo oroscsopo e': {}".format(intents.SegnoZodiacaleEntity.gemelli,
                                                                  speech.oroscopo[
                                                                      intents.SegnoZodiacaleEntity.gemelli])
    elif (data.month == 6 and data.day >= 21) or (data.month == 7 and data.day <= 22):
        text = \
            "il tuo segno e' {} e il tuo oroscsopo e': {}".format(intents.SegnoZodiacaleEntity.cancro,
                                                                  speech.oroscopo[
                                                                      intents.SegnoZodiacaleEntity.cancro])
    elif (data.month == 7 and data.day >= 23) or (data.month == 8 and data.day <= 22):
        text = \
            "il tuo segno e' {} e il tuo oroscsopo e': {}".format(intents.SegnoZodiacaleEntity.leone,
                                                                  speech.oroscopo[
                                                                      intents.SegnoZodiacaleEntity.leone])
    elif (data.month == 8 and data.day >= 23) or (data.month == 9 and data.day <= 22):
        text = \
            "il tuo segno e' {} e il tuo oroscsopo e': {}".format(intents.SegnoZodiacaleEntity.vergine,
                                                                  speech.oroscopo[
                                                                      intents.SegnoZodiacaleEntity.vergine])
    elif (data.month == 9 and data.day >= 23) or (data.month == 10 and data.day <= 22):
        text = \
            "il tuo segno e' {} e il tuo oroscsopo e': {}".format(intents.SegnoZodiacaleEntity.bilancia,
                                                                  speech.oroscopo[
                                                                      intents.SegnoZodiacaleEntity.bilancia])
    elif (data.month == 10 and data.day >= 23) or (data.month == 11 and data.day <= 21):
        text = \
            "il tuo segno e' {} e il tuo oroscsopo e': {}".format(intents.SegnoZodiacaleEntity.scorpione,
                                                                  speech.oroscopo[
                                                                      intents.SegnoZodiacaleEntity.scorpione])
    elif (data.month == 11 and data.day >= 22) or (data.month == 12 and data.day <= 21):
        text = \
            "il tuo segno e' {} e il tuo oroscsopo e': {}".format(intents.SegnoZodiacaleEntity.sagittario,
                                                                  speech.oroscopo[
                                                                      intents.SegnoZodiacaleEntity.sagittario])
    res.set_fulfillment_text(text)
    res.add(SimpleResponse(text, text))

    return res


def fulfillment(event, context):
    logger.debug("Event Body: %s", json.dumps(event["body"], indent=4))

    req = DialogflowRequest(event["body"])

    dn = req.get_intent_displayName()
    logger.info("Intent display name: %s", dn)

    res = 0
    if dn == intents.Intents.SegnoZodiacale:
        res = segno_zodiacale_f(req)
    elif dn == intents.Intents.DataDiNascita:
        res = data_di_nascita_f(req)

    response_body = res.get_final_response()
    logger.debug("Response Body: %s", json.dumps(json.loads(response_body), indent=4))

    return {
        "statusCode": 200,
        "headers": {'Content-Type': 'application/json'},
        "body": response_body
    }
