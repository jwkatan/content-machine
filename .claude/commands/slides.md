# Google Slides Command

Create branded Swimm presentations from content using the Google Slides Apps Script integration.

## Usage

```
/slides create "Presentation Title"     # Create a new presentation from a content brief
/slides create "Title" from [file]       # Create presentation from an existing content file
/slides template                         # Show available slide layouts from the branded template
/slides status                           # List tracked presentations
```

## Workflow

### 1. Understand the request

- What is the presentation about?
- Who is the audience? (prospects, developers, internal, conference)
- How many slides? (default: 8-12 for external, 5-8 for internal)
- Any specific content files to draw from?

### 2. Plan the deck structure

Before generating slides, outline the deck:

```
Slide 1: Title slide — presentation title + subtitle
Slide 2: Problem/context — why this matters
Slides 3-N: Content slides — key points, one idea per slide
Slide N+1: Summary/CTA — what to do next
```

Keep text minimal. Slides are visual aids, not documents:
- **Title**: Max 6-8 words
- **Body text**: Max 3-4 bullet points per slide, each 8-12 words
- **Speaker notes**: Put the detail here, not on the slide

### 3. Generate the presentation

Build the JSON payload following the slide layout types defined in the skill.
Use the `google-slides` skill to send the payload to the Apps Script endpoint.

```python
import requests, os, json
from dotenv import load_dotenv

load_dotenv("data_sources/config/.env")

url = os.environ["GSLIDES_APPS_SCRIPT_URL"]
api_key = os.environ["GSLIDES_API_KEY"]

payload = {
    "action": "create",
    "key": api_key,
    "title": "Presentation Title",
    "templateId": os.environ["GSLIDES_TEMPLATE_ID"],
    "slides": [
        {
            "layout": "TITLE",
            "tokens": {
                "TITLE": "Main Title Here",
                "SUBTITLE": "Supporting subtitle"
            },
            "speakerNotes": "Welcome everyone..."
        },
        {
            "layout": "CONTENT",
            "tokens": {
                "HEADING": "Key Point",
                "BODY": "- First bullet\n- Second bullet\n- Third bullet"
            },
            "speakerNotes": "Expand on the key point..."
        }
    ]
}

response = requests.post(url, json=payload)
result = response.json()
print(f"Presentation: https://docs.google.com/presentation/d/{result['presentationId']}/edit")
```

### 4. Present the result

Show the user:
- Link to the Google Slides presentation
- Summary of slides created
- Remind them to review and adjust visuals (images, charts) manually

## Content Guidelines

Follow `context/brand-voice.md` for tone. Presentations should be:
- **Concise**: One idea per slide
- **Visual**: Minimal text, maximum impact
- **Branded**: Uses Swimm template colors, fonts, layouts
- **Structured**: Clear narrative arc from problem to solution

## Layout Reference

Available layouts are defined by the branded template. Run `/slides template` to see current options.
Each layout has named placeholder tokens (e.g., `TITLE`, `BODY`, `HEADING`) that get filled with content.

## Notes

- The Apps Script duplicates the branded template and fills placeholders — it does NOT create slides from scratch
- Images, charts, and complex visuals should be added manually after generation
- Speaker notes are the place for detailed talking points
- This is a separate Apps Script deployment from the Google Docs integration
