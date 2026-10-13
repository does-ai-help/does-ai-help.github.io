"""Apply reviewed multi-label topic corrections and a small explicit hierarchy."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def title_topics(title):
    rules = {
        'engineering': r'\b(?:code|coding|software|developers?|devops|programming|swe-bench)\b',
        'mathematics': r'\b(?:mathematics|mathematical|mathematicians|math)\b|\bnavier[- ]stokes\b',
        'science': r'\b(?:scientific|scientists?|alphafold)\b',
        'learning': r'\b(?:education|learning|students?|learners?|teaching|tutoring|skill formation)\b',
        'work': r'\b(?:jobs?|employment|labou?r|workforce|careers?|employees?|workplace)\b',
        'quality': r'\b(?:quality|defects?|refactoring|maintenance|bugs?|debt|test coverage)\b',
        'productivity': r'\b(?:productivity|efficiency|velocity|speed)\b',
        'security': r'\b(?:security|cybersecurity|vulnerabilities|vulnerability|red[- ]teaming|remote code execution|data theft|owasp)\b',
        'agents': r'\b(?:agents?|agentic|harnesses?|orchestration)\b',
        'methods': r'\b(?:measurement|measuring|benchmarks?|evaluation|evaluating|surveys?|meta-analysis|systematic review|randomized|randomised)\b',
        'business': r'\b(?:firms?|business|economic|spending|costs?|adoption|enterprise|investment)\b',
        'cost': r'\b(?:costs?|spending|tokens?|tokenomics|token economics)\b',
        'governance': r'\b(?:polic(?:y|ies)|governance|provenance|disclosure|declaration)\b',
        'cognition': r'\b(?:cognition|cognitive|understanding|mental models?|critical thinking)\b',
    }
    return [topic for topic, pattern in rules.items() if re.search(pattern, title, re.I)] or ['context']


def classify(record, taxonomy, corrections):
    correction = corrections.get(record['id'], {})
    labels = list(dict.fromkeys([*record.get('topics', []), *correction.get('add', [])]))
    labels = [topic for topic in labels if topic not in correction.get('remove', [])]
    for topic in labels[:]:
        for parent in taxonomy['parents'].get(topic, []):
            if parent not in labels:
                labels.append(parent)
    if len(labels) > 1:
        labels = [topic for topic in labels if topic != 'context']
    unknown = set(labels) - set(taxonomy['topics'])
    if unknown:
        raise ValueError(f"Unknown topics for {record['id']}: {sorted(unknown)}")
    record['topics'] = labels or ['context']
    if correction:
        record['topic_basis'] = correction['basis']
    return record
