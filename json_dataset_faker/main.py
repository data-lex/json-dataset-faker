from jsf import JSF
from genson import SchemaBuilder
from helpers import read_file, upload_file, write_file
from typedefs import JsonDict, JsonList, String, StrList
import time
import json


def generate_data(schema: JsonDict) -> JsonList:
    faker: JSF = JSF(schema)
    synth_data: JsonList = list()
    for _ in range(0, 100):
        synth_data.append(faker.generate())
    return synth_data


def get_schema(source_json: String) -> JsonDict:
    builder: SchemaBuilder = SchemaBuilder()
    builder.add_object(source_json)
    schema: JsonDict = builder.to_schema()
    return schema


def handler(event: JsonDict, context: JsonDict) -> JsonDict:
    try:
        source_file: StrList = read_file(event['input_bucket'], event['input_key'])
        source_json: String = json.loads("".join(source_file))
        schema: JsonDict = get_schema(source_json)
        synth_data: JsonList = generate_data(schema)
        filename: String = str(int(time.time()))
        write_file(filename, synth_data)
        upload_file(event['output_bucket'], filename, event['label'])
        output: JsonDict = {
            'statusCode': 200,
            'body': 'SUCCESS'
        }

    except Exception as error_message:
        output: JsonDict = {
            'statusCode': 500,
            'body': str(error_message)
        }

    return output
