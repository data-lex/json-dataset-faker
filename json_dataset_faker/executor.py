from jsf import JSF
from genson import SchemaBuilder
from typedefs import JsonDict, JsonList, String, StrList
import json


def write_data(source_path: String, synth_data: JsonList) -> None:
    with open(f'{source_path}_synth_data.json', 'w') as f:
        for element in synth_data:
            f.write(f'{json.dumps(element)}\n')
    return


def generate_data(schema: JsonDict) -> JsonList:
    faker: JSF = JSF(schema)
    synth_data: JsonList = list()
    for _ in range(0, 100):
        synth_data.append(faker.generate())
    return synth_data


def get_schema(source_json: String) -> JsonDict:
    builder: SchemaBuilder = SchemaBuilder()
    source_dict: JsonDict = json.loads(source_json)
    builder.add_object(source_dict)
    schema: JsonDict = builder.to_schema()
    return schema


def read_source(source_path: String) -> StrList:
    with open(source_path, 'r') as f:
        file: StrList = f.readlines()
    return file


def main() -> None:
    source_path: String = input('JSON data source path: ')
    source_file: StrList = read_source(source_path)
    source_json: String = "".join(source_file)
    schema: JsonDict = get_schema(source_json)
    synth_data: JsonList = generate_data(schema)
    write_data(source_path, synth_data)
    return


if __name__ == '__main__':
    main()
