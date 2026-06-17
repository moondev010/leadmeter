from ollama import Client

class Ollama:
    def __init__(self, bearer_token, base_url):
        self.bearer_token = bearer_token
        self.base_url = base_url

    def generate(self, model, prompt, system_prompt, schema):
        client = Client(
            host=self.base_url,
            headers={
                "Authorization": f"Bearer {self.bearer_token}"
            }
        )

        response = client.chat(
           model=model,
            messages=[
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            format=schema,
            options={'temperature': 0}
        )

        return response.message.content









