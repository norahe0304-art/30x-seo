#!/usr/bin/env python3
"""
Brand mention analysis for AI-generated responses.

Extracts brand mentions from text, scores sentiment, and provides
quantitative positioning metrics across AI platforms.

Usage:
    python brand_mentions.py --brand "Acme Corp" --text "response text..."
    python brand_mentions.py --brand "Acme Corp" --file response.txt
    python brand_mentions.py --brand "Acme Corp" --file response.txt \
        --competitors "Rival Inc,Other Co"
"""

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass


@dataclass
class BrandMention:
    """A single mention of a brand in text."""
    text: str           # The sentence containing the mention
    position: int       # Character offset in source text
    context: str        # Surrounding paragraph
    sentiment: str      # positive, neutral, negative
    sentiment_score: float  # -1.0 to 1.0
    is_primary: bool    # First mention in text
    is_recommendation: bool  # Appears in a recommendation context


@dataclass
class BrandReport:
    """Aggregated brand mention analysis."""
    brand: str
    total_mentions: int
    first_mention_position: int     # -1 if not mentioned
    mention_density: float          # mentions per 1000 words
    avg_sentiment: float            # -1.0 to 1.0
    sentiment_label: str            # positive, neutral, negative
    is_recommended: bool            # Appears as a recommendation
    is_top_3: bool                  # Mentioned in first 3 items of any list
    competitor_rank: int            # Position among competitors (1 = most mentioned)
    mentions: list                  # List of BrandMention dicts


# Positive signal words (weighted)
POSITIVE_SIGNALS = {
    # Strong positive (weight 2)
    "best": 2, "leading": 2, "top": 2, "recommended": 2, "excellent": 2,
    "outstanding": 2, "superior": 2, "premier": 2, "industry-leading": 2,
    "market leader": 2, "gold standard": 2,
    # Moderate positive (weight 1)
    "good": 1, "popular": 1, "trusted": 1, "reliable": 1, "well-known": 1,
    "established": 1, "comprehensive": 1, "powerful": 1, "innovative": 1,
    "efficient": 1, "affordable": 1, "user-friendly": 1, "robust": 1,
    "versatile": 1, "feature-rich": 1, "scalable": 1,
}

# Negative signal words (weighted)
NEGATIVE_SIGNALS = {
    # Strong negative (weight 2)
    "worst": 2, "avoid": 2, "poor": 2, "terrible": 2, "unreliable": 2,
    "overpriced": 2, "outdated": 2, "declining": 2, "controversial": 2,
    # Moderate negative (weight 1)
    "expensive": 1, "limited": 1, "basic": 1, "lacking": 1, "slow": 1,
    "complicated": 1, "difficult": 1, "steep learning curve": 1,
    "missing": 1, "drawback": 1, "downside": 1, "however": 1,
    "although": 1, "but": 0.5, "despite": 0.5,
}

# Recommendation patterns
RECOMMENDATION_PATTERNS = [
    r"(?:we\s+)?recommend\w*\s+{brand}",
    r"{brand}\s+is\s+(?:a\s+)?(?:great|good|excellent|top)\s+(?:choice|option|pick)",
    r"(?:consider|try|check\s+out|look\s+into)\s+{brand}",
    r"(?:best|top)\s+(?:\w+\s+){{0,3}}(?:include|are|is)\s+{brand}",
    r"{brand}\s+(?:stands?\s+out|excels?|leads?)",
]


def extract_sentences(text: str) -> list[str]:
    """Split text into sentences."""
    return re.split(r'(?<=[.!?])\s+', text)


