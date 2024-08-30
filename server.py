import os
import uvicorn
from datetime import datetime, timezone
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

split_string = '=$%^'*20
log_file_path = './log.txt'

app = FastAPI()

@app.get('/hello')
async def hello():
    return {"hello": "world"}

@app.api_route('/{full_path:path}', methods=['GET', 'POST', 'DELETE', 'PATCH', 'OPTIONS', 'HEAD'])
async def catch_all(request: Request, full_path: str):
    method = request.method
    headers = request.headers
    body = await request.body()

    timestamp = datetime.now(timezone.utc).strftime("%d%m%Y-%H%M%S")

    log_data = f'{split_string}\n'
    log_data += f'Timestamp: {timestamp}\n'
    log_data += f'Method: {method}\n'
    log_data += f'Path: {full_path}\n'
    log_data += f'Headers: {dict(headers)}\n'
    log_data += f'Body: {body.decode("utf-8")}\n'
    log_data += f'{split_string}\n\n'

    with open(log_file_path, 'a') as fo:
        fo.write(log_data)

    response_data = {
        'message': f'Recieved: {timestamp}',
        'method': method,
        'path': full_path,
        'headers': dict(headers),
        'body': body.decode('utf-8')
    }

    return JSONResponse(response_data)


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
