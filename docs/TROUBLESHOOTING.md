# Troubleshooting

## Common Issues

### Skill Not Loading

**Symptom:** `/seo` command not recognized

**Solutions:**

1. Make sure you're running Claude Code from within the 30x-seo directory (or a parent):
```bash
cd /path/to/30x-seo
claude
```

2. Check SKILL.md exists and has proper frontmatter:
```bash
ls skills/30x-seo/SKILL.md
head -5 skills/30x-seo/SKILL.md
```
Should start with `---` followed by YAML.

3. Restart Claude Code.

---

### Python Dependency Errors

**Symptom:** `ModuleNotFoundError: No module named 'requests'`

**Solution:**

```bash
pip install --user beautifulsoup4 requests lxml playwright Pillow urllib3 validators
```

Or install from requirements.txt:
```bash
pip install --user -r requirements.txt
```

---

### Playwright Screenshot Errors

**Symptom:** `playwright._impl._errors.Error: Executable doesn't exist`

**Solution:**
```bash
pip install playwright
playwright install chromium
```

Playwright is optional — without it, visual analysis uses WebFetch as a fallback.

---

### Permission Denied Errors

**Symptom:** `Permission denied` when running scripts

**Solution:**
```bash
chmod +x scripts/*.py
chmod +x hooks/*.py
chmod +x hooks/*.sh
```

---

### Hook Not Triggering

**Symptom:** Schema validation hook not running

**Check:**

1. Verify hook is in settings:
```bash
cat ~/.claude/settings.json
```

2. Ensure correct relative path:
```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "python3 ./hooks/validate-schema.py \"$FILE_PATH\"",
            "exitCodes": { "2": "block" }
          }
        ]
      }
    ]
  }
}
```

3. Test hook directly:
```bash
python3 hooks/validate-schema.py test.html
```

---

### Subagent Not Found

**Symptom:** `Agent 'seo-technical' not found`

**Solution:**

1. Verify agent files exist:
```bash
ls agents/seo-*.md
```

2. Check agent frontmatter:
```bash
head -5 agents/seo-technical.md
```

---

### Timeout Errors

**Symptom:** `Request timed out after 30 seconds`

**Solutions:**

1. The target site may be slow — try again
2. Check your network connection
3. Some sites block automated requests

---

### Schema Validation False Positives

**Symptom:** Hook blocks valid schema

**Check:**

1. Ensure placeholders are replaced
2. Verify @context is `https://schema.org`
3. Check for deprecated types (HowTo, SpecialAnnouncement)
4. Validate at [Google's Rich Results Test](https://search.google.com/test/rich-results)

---

### DataForSEO Auth Errors

**Symptom:** `401 Unauthorized` or `Invalid credentials`

**Check credentials:**

```bash
cat ~/.config/dataforseo/auth | base64 -d
# Should output: your-email:your-password
```

**Recreate auth file:**
```bash
mkdir -p ~/.config/dataforseo
echo -n "your-email:your-password" | base64 > ~/.config/dataforseo/auth
chmod 600 ~/.config/dataforseo/auth
```

---

## Debug Mode

To see detailed output, run scripts directly:

```bash
# Test fetch
python3 scripts/fetch_page.py https://example.com

# Test parse
python3 scripts/parse_html.py page.html --json

# Test screenshot (requires Playwright)
python3 scripts/capture_screenshot.py https://example.com
```

---

## Getting Help

1. **Check the docs:** Review [COMMANDS.md](COMMANDS.md) and [ARCHITECTURE.md](ARCHITECTURE.md)
2. **GitHub Issues:** Report bugs at https://github.com/norahe0304-art/30x-seo/issues
