# Written by Pejman Ebrahimi
import pandas as pd
import json
import os
from collections import defaultdict
import re 

def format_conversation(messages):
    """Formats a list of messages into a readable string."""
    formatted_messages = []
    for msg in messages:
        role = msg.get('role', 'UNKNOWN_ROLE').upper()
        content = msg.get('content', '')
        content_str = str(content) if content is not None else ""
        formatted_messages.append(f"{role}: {content_str}")
    return "\n".join(formatted_messages)

def process_conversations_substring_match(excel_file_path="data.xlsx", json_folder_path="Json"):
    """
    Reads an Excel file, processes JSON conversations by looking for Participant IDs
    as substrings within any message content, and adds them to the Excel file.

    Args:
        excel_file_path (str): Path to the input Excel file.
        json_folder_path (str): Path to the folder containing JSON files.
    """
    try:
        df = pd.read_excel(excel_file_path)
        if "Participant ID" not in df.columns:
            print(f"Error: 'Participant ID' column not found in {excel_file_path}")
            return
        excel_participant_ids = set(df["Participant ID"].astype(str).str.strip().unique())
        if not excel_participant_ids:
            print(f"Warning: No Participant IDs found in the Excel file {excel_file_path}.")

    except FileNotFoundError:
        print(f"Error: Excel file not found at {excel_file_path}")
        return
    except Exception as e:
        print(f"Error reading Excel file {excel_file_path}: {e}")
        return

    participant_conversations = defaultdict(list)
    found_ids_in_json = set()

    if not os.path.isdir(json_folder_path):
        print(f"Error: JSON folder not found at {json_folder_path}")
        return

    print(f"Processing JSON files from folder: {json_folder_path}...")
    for filename in os.listdir(json_folder_path):
        if filename.endswith(".json"):
            file_path = os.path.join(json_folder_path, filename)
            print(f"  Processing file: {filename}...")
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    sessions_data = json.load(f)

                if not isinstance(sessions_data, list):
                    print(f"    Warning: Content of {filename} is not a list of sessions. Skipping.")
                    continue

                for session_index, session in enumerate(sessions_data):
                    if not isinstance(session, dict):
                        print(f"    Warning: Item at index {session_index} in {filename} is not a session dictionary. Skipping.")
                        continue

                    messages = session.get("messages")
                    if not messages or not isinstance(messages, list) or len(messages) == 0:
                        continue

                    session_participant_id = None
                    # Iterate through all messages in the session
                    for msg_index, msg in enumerate(messages):
                        if not isinstance(msg, dict):
                            continue

                        message_content = msg.get("content")
                        if message_content is not None:
                            message_content_str = str(message_content).strip()
                            for excel_pid in excel_participant_ids:
                                if excel_pid in message_content_str:
                                    session_participant_id = excel_pid
                                    found_ids_in_json.add(session_participant_id)
                                    break 
                            if session_participant_id:
                                break 

                    if session_participant_id:
                        session_conversation_str = format_conversation(messages)
                        participant_conversations[session_participant_id].append(session_conversation_str)

            except json.JSONDecodeError:
                print(f"    Error: Could not decode JSON from {filename}. Skipping this file.")
            except Exception as e:
                print(f"    Error processing file {filename} during session iteration: {e}")

    ids_in_excel_not_in_json = excel_participant_ids - found_ids_in_json
    if ids_in_excel_not_in_json:
        print(f"\nWarning: The following Participant IDs from '{excel_file_path}' were NOT found in any JSON conversations:")
        for pid_miss in sorted(list(ids_in_excel_not_in_json)):
            print(f"  - {pid_miss}")
    else:
        print("\nAll Participant IDs from the Excel file were found in the JSON conversations.")


    def get_aggregated_conversations(pid):
        pid_str = str(pid).strip()
        conv_list = participant_conversations.get(pid_str)
        if conv_list:
            return "\n\n========== NEXT SESSION ==========\n\n".join(conv_list)
        return ""

    df["Conversations"] = df["Participant ID"].apply(get_aggregated_conversations)

    output_excel_file_path = "data_with_conversations_substring.xlsx"
    try:
        df.to_excel(output_excel_file_path, index=False)
        print(f"\nSuccessfully processed files. Output saved to: {output_excel_file_path}")
    except Exception as e:
        print(f"Error saving updated Excel file: {e}")

if __name__ == "__main__":
    process_conversations_substring_match()