"""A module for interfacing with local vLLM models"""
import logging

from sciphi.interface.base import LLMInterface, ProviderName
from sciphi.interface.interface_manager import llm_provider
from sciphi.llm import vLLMConfig, vLLM

logger = logging.getLogger(__name__)


@llm_provider
class HuggingFaceLLMInterface(LLMInterface):
    """A class to interface with local vLLM models."""

    provider_name = ProviderName.VLLM

    def __init__(
        self,
        config: vLLMConfig = vLLMConfig(),
    ) -> None:
        self._model = vLLM(config)

    def get_completion(self, prompt: str) -> str:
        """Get a completion from the Local HuggingFace API based on the provided prompt."""
        logger.info(
            f"Getting completion from Local HuggingFace API for model={self._model.config.model_name}"
        )
        return self.model.get_instruct_completion(prompt)

    @property
    def model(self) -> vLLM:
        return self._model
