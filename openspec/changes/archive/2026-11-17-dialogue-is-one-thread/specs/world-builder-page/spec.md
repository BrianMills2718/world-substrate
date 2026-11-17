## ADDED Requirements

### Requirement: The dialogue is one thread
The describe stage is a single conversation with one message box and a Run button; talking to the AI continues the same thread instead of opening a separate dialogue.

Source: Brian, 2026-11-17: "the ui should just be more like chatgpt with a run button so that its not really a fully separate dialogue box if you want dialogue its just a continuation of the origianl"

#### Scenario: the-dialogue-is-one-thread
- **WHEN** a person sends a message and the AI answers
- **THEN** the answer, its questions and a draft of the world appear in the thread above the same message box
- **AND** Run builds the latest draft, or the typed text when there is no draft yet
