from dataclasses import fields, is_dataclass
from typing import Optional

import fire

from sciphi.core import LLMProviderName, RAGProviderName
from sciphi.interface.llm.sciphi_interface import SciPhiFormatter
from sciphi.interface.llm_interface_manager import LLMInterfaceManager
from sciphi.interface.rag_interface_manager import RAGInterfaceManager
from sciphi.llm import GenerationConfig


def filter_relevant_args(dataclass_type, args_dict):
    if not is_dataclass(dataclass_type):
        raise ValueError(f"{dataclass_type} is not a dataclass.")

    relevant_fields = {f.name for f in fields(dataclass_type)}
    return {k: v for k, v in args_dict.items() if k in relevant_fields}


def main(
    # api_key: Optional[str] = None,
    # llm_provider_name: str = "sciphi",
    # llm_api_base: str = "https://api.sciphi.ai/v1",
    # rag_provider_name: str = "sciphi-wiki",
    # rag_api_base: str = "https://api.sciphi.ai",
    # rag_top_k: int = 10,
    # rag_api_key: Optional[str] = None,
    query: str = "Who is the president of the United States?",
    llm_provider_name="sciphi",
    llm_model_name="SciPhi/SciPhi-Self-RAG-Mistral-7B-32k",
    llm_temperature=0.1,
    llm_top_k=100,
    llm_max_tokens_to_sample=256,
    llm_api_base: Optional[str] = None,
    llm_api_key: Optional[str] = None,
    llm_skip_special_tokens: bool = False,
    # RAG Settings
    rag_provider_name="sciphi-wiki",
    rag_enabled=True,
    rag_top_k=10,
    rag_api_base="https://api.sciphi.ai",
    rag_api_key=None,
    **kwargs,
):
    rag_interface = (
        RAGInterfaceManager.get_interface_from_args(
            RAGProviderName(rag_provider_name),
            api_base=rag_api_base or llm_api_base,
            api_key=rag_api_key or llm_api_key,
            top_k=rag_top_k,
        )
        if rag_enabled
        else None
    )
    sciphi_llm = LLMInterfaceManager.get_interface_from_args(
        LLMProviderName(llm_provider_name),
        api_key=llm_api_key,
        api_base=llm_api_base,
        # Currently only consumed by SciPhi
        rag_interface=rag_interface,
        # Consumed by single-load providers
        model_name=llm_model_name,
    )

    completion_config = GenerationConfig(
        temperature=llm_temperature,
        top_k=llm_top_k,
        max_tokens_to_sample=llm_max_tokens_to_sample,
        model_name=llm_model_name,
        skip_special_tokens=llm_skip_special_tokens,
        stop_token=SciPhiFormatter.INIT_PARAGRAPH_TOKEN,
    )
    print("completion_config = ", completion_config)
    completion = sciphi_llm.get_completion(query, completion_config)
    print("completion = ", completion)


if __name__ == "__main__":
    fire.Fire(main)
