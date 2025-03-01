"""consolidators.py

LLM-enabled consolidation methods for summarizing and analyzing log data.
"""

import logging

from dingus.llm_clients import OpenAIChatClient
from dingus.prompts import (
    FORMAT_RESPONSE,
    HEADER_PROMPT,
    PROMPT_PREFIX,
    SUMMARY_PROMPT,
    SYSTEM_PROMPT,
    VECTOR_DB_PROMPT,
)
from dingus.settings import TRUNCATE_LOGS
from dingus.tools.k8 import KubernetesClient
from dingus.tools.vectors import search_logs
from dingus.utils import get_logs_data

logger = logging.getLogger(__name__)


def create_response(user_input: str, summary: str, openai_client: OpenAIChatClient) -> str:
    """Generates a response from the LLM based on user input and log summaries.

    Args:
        user_input (str): The user's query or request.
        summary (str): A summary of relevant logs.
        openai_client (OpenAIChatClient): An instance of the OpenAI chat client.

    Returns:
        str: The response generated by the LLM.
    """
    prompt = (
        f"{PROMPT_PREFIX}{user_input}\n\n {FORMAT_RESPONSE}\n\n"
        f"Here is a summary of the logs you can use for info: \n{summary}"
    )

    messages = [
        {"role": "system", "content": "You are a production debugging expert."},
        {"role": "user", "content": prompt},
    ]

    return openai_client.chat(messages)


def get_vector_db_summary(query_text: str, vector_db: str, openai_client: OpenAIChatClient) -> str:
    """Generates a summary of logs retrieved from the vector database.

    Args:
        query_text (str): The search query for retrieving relevant logs.
        vector_db (str): The vector database to query.
        openai_client (OpenAIChatClient): An instance of the OpenAI chat client.

    Returns:
        str: The generated summary of the retrieved logs.
    """
    vector_search = search_logs(query_text=query_text, vector_db=vector_db, limit=20)

    logger.info(f"Vector search returned {len(vector_search)} results.")

    messages = [
        SYSTEM_PROMPT,
        {"role": "user", "content": VECTOR_DB_PROMPT + str(vector_search)},
    ]

    summary = openai_client.chat(messages, max_tokens=1000)
    logger.info(f"Generated vector DB summary: {summary}")

    return summary


def get_csv_summary(log_file_path: str, openai_client: OpenAIChatClient) -> str:
    """Generates a summary of log data from a CSV file.

    Args:
        log_file_path (str): The file path to the CSV log file.
        openai_client (OpenAIChatClient): An instance of the OpenAI chat client.

    Returns:
        str: A summarized version of the log data.
    """
    log_sample = str(get_logs_data(log_file_path)[:TRUNCATE_LOGS]).replace("'", "").replace(" ", "").replace("\\", "")

    messages = [
        SYSTEM_PROMPT,
        {"role": "user", "content": HEADER_PROMPT + log_sample},
    ]

    headers = openai_client.chat(messages, max_tokens=1000)
    headers = headers.replace("```", "").replace("[", "").replace("]", "")
    headers_list = [item.strip() for item in headers.split(",")]

    log_data = get_logs_data(log_file_path, headers_list)[:TRUNCATE_LOGS]

    messages = [
        SYSTEM_PROMPT,
        {"role": "user", "content": SUMMARY_PROMPT + str(log_data)},
    ]

    summary = openai_client.chat(messages, max_tokens=1000)

    with open("/data/summary_info.txt", "w") as f:
        f.write(summary)

    return summary


def get_k8_summary(openai_client: OpenAIChatClient, kube_config_path: str, namespace: str = "default") -> str:
    """
    Fetch and print a summary of the Kubernetes cluster.
    Args:
        openai_client (OpenAIChatClient): An instance of the OpenAI chat client.
        kube_config_path (str): Path to kube config.
        namespace (str): the k8 namespace.

    Returns:
        str: A summarized snapshot of the k8 deployment.
    """
    kube_client = KubernetesClient(kube_config_path=kube_config_path)
    health = []
    pods = kube_client.list_pods(namespace)

    if pods and isinstance(pods, list):
        health.append(str(kube_client.get_pod_health(pods[0], namespace)))

    messages = [
        SYSTEM_PROMPT,
        {"role": "user", "content": PROMPT_PREFIX + str(health)},
    ]

    k8_summary = openai_client.chat(messages, max_tokens=1000)
    return k8_summary
