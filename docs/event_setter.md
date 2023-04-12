# Missing Event Setter

## Configuration
* Check: `pess-event-setter`
* Severity: `Low`
* Confidence: `Medium`

## Description
The detector sees if a contract contains a setter that does not emit an event.

## Vulnerable Scenario
[test scenario](../tests/event_setter_test.sol)

## Recommendation
Setters must emit events.