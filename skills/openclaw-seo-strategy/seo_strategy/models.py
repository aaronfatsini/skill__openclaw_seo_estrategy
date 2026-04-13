from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional


@dataclass
class PageData:
    source: str
    url: Optional[str]
    raw_text: str
    title: str = ""
    meta_description: str = ""
    h1: List[str] = field(default_factory=list)
    h2: List[str] = field(default_factory=list)
    ctas: List[str] = field(default_factory=list)


@dataclass
class KeywordPlan:
    service: str
    primary: str
    secondary: List[str]
    search_intent: str
    cluster: str


@dataclass
class Issue:
    code: str
    severity: str
    finding: str
    impact: str
    recommendation: str


@dataclass
class SeoReport:
    executive_summary: str
    suggested_primary_keyword: str
    secondary_keywords: List[str]
    search_intent: str
    detected_issues: List[Issue]
    opportunities: List[str]
    page_structure: List[str]
    title_meta_proposals: List[Dict[str, str]]
    heading_proposals: List[Dict[str, List[str]]]
    copy_improvements: List[str]
    content_roadmap: List[str]
    prioritized_action_plan: List[str]
    keyword_plans_by_service: List[KeywordPlan]
