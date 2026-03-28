import os
import sys
from langchain_ollama import ChatOllama

# -----------------------------
# CONFIG
# -----------------------------
MODEL_NAME = "llama3.1:latest"
OUTPUT_FILE = "combined.txt"
file_path = 'query.txt'
with open(file_path, "r", encoding="utf-8") as f:
    query =  f.read()
print(query)
# query = input('What do you want me to do? \n')
# -----------------------------
# INIT MODEL
# -----------------------------
llm = ChatOllama(model=MODEL_NAME)


# -----------------------------
# TOOLS
# -----------------------------
def list_txt_files(folder_path: str):
    return [f for f in os.listdir(folder_path) if f.endswith(".txt")]


def read_file(file_path: str):
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()


def write_file(output_path: str, content: str):
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(content)


# -----------------------------
# AGENT LOGIC
# -----------------------------
def combine_files_agent(folder_path: str):
    print(f"\nScanning folder: {folder_path}")

    files = list_txt_files(folder_path)

    if not files:
        print("No .txt files found.")
        return

    print(f"Found files: {files}")

    combined_text = ""

    for file in files:
        print(f"\nProcessing: {file}")

        file_path = os.path.join(folder_path, file)
        content = read_file(file_path)

        # LLM processes content (agent-like reasoning)
        # COmbine the file content into a single file. 
        # CLean up spelling mistakes.
        # Use only the final cleaned text, do not add your comments.
        processed = llm.invoke(f"""
        
        {query}
        TEX T :  
        {content}
        """).content

        # combined_text += f"\n\n===== {file} =====\n"
        combined_text += '\n'  + processed

    output_path = os.path.join(folder_path, OUTPUT_FILE)
    write_file(output_path, combined_text)

    print(f"\nCombined file created at: {output_path}")


# -----------------------------
# ENTRY POINT
# -----------------------------
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python agent.py <folder_path>")
        sys.exit(1)

    folder = sys.argv[1]

    if not os.path.exists(folder):
        print("Folder does not exist.")
        sys.exit(1)

    combine_files_agent(folder)
