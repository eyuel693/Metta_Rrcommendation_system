import os, json
from dotenv import load_dotenv
import re
import google.generativeai as genai

load_dotenv()
KEY = os.getenv("GEMINI_API_KEY")
print(f"GEMINI_API_KEY loaded: {'Yes' if KEY else 'No'}")
if not KEY:
    print("Warning: GEMINI_API_KEY missing, using fallback parser")
else:
    try:
        genai.configure(api_key=KEY)
        print("Gemini API configured successfully")
    except Exception as e:
        print(f"Warning: Failed to configure Gemini API: {str(e)}, using fallback parser")

# Model
MODEL = None
MODEL_IS_OBJ = False
if KEY:
    try:
        MODEL = genai.GenerativeModel("gemini-2.0-flash")
        MODEL_IS_OBJ = True
        print("Gemini model initialized: gemini-2.0-flash")
    except Exception as e:
        print(f"Warning: Failed to initialize Gemini model: {str(e)}")
        MODEL = None

SCHEMA = ('Reply with ONLY one JSON object like: '
          '{"subject":<string|null>,"relation":"any"|"Watched"|"Likes"|"SimilarUser",'
          '"target_attribute":{"type":"Genre"|"Director","value":"<string>"},"max_depth":<int>}')

def _call(prompt):
    print(f"_call invoked with prompt: {prompt[:200]}...")
    if MODEL and MODEL_IS_OBJ:
        try:
            response = MODEL.generate_content([{"role": "user", "parts": [{"text": prompt}]}])
            print("Gemini API call successful")
            return response
        except Exception as e:
            print(f"Gemini generate_content failed: {str(e)}")
            raise RuntimeError(f"Gemini API call failed: {str(e)}")
    print("No valid Gemini model available")
    raise RuntimeError("No valid Gemini call method available.")

def _txt(resp):
    print("Extracting text from Gemini response")
    text = None

    # Candidate flow
    if hasattr(resp, "candidates") and resp.candidates:
        c = resp.candidates[0]
        content = getattr(c, "content", None)
        if isinstance(content, dict) and "parts" in content:
            text = content["parts"][0]["text"]
        elif hasattr(c, "content") and hasattr(c.content, "parts"):
            parts = getattr(c.content, "parts", [])
            if parts and hasattr(parts[0], "text"):
                text = parts[0].text
        if not text:
            text = str(c)

    # Direct text fallback
    if not text and hasattr(resp, "text"):
        text = resp.text
    if not text:
        text = str(resp)

    text = text.strip()
    print(f"Raw extracted text: {text[:200]}...")

    # Strip code block markers ```json ... ```
    cleaned_text = re.sub(r"^```(?:json)?\s*|\s*```$", "", text, flags=re.MULTILINE).strip()

    # Extra safety: extract JSON {...} if response has extra wrapper
    match = re.search(r"\{.*\}", cleaned_text, re.DOTALL)
    if match:
        cleaned_text = match.group(0)

    print(f"Cleaned text: {cleaned_text[:200]}...")
    return cleaned_text

def _fallback_parse(question, assumed_subject):
    print(f"_fallback_parse invoked with question: '{question}', assumed_subject: '{assumed_subject}'")
    try:
        # Handle "Does <user> like <genre> movies?"
        match = re.match(r"Does (\w+) like (\w+([- ]?\w+)*) movies\??", question, re.IGNORECASE)
        if match:
            subject = match.group(1).lower()
            genre = match.group(2).replace(" ", "-").lower()
            result = {
                "subject": subject,
                "relation": "Likes",
                "target_attribute": {"type": "Genre", "value": genre},
                "max_depth": 1
            }
            print(f"Fallback parsed 'Does ... like ...' match: {result}")
            return result
    
        match = re.match(r"What movies has (\w+) watched\??", question, re.IGNORECASE)
        if match:
            subject = match.group(1).lower()
            result = {
                "subject": subject,
                "relation": "Watched",
                "target_attribute": None,
                "max_depth": 1
            }
            print(f"Fallback parsed 'What movies has ...' match: {result}")
            return result
        
        match = re.match(r"Who are similar to (\w+)\??", question, re.IGNORECASE)
        if match:
            subject = match.group(1).lower()
            result = {
                "subject": subject,
                "relation": "SimilarUser",
                "target_attribute": None,
                "max_depth": 1
            }
            print(f"Fallback parsed 'Who are similar to ...' match: {result}")
            return result
        
        result = {
            "subject": assumed_subject.lower() if assumed_subject else None,
            "relation": "any",
            "target_attribute": None,
            "max_depth": 1
        }
        print(f"Fallback default result (no regex match): {result}")
        return result
    except Exception as e:
        print(f"Fallback parser error: {str(e)}")
        raise ValueError(f"Failed to parse question with fallback parser: {str(e)}")

