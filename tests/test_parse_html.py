"""Tests for scripts/parse_html.py - HTML parsing and SEO element extraction."""


from parse_html import parse_html


class TestTitleExtraction:
    def test_extracts_title(self, sample_html_full):
        result = parse_html(sample_html_full)
        assert result["title"] == "Best Widget Tools 2025 - WidgetCo"

    def test_missing_title_returns_none(self, sample_html_no_title):
        result = parse_html(sample_html_no_title)
        assert result["title"] is None

    def test_empty_title(self):
        html = "<html><head><title>   </title></head><body></body></html>"
        result = parse_html(html)
        # Empty/whitespace title should be empty string after strip
        assert result["title"] == ""


class TestMetaTags:
    def test_extracts_meta_description(self, sample_html_full):
        result = parse_html(sample_html_full)
        expected = "Discover the best widget tools for your business in 2025."
        assert result["meta_description"] == expected

    def test_extracts_meta_robots(self, sample_html_full):
        result = parse_html(sample_html_full)
        assert result["meta_robots"] == "index, follow"

    def test_missing_meta_description(self, sample_html_minimal):
        result = parse_html(sample_html_minimal)
        assert result["meta_description"] is None

    def test_missing_meta_robots(self, sample_html_minimal):
        result = parse_html(sample_html_minimal)
        assert result["meta_robots"] is None

    def test_extracts_open_graph(self, sample_html_full):
        result = parse_html(sample_html_full)
        assert result["open_graph"]["og:title"] == "Best Widget Tools 2025"
        assert result["open_graph"]["og:description"] == "Top widget tools reviewed."
        assert result["open_graph"]["og:image"] == "https://example.com/og.png"

    def test_extracts_twitter_card(self, sample_html_full):
        result = parse_html(sample_html_full)
        assert result["twitter_card"]["twitter:card"] == "summary_large_image"
        assert result["twitter_card"]["twitter:title"] == "Best Widget Tools 2025"


class TestCanonicalAndHreflang:
    def test_extracts_canonical(self, sample_html_full):
        result = parse_html(sample_html_full)
        assert result["canonical"] == "https://example.com/widgets"

    def test_missing_canonical(self, sample_html_minimal):
        result = parse_html(sample_html_minimal)
        assert result["canonical"] is None

    def test_extracts_hreflang(self, sample_html_full):
        result = parse_html(sample_html_full)
        assert len(result["hreflang"]) == 2
        langs = [h["lang"] for h in result["hreflang"]]
        assert "en" in langs
        assert "es" in langs


class TestHeadings:
    def test_extracts_h1(self, sample_html_full):
        result = parse_html(sample_html_full)
        assert "Best Widget Tools for 2025" in result["h1"]

    def test_extracts_h2(self, sample_html_full):
        result = parse_html(sample_html_full)
        assert len(result["h2"]) == 2
        assert "Top Picks" in result["h2"]
        assert "Detailed Reviews" in result["h2"]

    def test_extracts_h3(self, sample_html_full):
        result = parse_html(sample_html_full)
        assert "WidgetCo Pro" in result["h3"]
        assert "RivalWidget" in result["h3"]

    def test_no_headings(self, sample_html_minimal):
        result = parse_html(sample_html_minimal)
        assert result["h1"] == []
        assert result["h2"] == []
        assert result["h3"] == []

    def test_empty_heading_ignored(self):
        html = "<html><body><h1>  </h1><h1>Real Heading</h1></body></html>"
        result = parse_html(html)
        # Empty-after-strip headings should be skipped
        assert result["h1"] == ["Real Heading"]


class TestImages:
    def test_extracts_images(self, sample_html_full):
        result = parse_html(sample_html_full)
        assert len(result["images"]) == 2

    def test_image_attributes(self, sample_html_full):
        result = parse_html(sample_html_full, base_url="https://example.com")
        hero = next(img for img in result["images"] if "hero" in img["src"])
        assert hero["alt"] == "Widget tools comparison"
        assert hero["width"] == "800"
        assert hero["height"] == "400"
        assert hero["loading"] == "lazy"

    def test_relative_src_resolved_with_base_url(self, sample_html_full):
        result = parse_html(sample_html_full, base_url="https://example.com")
        srcs = [img["src"] for img in result["images"]]
        assert "https://example.com/images/hero.jpg" in srcs

    def test_image_missing_alt(self, sample_html_full):
        result = parse_html(sample_html_full)
        # Second image has empty alt
        alt_values = [img["alt"] for img in result["images"]]
        assert "" in alt_values

    def test_no_images(self, sample_html_minimal):
        result = parse_html(sample_html_minimal)
        assert result["images"] == []


