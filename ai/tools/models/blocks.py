def text_start():
    return {
        "type": "text_start",
    }

def text_chunk(text):
    return {
        "type": "text_chunk",
        "text": text
    }

def text_result(block):
    return {
        "type": "text_result",
        "id": block.session_id,
    }

def tool_use(block):
    return {
        "type": "tool_use",
        "name": block.name,
        "id": block.id,
        "input": block.input
    }

def tool_result(block):
    return {
        "type": "tool_result",
        "id": block.tool_use_id,
        "content": block.content,
        "is_error": getattr(block, 'is_error', True)
    }

def tool_error(block):
    return {
        "type": "tool_error",
        "id": block.tool_use_id,
        "error": block.content,
    }

def result_error(subtype, session_id, message):
    return {
        "type": "result_error",
        "id": session_id,
        "subtype": subtype,
        "error": message,
    }