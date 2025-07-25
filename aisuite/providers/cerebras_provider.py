"""Cerebras provider for the aisuite."""

import cerebras.cloud.sdk as cerebras
from aisuite.provider import Provider, LLMError
from aisuite.providers.message_converter import OpenAICompliantMessageConverter


class CerebrasMessageConverter(OpenAICompliantMessageConverter):
    """
    Cerebras-specific message converter if needed.
    """


# pylint: disable=too-few-public-methods
class CerebrasProvider(Provider):
    """Provider for Cerebras."""

    def __init__(self, **config):
        self.client = cerebras.Cerebras(**config)
        self.transformer = CerebrasMessageConverter()

    def chat_completions_create(self, model, messages, **kwargs):
        """
        Makes a request to the Cerebras chat completions endpoint using the official client.
        """
        try:
            response = self.client.chat.completions.create(
                model=model,
                messages=messages,
                **kwargs,  # Pass any additional arguments to the Cerebras API.
            )
            return self.transformer.convert_response(response.model_dump())

        # Re-raise Cerebras API-specific exceptions.
        except cerebras.PermissionDeniedError:
            raise
        except cerebras.AuthenticationError:
            raise
        except cerebras.RateLimitError:
            raise

        # Wrap all other exceptions in LLMError.
        except Exception as e:
            raise LLMError(f"An error occurred: {e}") from e
