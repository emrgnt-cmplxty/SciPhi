"""A module for interfacing with local HuggingFace models"""
import logging

from sciphi.interface.base import LLMInterface, ProviderName
from sciphi.interface.interface_manager import llm_provider
from sciphi.llm import HuggingFaceConfig, HuggingFaceLLM

logger = logging.getLogger(__name__)


@llm_provider
class HuggingFaceLLMInterface(LLMInterface):
    """A class to interface with local HuggingFace models."""

    provider_name = ProviderName.HUGGING_FACE

    def __init__(
        self,
        config: HuggingFaceConfig = HuggingFaceConfig(),
    ) -> None:
        self._model = HuggingFaceLLM(config)

    def get_completion(self, prompt: str) -> str:
        """Get a completion from the Local HuggingFace API based on the provided prompt."""
        logger.info(
            f"Getting completion from Local HuggingFace API for model={self._model.config.model_name}"
        )
        return self.model.get_instruct_completion(prompt)

    @property
    def model(self) -> HuggingFaceLLM:
        return self._model