def parse_question_to_json(q, assumed_subject=None):
    print(f"parse_question_to_json invoked with question: '{q}', assumed_subject: '{assumed_subject}'")
    if not q or not q.strip():
        print("Empty question provided")
        raise ValueError("Empty question")
    prompt = SCHEMA + "\n\nUser question: " + (f"(Assume subject: {assumed_subject}) " if assumed_subject else "") + q.strip()
    print(f"Generated prompt for Gemini: {prompt[:200]}...")
    if not MODEL:
        print("No Gemini model, using fallback parser")
        return _fallback_parse(q, assumed_subject)
    try:
        resp = _call(prompt)
        text = _txt(resp).strip()
        print(f"Gemini response text (clean): {text[:200]}...")
        i, j = text.find("{"), text.rfind("}")
        if i == -1 or j == -1 or j <= i:
            print(f"No valid JSON found in Gemini output: {text[:200]}..., switching to fallback parser")
            return _fallback_parse(q, assumed_subject)
        parsed = json.loads(text[i:j+1])
        parsed["subject"] = (parsed.get("subject") or assumed_subject).lower() if parsed.get("subject") or assumed_subject else None
        parsed["max_depth"] = max(1, min(5, int(parsed.get("max_depth", 1))))
        if parsed.get("target_attribute") and parsed["target_attribute"].get("value"):
            parsed["target_attribute"]["value"] = parsed["target_attribute"]["value"].lower()
           
            if parsed["target_attribute"]["value"] == "<string>":
                parsed["target_attribute"] = None
                print("Fixed invalid target_attribute value '<string>' to None")
        print(f"Gemini parsed JSON: {parsed}")
        return parsed
    except Exception as e:
        print(f"Gemini parsing failed: {str(e)}, switching to fallback parser")
        return _fallback_parse(q, assumed_subject)

def map_json_to_metta(parsed_json):
    print(f"map_json_to_metta invoked with parsed_json: {parsed_json}")
    subject = parsed_json.get('subject')
    if not subject:
        print("No subject provided in parsed JSON")
        raise ValueError("No subject provided in parsed JSON")
    relation = parsed_json.get('relation')
    target_attribute = parsed_json.get('target_attribute')
    if relation == "Likes" and target_attribute and target_attribute['type'] == "Genre":
        query = f'!(match &self (preference {subject} "{target_attribute["value"]}") "{target_attribute["value"]}")'
        print(f"Mapped to Likes query: {query}")
    elif relation == "Watched":
        query = f'!(watched {subject} $movie)'
        print(f"Mapped to Watched query: {query}")
    elif relation == "SimilarUser":
        query = f'!(similar-users {subject} $user)'
        print(f"Mapped to SimilarUser query: {query}")
    else:
        query = f'!(recommend-to {subject} $movie)'
        print(f"Mapped to default recommend-to query: {query}")
    print(f"Final MeTTa query: {query}")
    return query

if __name__ == "__main__":
    print("Running parser.py test cases")
    test_queries = [
        {"question": "Does Alice like Sci-Fi movies?", "assumed_subject": "Alice"},
        {"question": "What movies has Alice watched?", "assumed_subject": "Alice"}
    ]
    for test in test_queries:
        print(f"\nTesting query: '{test['question']}' with assumed_subject: '{test['assumed_subject']}'")
        try:
            parsed = parse_question_to_json(test['question'], test['assumed_subject'])
            print(f"Parsed result: {parsed}")
            metta_query = map_json_to_metta(parsed)
            print(f"Generated MeTTa query: {metta_query}")
        except Exception as e:
            print(f"Test failed for '{test['question']}': {str(e)}")
    print("Test cases completed")
