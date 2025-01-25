UPDATE_GRAPH_PROMPT = """
You are an AI expert specializing in graph memory management and optimization. Your task is to analyze existing graph memories alongside new information, and update the relationships in the memory list to ensure the most accurate, current, and coherent representation of knowledge.

Input:
1. Existing Graph Memories: A list of current graph memories, each containing source, target, and relationship information.
2. New Graph Memory: Fresh information to be integrated into the existing graph structure.

Guidelines:
1. Identification: Use the source and target as primary identifiers when matching existing memories with new information.
2. Conflict Resolution:
   - If new information contradicts an existing memory:
     a) For matching source and target but differing content, update the relationship of the existing memory.
     b) If the new memory provides more recent or accurate information, update the existing memory accordingly.
3. Comprehensive Review: Thoroughly examine each existing graph memory against the new information, updating relationships as necessary. Multiple updates may be required.
4. Consistency: Maintain a uniform and clear style across all memories. Each entry should be concise yet comprehensive.
5. Semantic Coherence: Ensure that updates maintain or improve the overall semantic structure of the graph.
6. Temporal Awareness: If timestamps are available, consider the recency of information when making updates.
7. Relationship Refinement: Look for opportunities to refine relationship descriptions for greater precision or clarity.
8. Redundancy Elimination: Identify and merge any redundant or highly similar relationships that may result from the update.

Memory Format:
source -- RELATIONSHIP -- destination

Task Details:
======= Existing Graph Memories:=======
{existing_memories}

======= New Graph Memory:=======
{new_memories}

Output:
Provide a list of update instructions, each specifying the source, target, and the new relationship to be set. Only include memories that require updates.
"""

EXTRACT_RELATIONS_PROMPT = """

You are an advanced algorithm designed to extract structured information from text to construct knowledge graphs. Your goal is to capture comprehensive and accurate information. Follow these key principles:

1. Extract only explicitly stated information from the text.
2. Establish relationships among the entities provided.
3. Use "USER_ID" as the source entity for any self-references (e.g., "I," "me," "my," etc.) in user messages.
4. Distinguish between persistent facts and temporal information:
   - Persistent facts (e.g., "Toy-Nadeshiko is an economic news website") should NOT include timestamps
   - Temporal information MUST include timestamps with appropriate granularity:
     * News headlines/articles: Use date only (YYYY_MM_DD)
     * Real-time status (e.g., cafe occupancy): Use minutes with timezone (YYYY_MM_DD__HH_MM_JST)
     * System events: Use full timestamp with timezone (YYYY_MM_DD__HH_MM_SS_UTC)
   Example:
   - Persistent: "WEBSITE_FOCUSES_ON_ECONOMIC_NEWS"
   - News headline: "HAS_HEADLINE_AS_OF_2025_01_25"
   - Cafe status: "HAS_OCCUPANCY_AS_OF_2025_01_25__13_45_JST"
   - System event: "USER_LOGGED_IN_AT_2025_01_25__13_45_30_UTC"
5. For temporal information, use timestamps in these formats:
   - Date only: YYYY_MM_DD
   - With time: YYYY_MM_DD__HH_MM_TIMEZONE
     where TIMEZONE is JST, UTC, etc.
   - For non-standard timezones: YYYY_MM_DD__HH_MM_plusHHMM or YYYY_MM_DD__HH_MM_minusHHMM
   Current time is CURRENT_TIME.
6. IMPORTANT: Do not use any special characters in relationship names. Use only alphanumeric characters and underscores. For example:
   - Good: "PUBLISHED_NEWS_ON_2025_01_25"
   - Bad: "Published news (on 2025-01-25)"
7. Dont use any special characters in relationship names. Use only alphanumeric characters and underscores.'@' should be replaced with 'atmark'

additional instructions:
CUSTOM_PROMPT

Relationships:
    - Use consistent, general, and timeless relationship types.
    - Example: Prefer "professor" over "became_professor."
    - Relationships should only be established among the entities explicitly mentioned in the user message.

Entity Consistency:
    - Ensure that relationships are coherent and logically align with the context of the message.
    - Maintain consistent naming for entities across the extracted data.

Strive to construct a coherent and easily understandable knowledge graph by eshtablishing all the relationships among the entities and adherence to the user’s context.

Adhere strictly to these guidelines to ensure high-quality knowledge graph extraction."""
DELETE_RELATIONS_SYSTEM_PROMPT = """
You are a graph memory manager specializing in identifying, managing, and optimizing relationships within graph-based memories. Your primary task is to analyze a list of existing relationships and determine which ones should be deleted based on the new information provided.
Input:
1. Existing Graph Memories: A list of current graph memories, each containing source, relationship (with optional timestamp), and destination information.
2. New Text: The new information to be integrated into the existing graph structure.
3. Use "USER_ID" as node for any self-references (e.g., "I," "me," "my," etc.) in user messages.

Now, timestamp information is written into the Relation when temporal information is involved. Past Relations are not necessarily incorrect. For example, information like "BBC website -- has headline as of June 02, 2011 -- Japan's Great East Earthquake" should not be deleted.

Guidelines:
1. Identification: Use the new information to evaluate existing relationships in the memory graph.
2. Deletion Criteria: Delete a relationship only if it meets at least one of these conditions:
   - Contradictory: The new information clearly contradicts the existing information. However, do not consider relationships contradictory solely due to different timestamps.
   - Obvious Mistake: The existing relationship is objectively and clearly incorrect.
3. DO NOT DELETE if their is a possibility of same type of relationship but different destination nodes.
4. Comprehensive Analysis:
   - Thoroughly examine each existing relationship against the new information and delete as necessary.
   - Multiple deletions may be required based on the new information.
5. Semantic Integrity:
   - Ensure that deletions maintain or improve the overall semantic structure of the graph.
   - Avoid deleting relationships that are NOT contradictory/outdated to the new information.
6. Temporal Awareness: Prioritize recency when timestamps are available.
7. Necessity Principle: Only DELETE relationships that must be deleted and are obviously incorrect or clearly contradictory to the new information to maintain an accurate and coherent memory graph. The aim is to eliminate the possibility of causing confusion in thinking.

Note: DO NOT DELETE if their is a possibility of same type of relationship but different destination nodes. 

For example:
Existing Memory: BBC website -- has headline as of June 02, 2011 -- Japan's Great East Earthquake
New Information: BBC website -- has headline as of October 27, 2023 -- Latest News

In the above example, do not delete the past information because the past information is not incorrect and represents information from a different point in time.

Memory Format:
source -- relationship (with optional timestamp) -- destination

Provide a list of deletion instructions, each specifying the relationship to be deleted.
"""


def get_delete_messages(existing_memories_string, data, user_id):
    return DELETE_RELATIONS_SYSTEM_PROMPT.replace(
        "USER_ID", user_id
    ), f"Here are the existing memories: {existing_memories_string} \n\n New Information: {data}"
