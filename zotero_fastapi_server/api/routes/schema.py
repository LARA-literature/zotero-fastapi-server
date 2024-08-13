import json
import gzip
import os
from io import BytesIO
from fastapi import APIRouter, Response, HTTPException, status
from fastapi.responses import StreamingResponse

from typing import List

router = APIRouter()

@router.get("/schema", response_class=StreamingResponse)
async def get_schema(format: str = "json"):
    """
    Return the schema in a compressed format.
    """
    if format != "json":
        return Response(content="Format not supported", status_code=400)
    
    # read schema from file

    print("!!!!!!!!:", os.getcwd())

    with open("zotero_fastapi_server/api/schemata/item_schema.json", "r") as schema_file:
        schema = json.load(schema_file)
    
    schema_json = json.dumps(schema).encode('utf-8')
    buffer = BytesIO()
    
    with gzip.GzipFile(fileobj=buffer, mode='wb') as gzip_file:
        gzip_file.write(schema_json)
    
    buffer.seek(0)
    
    return StreamingResponse(buffer, media_type="application/json", headers={"Content-Encoding": "gzip"})