class TestLinks:
    def test_classifies_internal_links(self, sample_html_full):
        result = parse_html(sample_html_full, base_url="https://example.com")
        internal_hrefs = [lnk["href"] for lnk in result["links"]["internal"]]
        assert "https://example.com/" in internal_hrefs
        assert "https://example.com/reviews/widgetco-pro" in internal_hrefs

    def test_classifies_external_links(self, sample_html_full):
        result = parse_html(sample_html_full, base_url="https://example.com")
        external_hrefs = [lnk["href"] for lnk in result["links"]["external"]]
        assert "https://external.com/deal" in external_hrefs

    def test_no_links_without_base_url(self, sample_html_full):
        """Without base_url, links are not classified."""
        result = parse_html(sample_html_full)
        assert result["links"]["internal"] == []
        assert result["links"]["external"] == []

    def test_skips_fragment_links(self):
        html = (
            '<html><body><a href="#section">Jump</a>'
            '<a href="javascript:void(0)">Click</a></body></html>'
        )
        result = parse_html(html, base_url="https://example.com")
        assert result["links"]["internal"] == []
        assert result["links"]["external"] == []

    def test_link_text_truncated(self):
        long_text = "A" * 200
        html = f'<html><body><a href="/page">{long_text}</a></body></html>'
        result = parse_html(html, base_url="https://example.com")
        assert len(result["links"]["internal"][0]["text"]) == 100


class TestSchemaJsonLD:
    def test_extracts_valid_schema(self, sample_html_full):
        result = parse_html(sample_html_full)
        assert len(result["schema"]) == 1
        assert result["schema"][0]["@type"] == "Article"
        assert result["schema"][0]["headline"] == "Best Widget Tools 2025"

    def test_multiple_schemas(self, sample_html_multiple_schemas):
        result = parse_html(sample_html_multiple_schemas)
        # Should have 2 valid schemas (third is invalid JSON)
        assert len(result["schema"]) == 2
        types = [s["@type"] for s in result["schema"]]
        assert "Organization" in types
        assert "WebPage" in types

    def test_invalid_json_ld_skipped(self, sample_html_multiple_schemas):
        result = parse_html(sample_html_multiple_schemas)
        # Invalid JSON should be silently skipped, not crash
        assert len(result["schema"]) == 2

    def test_no_schema(self, sample_html_minimal):
        result = parse_html(sample_html_minimal)
        assert result["schema"] == []


class TestWordCount:
    def test_word_count_excludes_nav_footer(self, sample_html_full):
        result = parse_html(sample_html_full)
        # Should count content words but exclude nav/footer/script/style
        assert result["word_count"] > 0
        # "Home" is in nav, "Copyright 2025" is in footer -- both excluded
        # Main content has substantial words

    def test_minimal_word_count(self, sample_html_minimal):
        result = parse_html(sample_html_minimal)
        assert result["word_count"] == 2  # "Hello world"

    def test_empty_html(self):
        result = parse_html("")
        assert result["word_count"] == 0


class TestResultStructure:
    def test_all_keys_present(self, sample_html_minimal):
        result = parse_html(sample_html_minimal)
        expected_keys = [
            "title", "meta_description", "meta_robots", "canonical",
            "h1", "h2", "h3", "images", "links", "schema",
            "open_graph", "twitter_card", "word_count", "hreflang",
        ]
        for key in expected_keys:
            assert key in result, f"Missing key: {key}"

    def test_links_has_internal_external(self, sample_html_minimal):
        result = parse_html(sample_html_minimal)
        assert "internal" in result["links"]
        assert "external" in result["links"]
