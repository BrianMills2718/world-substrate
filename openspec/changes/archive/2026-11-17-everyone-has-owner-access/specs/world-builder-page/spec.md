## ADDED Requirements

### Requirement: Everyone has owner access
When the server runs with open access on, every visitor is treated as the owner: worlds and runs are saved to one shared library everyone sees, spending comes from the one owner daily allowance, and the page shows no password control. Turning the setting off restores the owner password.

Source: Brian, 2026-11-17: "A everyone gets owner level."

#### Scenario: everyone-has-owner-access
- **WHEN** open access is on and a person opens the page with no password
- **THEN** the service reports owner mode and open access
- **AND** the page shows no Owner access control and no not-saved notice, and the library is shown
