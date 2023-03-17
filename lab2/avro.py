setup_avro = '''
import fastavro
import io

schema = {
    "type": "record",
    "name": "Data",
    "fields": [
        {"name": "PackageID", "type": "int"},
        {"name": "PersonID", "type": "int"},
        {"name": "Name", "type": "string"},
        {"name": "Inventory", "type": {"type": "map", "values": "int"}},
        {"name": "CurrentLocation", "type": "string"}
    ]
}
def serialize_avro(schema, d):
    buffer = io.BytesIO()
    fastavro.schemaless_writer(buffer, schema, d)
    return buffer
    
src = serialize_avro(schema, d)
'''
