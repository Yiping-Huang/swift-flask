from flask import Response

def stream_response(generator):
    return Response(generator(), content_type='text/event-stream')

def generate_stream(data_source):
    for data in data_source:
        yield f"data: {data}\n\n"  # Stream data in the Server-Sent Events format
