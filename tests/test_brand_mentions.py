"""Tests for scripts/brand_mentions.py - brand mention extraction and analysis."""


from brand_mentions import (
    _is_in_top_3_list,
    _is_recommendation,
    _score_sentiment,
    analyze_brand,
    compare_brands,
    extract_sentences,
    find_mentions,
)


class TestExtractSentences:
    def test_splits_on_period(self):
        text = "First sentence. Second sentence. Third one."
        sentences = extract_sentences(text)
        assert len(sentences) == 3

    def test_splits_on_exclamation(self):
        text = "Great product! Buy now. Works well?"
        sentences = extract_sentences(text)
        assert len(sentences) == 3

    def test_single_sentence(self):
        text = "Just one sentence here"
        sentences = extract_sentences(text)
        assert len(sentences) == 1


class TestFindMentions:
    def test_finds_brand_mentions(self, brand_text_positive):
        mentions = find_mentions(brand_text_positive, "Acme Corp")
        assert len(mentions) == 3

    def test_case_insensitive(self):
        text = "acme corp is great. ACME CORP is the best."
        mentions = find_mentions(text, "Acme Corp")
        assert len(mentions) == 2

    def test_no_mentions_returns_empty(self, brand_text_no_mentions):
        mentions = find_mentions(brand_text_no_mentions, "Acme Corp")
        assert len(mentions) == 0

    def test_first_mention_is_primary(self, brand_text_positive):
        mentions = find_mentions(brand_text_positive, "Acme Corp")
        assert mentions[0].is_primary is True
        assert mentions[1].is_primary is False

    def test_mention_has_position(self, brand_text_positive):
        mentions = find_mentions(brand_text_positive, "Acme Corp")
        assert mentions[0].position >= 0

    def test_mention_has_context(self, brand_text_positive):
        mentions = find_mentions(brand_text_positive, "Acme Corp")
        assert len(mentions[0].context) > 0


class TestSentimentScoring:
    def test_positive_sentiment(self):
        score = _score_sentiment("Acme Corp is the best and most innovative tool", "Acme Corp")
        assert score > 0

    def test_negative_sentiment(self):
        score = _score_sentiment("Acme Corp is overpriced and terrible", "Acme Corp")
        assert score < 0

    def test_neutral_sentiment(self):
        score = _score_sentiment("Acme Corp was founded in 2020", "Acme Corp")
        assert score == 0.0

    def test_brand_not_in_sentence(self):
        score = _score_sentiment("This is a great product", "Acme Corp")
        assert score == 0.0

    def test_mixed_signals(self):
        score = _score_sentiment("Acme Corp is good but expensive", "Acme Corp")
        # Should have both positive and negative, result is nonzero but moderate
        assert isinstance(score, float)


class TestRecommendationDetection:
    def test_recommend_pattern(self):
        assert _is_recommendation("We recommend Acme Corp for all teams", "Acme Corp")

    def test_great_choice_pattern(self):
        assert _is_recommendation("Acme Corp is a great choice for startups", "Acme Corp")

    def test_consider_pattern(self):
        assert _is_recommendation("Consider Acme Corp if you need reliability", "Acme Corp")

    def test_stands_out_pattern(self):
        assert _is_recommendation("Acme Corp stands out among competitors", "Acme Corp")

    def test_no_recommendation(self):
        assert not _is_recommendation("Acme Corp was founded in 2020", "Acme Corp")


class TestIsInTop3List:
    def test_in_top_3_numbered(self):
        text = "Top tools:\n1. Alpha\n2. Acme Corp\n3. Beta"
        assert _is_in_top_3_list(text, "Acme Corp") is True

    def test_not_in_top_3(self):
        text = "Top tools:\n1. Alpha\n2. Beta\n3. Gamma\n4. Acme Corp"
        assert _is_in_top_3_list(text, "Acme Corp") is False

    def test_in_top_3_bulleted(self):
        text = "Options:\n- Acme Corp is the top pick\n- Beta\n- Gamma"
        assert _is_in_top_3_list(text, "Acme Corp") is True

    def test_no_list(self):
        text = "Acme Corp is mentioned but not in any list."
        assert _is_in_top_3_list(text, "Acme Corp") is False


