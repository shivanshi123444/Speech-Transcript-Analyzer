import re
from typing import List, Dict

class Extractor:
    def __init__(self):
        # Basic patterns for action items and insights
        # These are highly simplified and would need significant refinement
        self.action_item_patterns = [
            r"(?:assign|task|follow up|ensure|need to|will do|action item)[:\s]*([A-Za-z0-9\s,.'\"-]+)",
            r"([A-Z][a-zA-Z\s]+) to (?:work on|prepare|send|check|finalize) (.+)",
            r"(?:deadline|due by|by) ([A-Za-z0-9\s,/-]+)[:\s]*(.+)",
        ]
        self.insight_patterns = [
            r"(?:key decision|decided that|important point|insight)[:\s]*([A-Za-z0-9\s,.'\"-]+)",
            r"(?:we agreed|agreement on)[:\s]*([A-Za-z0-9\s,.'\"-]+)",
            r"(?:conclusion was|takeaway)[:\s]*([A-Za-z0-9\s,.'\"-]+)",
        ]

    def _extract_patterns(self, text: str, patterns: List[str]) -> List[str]:
        extracted = []
        for pattern in patterns:
            extracted.extend(re.findall(pattern, text, re.IGNORECASE))
        return [item[0] if isinstance(item, tuple) else item for item in extracted] # Handle grouped matches

    def extract_action_items(self, text: str) -> List[Dict]:
        """Identifies and lists action items."""
        action_items = []
        for line in text.split('\n'):
            for pattern in self.action_item_patterns:
                match = re.search(pattern, line, re.IGNORECASE)
                if match:
                    # Very basic parsing for responsible parties/deadlines
                    item_text = match.group(0).strip()
                    responsible_party = "Unassigned"
                    deadline = "N/A"

                    # Simple heuristic: look for names or dates near the action item
                    # This is rudimentary and would need more advanced NLP for accuracy
                    if " to " in item_text:
                        parts = item_text.split(" to ", 1)
                        if len(parts) > 1:
                            potential_party = parts[0].strip().split()[-1] # Last word before 'to'
                            if len(potential_party) < 20: # Heuristic for name
                                responsible_party = potential_party

                    date_match = re.search(r"(?:on|by|due by)\s*((?:January|February|March|April|May|June|July|August|September|October|November|December|\d{1,2}[/-]\d{1,2}[/-]\d{2,4})\s*\d{1,2},?\s*\d{4}|\d{1,2}[/-]\d{1,2}[/-]\d{2,4})", line, re.IGNORECASE)
                    if date_match:
                        deadline = date_match.group(1)

                    action_items.append({
                        "item": item_text,
                        "responsible_party": responsible_party,
                        "deadline": deadline
                    })
                    break # Only take the first match per line for simplicity
        return action_items

    def extract_insights(self, text: str) -> List[str]:
        """Highlights key insights, decisions, and important discussion points."""
        insights = []
        for line in text.split('\n'):
            for pattern in self.insight_patterns:
                match = re.search(pattern, line, re.IGNORECASE)
                if match:
                    insights.append(match.group(0).strip())
                    break
        return insights

    def attribute_statements(self, text: str) -> List[Dict]:
        """
        Attributes statements to individual speakers.
        Assumes transcript format like "Speaker Name: statement" or "NAME: statement".
        """
        attributed_statements = []
        lines = text.split('\n')
        speaker_pattern = re.compile(r"^(?:(Speaker \d+)|([A-Z][a-z]+(?: [A-Z][a-z]+)*)):?\s*(.*)", re.IGNORECASE)

        for line in lines:
            match = speaker_pattern.match(line.strip())
            if match:
                speaker = match.group(1) or match.group(2)
                statement = match.group(3).strip()
                if speaker and statement:
                    attributed_statements.append({"speaker": speaker.strip(), "statement": statement})
        return attributed_statements

    def attribute_action_items_and_insights(self, text: str, action_items: List[Dict], insights: List[str]) -> Dict[str, Dict[str, List]]:
        """
        Attempts to attribute extracted action items and insights to speakers.
        This is a heuristic: it finds the closest speaker preceding the item/insight.
        """
        attributed_data = {"action_items": {}, "insights": {}}
        lines = text.split('\n')
        current_speaker = "Unknown"
        speaker_pattern = re.compile(r"^(?:(Speaker \d+)|([A-Z][a-z]+(?: [A-Z][a-z]+)*)):?\s*(.*)", re.IGNORECASE)

        for i, line in enumerate(lines):
            speaker_match = speaker_pattern.match(line.strip())
            if speaker_match:
                current_speaker = speaker_match.group(1) or speaker_match.group(2)
            else:
                # Check if this line contains an action item or insight
                for item in action_items:
                    if item['item'] in line:
                        if current_speaker not in attributed_data["action_items"]:
                            attributed_data["action_items"][current_speaker] = []
                        attributed_data["action_items"][current_speaker].append(item)
                for insight in insights:
                    if insight in line:
                        if current_speaker not in attributed_data["insights"]:
                            attributed_data["insights"][current_speaker] = []
                        attributed_data["insights"][current_speaker].append(insight)

        # Handle any action items/insights not directly attributed (e.g., if they appear before any speaker tag)
        for item in action_items:
            found = False
            for speaker_dict in attributed_data["action_items"].values():
                if item in speaker_dict:
                    found = True
                    break
            if not found:
                if "Unknown" not in attributed_data["action_items"]:
                    attributed_data["action_items"]["Unknown"] = []
                attributed_data["action_items"]["Unknown"].append(item)

        for insight in insights:
            found = False
            for speaker_dict in attributed_data["insights"].values():
                if insight in speaker_dict:
                    found = True
                    break
            if not found:
                if "Unknown" not in attributed_data["insights"]:
                    attributed_data["insights"]["Unknown"] = []
                attributed_data["insights"]["Unknown"].append(insight)

        return attributed_data