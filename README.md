# knowledge
A command line for one knowledge base: process a source, name a topic, relate a thing.

## Layers
- **Discovery**: finds what is worth reading.
  - **Inbox**: whatever is found is saved immediately and can be processed whenever.
    - **CLI**: identifiers and open pages, added from the terminal.
    - **Connector**: pages behind a login, added from the browser.
    - **Monitor**: new work found by saved searches, added automatically.
      - Zotero > File > New Feed > From URL
- **Sources**: keeps what was found, in the library.
  - **Archive**: sources that were processed and kept.
- **Knowledge**: says what it means and how it connects.
  - **Notes**: single ideas in one's own words, linked to what is already there.

## Commands
```
knowledge
├── source
│   └── add <url> --topic <topic> [--topic …]
├── topic
│   ├── add <name> [--broader <topic>]
│   ├── rm  <topic>
│   └── list
└── entity
    ├── add  <name> --kind <kind> [--description <text>]
    │                             [--same-as <url>]
    │                             [--url <url>]
    │                             [--alternate-name <text>]
    ├── link <from> <relation> <to>
    ├── rm   <entity>
    └── list
```

## The repository it works on
One repository holds one person's knowledge base; domains are views onto it. `knowledge` finds
the repository by walking up from where it was run, looking for `knowledge/config.toml`.

| Path | Vocabulary | Description |
|---|---|---|
| `knowledge/config.toml` | N/A | the namespace its ids are minted under |
| `knowledge/model/entities.ttl` | schema.org | who and what the knowledge base is made of, and how they relate |
| `knowledge/model/topics.ttl` | SKOS | the controlled vocabulary that tags the sources |
| `knowledge/model/terms.ttl` | SKOS | the vocabulary and acronyms its sources use |
| `knowledge/zotero/library.json` | Zotero | a backup of every source and its metadata |
| `knowledge/zotero/collections.json` | Zotero | a backup of how the library is organised |
| `knowledge/zotero/governance.yml` | N/A | the rules the library follows |

## Development
Run once per clone, so every commit is checked first.
```shell
uv run --locked pre-commit install --install-hooks
```