def find_mentions(text: str, brand: str) -> list[BrandMention]:
    """Find all mentions of a brand in text and analyze each."""
    mentions = []
    brand_lower = brand.lower()
    brand_pattern = re.compile(re.escape(brand), re.IGNORECASE)
    sentences = extract_sentences(text)
    text_lower = text.lower()

    is_first = True
    for sentence in sentences:
        if not brand_pattern.search(sentence):
            continue

        # Find position in original text
        sent_lower = sentence.lower()
        pos = text_lower.find(sent_lower)
        if pos == -1:
            pos = text_lower.find(brand_lower)

        # Get surrounding context (paragraph)
        para_start = max(0, text.rfind('\n\n', 0, pos) + 2) if pos > 0 else 0
        para_end = text.find('\n\n', pos)
        if para_end == -1:
            para_end = len(text)
        context = text[para_start:para_end].strip()

        # Score sentiment for this sentence
        sentiment_score = _score_sentiment(sentence, brand)
        if sentiment_score > 0.2:
            sentiment = "positive"
        elif sentiment_score < -0.2:
            sentiment = "negative"
        else:
            sentiment = "neutral"

        # Check if recommendation
        is_rec = _is_recommendation(sentence, brand)

        mention = BrandMention(
            text=sentence.strip(),
            position=pos if pos >= 0 else 0,
            context=context[:500],
            sentiment=sentiment,
            sentiment_score=round(sentiment_score, 2),
            is_primary=is_first,
            is_recommendation=is_rec,
        )
        mentions.append(mention)
        is_first = False

    return mentions


def _score_sentiment(sentence: str, brand: str) -> float:
    """Score sentiment of a sentence mentioning the brand. Returns -1.0 to 1.0."""
    sent_lower = sentence.lower()
    brand_lower = brand.lower()

    # Only score sentiment in the vicinity of the brand mention
    brand_pos = sent_lower.find(brand_lower)
    if brand_pos == -1:
        return 0.0

    # Check window around brand (wider for short sentences)
    window_start = max(0, brand_pos - 100)
    window_end = min(len(sent_lower), brand_pos + len(brand_lower) + 100)
    window = sent_lower[window_start:window_end]

    positive_score = 0.0
    negative_score = 0.0

    for word, weight in POSITIVE_SIGNALS.items():
        if word in window:
            positive_score += weight

    for word, weight in NEGATIVE_SIGNALS.items():
        if word in window:
            negative_score += weight

    total = positive_score + negative_score
    if total == 0:
        return 0.0

    return (positive_score - negative_score) / max(total, 1.0)


def _is_recommendation(sentence: str, brand: str) -> bool:
    """Check if the sentence recommends the brand."""
    for pattern_template in RECOMMENDATION_PATTERNS:
        pattern = pattern_template.format(brand=re.escape(brand))
        if re.search(pattern, sentence, re.IGNORECASE):
            return True
    return False


def _is_in_top_3_list(text: str, brand: str) -> bool:
    """Check if brand appears in the first 3 items of any numbered/bulleted list."""
    brand_lower = brand.lower()
    lines = text.split('\n')

    list_position = 0
    in_list = False

    for line in lines:
        stripped = line.strip()
        # Detect list items
        if re.match(r'^(?:\d+[.)]\s|[-*]\s)', stripped):
            if not in_list:
                in_list = True
                list_position = 0
            list_position += 1
            if list_position <= 3 and brand_lower in stripped.lower():
                return True
        else:
            if stripped:  # Non-empty non-list line resets
                in_list = False
                list_position = 0

    return False


def analyze_brand(text: str, brand: str) -> BrandReport:
    """Analyze all mentions of a brand in text."""
    mentions = find_mentions(text, brand)
    word_count = len(text.split())

    if not mentions:
        return BrandReport(
            brand=brand,
            total_mentions=0,
            first_mention_position=-1,
            mention_density=0.0,
            avg_sentiment=0.0,
            sentiment_label="not mentioned",
            is_recommended=False,
            is_top_3=False,
            competitor_rank=0,
            mentions=[],
        )

    avg_sentiment = sum(m.sentiment_score for m in mentions) / len(mentions)
    if avg_sentiment > 0.2:
        sentiment_label = "positive"
    elif avg_sentiment < -0.2:
        sentiment_label = "negative"
    else:
        sentiment_label = "neutral"

    return BrandReport(
        brand=brand,
        total_mentions=len(mentions),
        first_mention_position=mentions[0].position,
        mention_density=round(len(mentions) / max(word_count, 1) * 1000, 2),
        avg_sentiment=round(avg_sentiment, 2),
        sentiment_label=sentiment_label,
        is_recommended=any(m.is_recommendation for m in mentions),
        is_top_3=_is_in_top_3_list(text, brand),
        competitor_rank=0,  # Set by compare_brands
        mentions=[asdict(m) for m in mentions],
    )


