# 📸 Google Maps Photos API: every place photo as clean JSON

Pull every photo Google Maps holds for a business or landmark, as structured JSON. Type a place name and get back full-size image URLs, thumbnails, gallery positions, and a stable photo ID for each one.

**Actor:** [Google Maps Photos API on Apify Store](https://apify.com/johnvc/google-maps-photos-api?fpr=9n7kx3)

## Video Walkthrough

https://www.youtube.com/watch?v=jREWahDGhJM

## Quick Start

```bash
git clone https://github.com/johnisanerd/Apify-Google-Maps-Photos-API.git
cd Apify-Google-Maps-Photos-API
cp .env.example .env          # paste your Apify token
uv sync
uv run google-maps-photos-api-example.py
```

Get a free Apify API key at [apify.com](https://apify.com?fpr=9n7kx3).

## Why Use This Google Maps Photos API?

- **No place ID needed.** Search by name, or by category and city. Paste a Google Maps URL if you have one. Identifiers work too, and skip the search charge.
- **Filter to one gallery section.** Menu, food and drink, vibe, by owner, videos, or Street View and 360.
- **Stable photo IDs.** Every row carries one, so a re-run updates rather than duplicates.
- **Category discovery built in.** Each place contributes a summary row listing every gallery section it offers, with the ID to filter by.

## Features

| Feature | Detail |
|---|---|
| Search by name | `searchTerm` takes a business name or a category plus a city |
| Google Maps URLs | `placeUrls` parses the identifier out of the link locally, no lookup |
| Place identifiers | `dataId` and `dataIds` accept the hex pair or a `fid` from a places search |
| Category filter | 8 sections; 5 universal, 3 on food and drink venues |
| Bulk | `maxPlacesPerSearch` sweeps a whole neighbourhood in one run |
| Localization | `hl` sets the interface language |

## Usage Examples

Search a neighbourhood and pull food photos for the top five matches:

```python
run_input = {
    "searchTerm": "coffee shops in Austin, TX",
    "maxPlacesPerSearch": 5,
    "photoCategory": "food_and_drink",
    "maxPhotosPerPlace": 40,
}
```

Street View and 360 panoramas for one place:

```python
run_input = {"searchTerm": "Blanton Museum of Art, Austin TX", "photoCategory": "street_view"}
```

Skip the search charge with identifiers you already have:

```python
run_input = {"dataIds": ["0x8644b5554461664d:0xbc4ff333ec9ad1ad"], "maxPhotosPerPlace": 20}
```

## Input Parameters

| Parameter | Type | Description |
|---|---|---|
| `searchTerm` | string | Find a place by name, or by category and city. Billed per search. |
| `searchTerms` | array | Several searches in one run. |
| `maxPlacesPerSearch` | integer | How many matches per search to fetch photos for. Default 3, max 20. |
| `placeUrls` | array | Google Maps place URLs. Parsed locally, no search charge. |
| `dataId` / `dataIds` | string / array | Place identifiers. No search charge. |
| `maxPhotosPerPlace` | integer | Default 20. Photos arrive in blocks of 20. |
| `photoCategory` | select | all, latest, videos, by_owner, street_view, menu, food_and_drink, vibe |
| `categoryId` | string | A venue-specific section, such as one dish. Overrides `photoCategory`. |
| `hl` | string | Two-letter interface language. Default `en`. |

## Output Format

One row per photo:

```json
{
  "result_type": "photo",
  "data_id": "0x8644b5554461664d:0xbc4ff333ec9ad1ad",
  "place_title": "Mozart's Coffee Roasters",
  "position": 1,
  "image": "https://lh3.googleusercontent.com/gps-cs-s/...=w608-h342-k-no",
  "thumbnail": "https://lh3.googleusercontent.com/gps-cs-s/...=w203-h114-k-no",
  "photo_id": "CIABIhAhgrI-VHBBnTZQYGq3jqot",
  "fetched_at": "2026-08-04T00:24:39.188574+00:00"
}
```

Plus one unbilled summary row per place, which is how you discover its gallery sections:

```json
{
  "result_type": "place_summary",
  "place_title": "Mozart's Coffee Roasters",
  "photos_returned": 20,
  "pages_fetched": 1,
  "place_categories": [
    { "title": "Menu", "id": "CgIYIQ" },
    { "title": "Street View & 360", "id": "CgIgARICCAI" }
  ]
}
```

Captions, EXIF, contributor names, and upload dates are not returned.

## Install in Claude Cowork Desktop

![Install in Claude Cowork Desktop](https://raw.githubusercontent.com/johnisanerd/ApifyPublicData/main/assets/guides/install_mcp_into_claude_desktop.png)

Cowork is the desktop app's automation mode. To give it the Google Maps Photos API as a tool, add the Apify MCP server as a connector.

1. Open the Claude desktop app and go to **Settings → Connectors** (or **Settings → Developer → Edit Config** to edit `claude_desktop_config.json` directly).
   - macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
   - Windows: `%APPDATA%\Claude\claude_desktop_config.json`
2. Add the Apify MCP server, preloaded with only this Actor:

```json
{
  "mcpServers": {
    "apify": {
      "command": "npx",
      "args": [
        "-y",
        "mcp-remote",
        "https://mcp.apify.com/?tools=actors,docs,johnvc/google-maps-photos-api"
      ]
    }
  }
}
```

3. Restart the app. When Cowork first calls the tool, complete the OAuth prompt in your browser, or add your Apify API token in the connector settings to skip OAuth.
4. In a Cowork chat, confirm the tool is available and ask it to run the Google Maps Photos API.

Download the desktop app and start a free trial: https://claude.ai/referral/uIlpa7nPLg
More help: https://docs.apify.com/platform/integrations/claude-desktop

## Install in Claude Code

![Install in Claude Code](https://raw.githubusercontent.com/johnisanerd/ApifyPublicData/main/assets/guides/install_mcp_into_claude_code.png)

Claude Code is the command-line tool. Add the Actor's MCP server with one command:

```bash
claude mcp add --transport http apify \
  "https://mcp.apify.com/?tools=actors,docs,johnvc/google-maps-photos-api"
```

To use a token instead of browser OAuth:

```bash
claude mcp add --transport http apify \
  "https://mcp.apify.com/?tools=actors,docs,johnvc/google-maps-photos-api" \
  --header "Authorization: Bearer YOUR_APIFY_TOKEN"
```

Then verify with `claude mcp list`, or run `/mcp` inside a session. Ask Claude Code to call the Google Maps Photos API.

Try Claude Code free: https://claude.ai/referral/uIlpa7nPLg
Claude Code MCP docs: https://code.claude.com/docs/en/mcp

## Install in Claude (website)

![Install in Claude (website)](https://raw.githubusercontent.com/johnisanerd/ApifyPublicData/main/assets/guides/install_mcp_into_claude_ai.png)

On claude.ai you add Apify as a connector, then enable just this Actor's tool.

1. Go to **Settings → Connectors → Browse connectors** and search for **Apify MCP server**. Install it (enable or update if prompted).
2. When connecting, authenticate with your Apify API token, and enable the tool `johnvc/google-maps-photos-api`.
3. In any chat, open **+ → Connectors** and turn on **Apify**.
4. Alternatively, choose **Add custom connector** and paste the full MCP URL `https://mcp.apify.com/?tools=actors,docs,johnvc/google-maps-photos-api`, using OAuth when prompted.
5. Ask Claude to run the Google Maps Photos API.

Open Claude on the web: https://claude.ai/referral/uIlpa7nPLg

## Install in Cursor

![Install in Cursor](https://raw.githubusercontent.com/johnisanerd/ApifyPublicData/main/assets/guides/install_mcp_into_cursor.png)

Cursor reads MCP servers from a project file at `.cursor/mcp.json`.

1. In your project, create `.cursor/mcp.json`:

```json
{
  "mcpServers": {
    "apify": {
      "url": "https://mcp.apify.com/?tools=actors,docs,johnvc/google-maps-photos-api"
    }
  }
}
```

2. If you prefer token auth over browser OAuth, add a header:

```json
{
  "mcpServers": {
    "apify": {
      "url": "https://mcp.apify.com/?tools=actors,docs,johnvc/google-maps-photos-api",
      "headers": { "Authorization": "Bearer YOUR_APIFY_TOKEN" }
    }
  }
}
```

3. Open **Cursor → Settings → MCP** and confirm the **apify** server is connected (green dot).
4. In Composer or Chat, ask Cursor to call the Google Maps Photos API.

New to Cursor? Get it here: https://cursor.com/referral?code=XQP4VBLI3NNX

## Install in ChatGPT

![Install in ChatGPT](https://raw.githubusercontent.com/johnisanerd/ApifyPublicData/main/assets/guides/install_mcp_into_ChatGPT.png)

ChatGPT connects to the Apify MCP server through Developer mode (available on ChatGPT Pro, Plus, Business, Enterprise, and Education plans).

1. Click your profile icon, then go to **Settings > Apps**. If you do not see a **Create app** button, open **Advanced settings** and enable **Developer mode**.
2. Click **Create app** and fill out the form:
   - **Name:** Apify
   - **MCP Server URL:** `https://mcp.apify.com/?tools=actors,docs,johnvc/google-maps-photos-api`
   - **Authentication:** OAuth
3. Click **Create** and authorize the connection with Apify.
4. To use the app in a conversation, click **+** in the chat, choose **Developer mode**, and select **Apify**.

More help: https://docs.apify.com/platform/integrations/mcp

---

[**Made with care**](https://apify.com/johnvc?fpr=9n7kx3)

*Use the Google Maps Photos API to power local lead lists, market research, and place data for your product or AI agent.*

## Featured Tasks

Ready-to-run examples on the Apify Store, each targeting one local-data use case:

- [Extract local business leads from Google Maps by API](https://apify.com/johnvc/google-maps-photos-api/examples/extract-local-business-leads-from-google-maps-by-api?fpr=9n7kx3)
- [Extract phone numbers from Google Maps by zip code](https://apify.com/johnvc/google-maps-photos-api/examples/extract-phone-numbers-from-google-maps-by-zip-code?fpr=9n7kx3)
- [Find roofing contractor leads in Tampa with phone numbers](https://apify.com/johnvc/google-maps-photos-api/examples/find-roofing-contractor-leads-in-tampa-with-phone-numbers?fpr=9n7kx3)
- [Build a list of med spas in Miami with phone numbers](https://apify.com/johnvc/google-maps-photos-api/examples/build-a-list-of-med-spas-in-miami-with-phone-numbers?fpr=9n7kx3)
- [Generate local leads in Claude via Google Maps MCP](https://apify.com/johnvc/google-maps-photos-api/examples/generate-local-leads-in-claude-via-google-maps-mcp?fpr=9n7kx3)
- [Export Google Maps Places to CSV](https://apify.com/johnvc/google-maps-photos-api/examples/export-google-maps-places-to-csv?fpr=9n7kx3)

Last Updated: 2026.08.08
