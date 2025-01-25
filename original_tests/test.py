import logging
from mem0 import Memory
import os
from dotenv import load_dotenv
import datetime
import json
from pathlib import Path

load_dotenv()
password = str(os.environ["FIRST_PROJECT_PASSWORD"])

# ログファイルのパスを設定
log_dir = Path("logs")
log_dir.mkdir(exist_ok=True)
log_file = log_dir / f"memory_log_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"

# ロギング設定
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(name)s] [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler(log_file, encoding='utf-8'),
        logging.StreamHandler()  # 標準出力にも表示
    ]
)

logger = logging.getLogger(__name__)

def write_log(message, file_path):
    """ログをファイルに書き込む関数"""
    logger.info(message)

config = {
    "llm": {
    "provider": "openai",
    "config": {
            "model": "gpt-4o-mini",
            "temperature": 0.2,
            "max_tokens": 10000,
        }
    },
    "graph_store": {
        "provider": "neo4j",
        "config": {
            "url": "neo4j+s://204ad1f6.databases.neo4j.io",
            "username": "neo4j",
            "password": password,
        },
        "llm" : {
            "provider": "openai",
            "config": {
                "model": "gpt-4o-mini",#gpt-4o-2024-11-20
                "temperature": 0.0,
            }
        }
    },
    "version": "v1.1"
}

m = Memory.from_config(config_dict=config)

conversation = ("""
Input:
user: What is Toy Nadeshiko?
assistant: I understand. Toy Nadeshiko is a privately-run website that collects information on economic news.
user: Thank you. What's on it?

<New Messages>
assistant: Yes, the headline on the top page of today's "Toy Nadeshiko" website is "Next-generation battery, development competition intensifies."
</New Messages>
""")
# 結果をログファイルに書き込む
add_result = m.graph.add(conversation, filters={"user_id": "alice"})
write_log(f"Add Result: {json.dumps(add_result, indent=2)}", log_file)

#search_result = m.search("tell me my name.", user_id="alice")
#write_log(f"Search Result: {json.dumps(search_result, indent=2)}", log_file)
get_all_result = m.get_all(user_id="alice")
write_log(f"Get All Result: {json.dumps(get_all_result, indent=2)}", log_file)

m.delete_all(user_id="alice")
write_log("Deleted all memories for user 'alice'", log_file)