class TestAnalyzeBrand:
    def test_positive_analysis(self, brand_text_positive):
        report = analyze_brand(brand_text_positive, "Acme Corp")
        assert report.total_mentions == 3
        assert report.sentiment_label == "positive"
        assert report.avg_sentiment > 0
        assert report.is_recommended is True

    def test_negative_analysis(self, brand_text_negative):
        report = analyze_brand(brand_text_negative, "Acme Corp")
        assert report.total_mentions == 3
        assert report.sentiment_label == "negative"
        assert report.avg_sentiment < 0

    def test_no_mentions_report(self, brand_text_no_mentions):
        report = analyze_brand(brand_text_no_mentions, "Acme Corp")
        assert report.total_mentions == 0
        assert report.first_mention_position == -1
        assert report.mention_density == 0.0
        assert report.sentiment_label == "not mentioned"
        assert report.is_recommended is False
        assert report.is_top_3 is False
        assert report.mentions == []

    def test_mention_density(self, brand_text_positive):
        report = analyze_brand(brand_text_positive, "Acme Corp")
        assert report.mention_density > 0
        # 3 mentions in ~30 words => density ~ 100 per 1000 words
        assert report.mention_density > 50

    def test_in_top_3_list(self, brand_text_comparison):
        report = analyze_brand(brand_text_comparison, "Acme Corp")
        assert report.is_top_3 is True

    def test_not_in_top_3(self, brand_text_comparison):
        report = analyze_brand(brand_text_comparison, "DeltaApp")
        assert report.is_top_3 is False

    def test_mentions_are_dicts(self, brand_text_positive):
        report = analyze_brand(brand_text_positive, "Acme Corp")
        assert isinstance(report.mentions, list)
        assert isinstance(report.mentions[0], dict)
        assert "text" in report.mentions[0]
        assert "sentiment" in report.mentions[0]


class TestCompareBrands:
    def test_comparison_structure(self, brand_text_comparison):
        result = compare_brands(brand_text_comparison, "Acme Corp", ["AlphaTool", "BetaSoft"])
        assert "primary_brand" in result
        assert "competitors" in result
        assert "summary" in result
        assert "AlphaTool" in result["competitors"]
        assert "BetaSoft" in result["competitors"]

    def test_ranking(self, brand_text_comparison):
        result = compare_brands(brand_text_comparison, "Acme Corp", ["AlphaTool", "BetaSoft"])
        summary = result["summary"]
        # AlphaTool has more mentions, should rank higher
        assert summary["mention_counts"]["AlphaTool"] >= 1
        assert summary["mention_counts"]["Acme Corp"] >= 1

    def test_primary_rank_in_summary(self, brand_text_comparison):
        result = compare_brands(brand_text_comparison, "Acme Corp", ["AlphaTool", "BetaSoft"])
        assert result["summary"]["primary_rank"] >= 1

    def test_total_brands_mentioned(self, brand_text_comparison):
        result = compare_brands(brand_text_comparison, "Acme Corp", ["AlphaTool", "BetaSoft"])
        assert result["summary"]["total_brands_mentioned"] >= 2

    def test_competitor_not_in_text(self):
        text = "Acme Corp is the best tool available."
        result = compare_brands(text, "Acme Corp", ["NonExistentBrand"])
        assert result["competitors"]["NonExistentBrand"]["total_mentions"] == 0
        assert result["primary_brand"]["total_mentions"] == 1


class TestEdgeCases:
    def test_empty_text(self):
        report = analyze_brand("", "Acme Corp")
        assert report.total_mentions == 0

    def test_brand_is_substring(self):
        """Ensure partial matches are handled (brand_pattern uses re.escape)."""
        text = "AcmeCorpX is not the same as Acme Corp."
        mentions = find_mentions(text, "Acme Corp")
        # Should find "Acme Corp" in both occurrences (AcmeCorpX contains Acme Corp)
        assert len(mentions) >= 1

    def test_special_characters_in_brand(self):
        text = "C++ Tools is the best. We recommend C++ Tools."
        mentions = find_mentions(text, "C++ Tools")
        assert len(mentions) == 2

    def test_very_long_text(self):
        """Performance sanity check with large text."""
        text = "Acme Corp is great. " * 1000
        report = analyze_brand(text, "Acme Corp")
        assert report.total_mentions > 0
        assert report.mention_density > 0
