# knowledge
A command line for one knowledge base: capture a source, name a topic, relate a thing.

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
One repository holds one domain, and one collection in the library holds its sources. `knowledge` finds
the repository by walking up from where it was run, looking for a `knowledge/` directory.

| Path | Vocabulary | Description |
|---|---|---|
| `knowledge/model/entities.ttl` | schema.org | who and what the domain is made of, and how they relate |
| `knowledge/model/topics.ttl` | SKOS | the controlled vocabulary that tags the sources |
| `knowledge/model/terms.ttl` | SKOS | the vocabulary and acronyms the domain's documents use |
| `knowledge/zotero/library.json` | Zotero | a backup of every source and its metadata |
| `knowledge/zotero/collections.json` | Zotero | a backup of how the library is organised |
| `knowledge/zotero/governance.yml` | — | the rules the library follows |
