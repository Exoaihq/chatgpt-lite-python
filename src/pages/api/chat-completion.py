import os
import json
from aiohttp import ClientSession
from aiohttp.web import Request, Response, StreamResponse
from typing import List, Dict, Any, Union

async def handler(req: Request) -> Union[Response, StreamResponse]:
    try:
        data = await req.json()
        messages = data['messages']
        prompts = data['prompts']
        config = data['config']

        char_limit = 12000
        char_count = 0
        messages_to_send = []

        for message in messages:
            if char_count + len(message['content']) > char_limit:
                break
            char_count += len(message['content'])
            messages_to_send.append(message)

        use_azure_openai = os.environ.get('AZURE_OPENAI_API_BASE_URL') is not None

        if use_azure_openai:
            api_base_url = os.environ['AZURE_OPENAI_API_BASE_URL']
            version = '2023-03-15-preview'
            deployment = os.environ.get('AZURE_OPENAI_DEPLOYMENT', '')
            if api_base_url.endswith('/'):
                api_base_url = api_base_url[:-1]
            api_url = f"{api_base_url}/openai/deployments/{deployment}/chat/completions?api-version={version}"
            api_key = os.environ['AZURE_OPENAI_API_KEY']
            model = ''  # Azure Open AI always ignores the model and decides based on the deployment name passed through.
        else:
            api_base_url = os.environ.get('OPENAI_API_BASE_URL', 'https://api.openai.com')
            if api_base_url.endswith('/'):
                api_base_url = api_base_url[:-1]
            api_url = f"{api_base_url}/v1/chat/completions"
            api_key = os.environ['OPENAI_API_KEY']
            model = config.get('model', 'gpt-3.5-turbo')  # todo: allow this to be passed through from client and support gpt-4

        if config.get('stream', False) is False:
            data = await openai(api_url, api_key, model, messages_to_send, prompts)
            return Response(text=json.dumps(data), content_type='application/json')
        else:
            stream = await openai_stream(api_url, api_key, model, messages_to_send, prompts, config)
            return stream
    except Exception as error:
        print(error)
        return Response(text='Error', status=500)

async def openai_stream(api_url: str, api_key: str, model: str, messages: List[Dict[str, Any]], prompts: List[Dict[str, Any]], config: Dict[str, Any]) -> StreamResponse:
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {api_key}',
        'api-key': api_key
    }
    payload = {
        'model': model,
        'frequency_penalty': 0,
        'max_tokens': 4000,
        'messages': [*prompts, *messages],
        'presence_penalty': 0,
        'stream': config.get('stream', True),
        'temperature': 0.7,
        'top_p': 0.95
    }

    async with ClientSession() as session:
        async with session.post(api_url, headers=headers, json=payload) as res:
            if res.status != 200:
                status_text = res.reason
                raise Exception(f"The OpenAI API has encountered an error with a status code of {res.status} and message {status_text}")

            response = StreamResponse()
            response.content_type = 'application/json'

            async def stream_data(response):
                async for chunk in res.content.iter_chunked(8192):
                    chunk = chunk.decode('utf-8').replace('[DONE]\n', '[DONE]\n\n')
                    data = json.loads(chunk)
                    text = data['choices'][0]['delta']['content']
                    await response.write(text.encode('utf-8'))

            await response.prepare(req)
            await stream_data(response)
            return response

async def openai(api_url: str, api_key: str, model: str, messages: List[Dict[str, Any]], prompts: List[Dict[str, Any]]) -> Dict[str, Any]:
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {api_key}',
        'api-key': api_key
    }
    payload = {
        'model': model,
        'frequency_penalty': 0,
        'max_tokens': 4000,
        'messages': [*prompts, *messages],
        'presence_penalty': 0,
        'stream': False,
        'temperature': 0.7,
        'top_p': 0.95
    }

    async with ClientSession() as session:
        async with session.post(api_url, headers=headers, json=payload) as res:
            json_data = await res.json()
            return {
                'message': json_data['choices'][0]['message']['content'],
                'usage': json_data['usage']
            }