def compare_brands(text: str, primary_brand: str, competitors: list[str]) -> dict:
    """Compare brand mentions against competitors."""
    all_brands = [primary_brand] + competitors
    reports = {}

    for brand in all_brands:
        reports[brand] = analyze_brand(text, brand)

    # Rank by total mentions (descending)
    sorted_brands = sorted(reports.keys(), key=lambda b: reports[b].total_mentions, reverse=True)
    for rank, brand in enumerate(sorted_brands, 1):
        reports[brand].competitor_rank = rank

    primary = reports[primary_brand]

    return {
        "primary_brand": asdict(primary),
        "competitors": {b: asdict(reports[b]) for b in competitors},
        "summary": {
            "primary_rank": primary.competitor_rank,
            "total_brands_mentioned": sum(1 for r in reports.values() if r.total_mentions > 0),
            "primary_sentiment": primary.sentiment_label,
            "primary_recommended": primary.is_recommended,
            "primary_in_top_3": primary.is_top_3,
            "mention_counts": {b: reports[b].total_mentions for b in all_brands},
        },
    }


def main():
    parser = argparse.ArgumentParser(description="Analyze brand mentions in AI-generated responses")
    parser.add_argument("--brand", required=True, help="Primary brand name to analyze")
    parser.add_argument("--text", help="Text to analyze (inline)")
    parser.add_argument("--file", help="File containing text to analyze")
    parser.add_argument("--competitors", help="Comma-separated list of competitor brand names")
    parser.add_argument("--json", "-j", action="store_true", help="Output as JSON")

    args = parser.parse_args()

    if args.file:
        with open(args.file) as f:
            text = f.read()
    elif args.text:
        text = args.text
    else:
        print("Error: provide --text or --file", file=sys.stderr)
        sys.exit(1)

    competitors = [c.strip() for c in args.competitors.split(",")] if args.competitors else []

    if competitors:
        result = compare_brands(text, args.brand, competitors)
    else:
        report = analyze_brand(text, args.brand)
        result = asdict(report)

    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        _print_report(result, bool(competitors))


def _print_report(result: dict, is_comparison: bool):
    """Print human-readable report."""
    if is_comparison:
        primary = result["primary_brand"]
        print(f"Brand Mention Analysis: {primary['brand']}")
        print("=" * 50)
        print(f"  Mentions: {primary['total_mentions']}")
        print(f"  Sentiment: {primary['sentiment_label']} ({primary['avg_sentiment']:+.2f})")
        print(f"  Recommended: {'Yes' if primary['is_recommended'] else 'No'}")
        print(f"  In Top 3 List: {'Yes' if primary['is_top_3'] else 'No'}")
        print(f"  Rank vs Competitors: #{primary['competitor_rank']}")

        print("\nCompetitor Comparison:")
        print(f"  {'Brand':<25} {'Mentions':<10} {'Sentiment':<12} {'Recommended'}")
        print(f"  {'-'*25} {'-'*10} {'-'*12} {'-'*12}")

        all_brands = [(primary['brand'], primary)] + list(result['competitors'].items())
        for brand_name, data in sorted(
            all_brands, key=lambda x: x[1]['total_mentions'], reverse=True
        ):
            if isinstance(data, str):
                data = result['competitors'][data]
            rec = "Yes" if data['is_recommended'] else "No"
            sent = data['sentiment_label']
            print(f"  {brand_name:<25} {data['total_mentions']:<10} {sent:<12} {rec}")
    else:
        print(f"Brand Mention Analysis: {result['brand']}")
        print("=" * 50)
        print(f"  Total Mentions: {result['total_mentions']}")
        if result['total_mentions'] > 0:
            print(f"  First Mention Position: character {result['first_mention_position']}")
            print(f"  Mention Density: {result['mention_density']} per 1000 words")
            print(f"  Avg Sentiment: {result['sentiment_label']} ({result['avg_sentiment']:+.2f})")
            print(f"  Recommended: {'Yes' if result['is_recommended'] else 'No'}")
            print(f"  In Top 3 List: {'Yes' if result['is_top_3'] else 'No'}")

            print("\n  Mentions:")
            for i, m in enumerate(result['mentions'], 1):
                print(f"    {i}. [{m['sentiment']}] {m['text'][:120]}")
        else:
            print("  Brand not mentioned in text.")


if __name__ == "__main__":
    main()
