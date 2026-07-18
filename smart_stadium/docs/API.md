# API Reference

Base URL: `/api/v1`
All responses use the envelope: `{"success": bool, "message": str, "data": ...}`.
Interactive, always-up-to-date docs are served at `/docs` (Swagger) and `/redoc`.

## Health Check
| Method | Path | Description |
|---|---|---|
| GET | `/health` | API + database liveness check |

## AI Fan Assistant
| Method | Path | Description |
|---|---|---|
| POST | `/assistant/faq` | Add a knowledge-base FAQ entry |
| GET | `/assistant/faq` | List FAQ entries (optional `category`) |
| POST | `/assistant/ask` | Ask a natural-language question |
| GET | `/assistant/history` | Recent chat history |

## Stadium Navigation
| Method | Path | Description |
|---|---|---|
| POST | `/navigation/points` | Create a navigation point |
| GET | `/navigation/points` | List points (filter by `category`, `zone`) |
| GET | `/navigation/points/{point_id}` | Get a point by ID |
| GET | `/navigation/route?origin_id=&destination_id=` | Compute route/distance between two points |

## Smart Ticket (QR Code)
| Method | Path | Description |
|---|---|---|
| POST | `/tickets` | Issue a ticket (generates a real QR code) |
| GET | `/tickets` | List tickets (optional `match_id`) |
| GET | `/tickets/{ticket_id}` | Get ticket by ID |
| POST | `/tickets/verify` | Verify QR code and check the holder in |
| POST | `/tickets/{ticket_id}/cancel` | Cancel a ticket |

## Live Match Information & Match Schedule
| Method | Path | Description |
|---|---|---|
| POST | `/matches` | Create a match |
| GET | `/matches` | List matches (optional `status`) |
| GET | `/matches/live` | Currently live/halftime matches |
| GET | `/matches/schedule` | Upcoming scheduled matches |
| GET | `/matches/{match_id}` | Get match by ID |
| PATCH | `/matches/{match_id}` | Update live score / status / summary |
| DELETE | `/matches/{match_id}` | Delete a match |

## Crowd Density Monitoring
| Method | Path | Description |
|---|---|---|
| POST | `/crowd` | Record a density reading for a zone |
| GET | `/crowd/latest` | Latest reading for every zone |
| GET | `/crowd/{zone}` | Latest reading for one zone |
| GET | `/crowd/{zone}/history` | Historical readings for a zone |

## Smart Parking
| Method | Path | Description |
|---|---|---|
| POST | `/parking/slots` | Create a parking slot |
| GET | `/parking/slots` | List slots (filter by `zone`, `status`) |
| GET | `/parking/availability` | Availability summary |
| POST | `/parking/bookings` | Book a slot |
| POST | `/parking/bookings/{booking_id}/release` | Release a booking |

## Food & Beverage
| Method | Path | Description |
|---|---|---|
| POST | `/food/menu` | Add a menu item |
| GET | `/food/menu` | List menu items |
| POST | `/food/orders` | Place a multi-item order |
| GET | `/food/orders` | List orders (optional `status`) |
| GET | `/food/orders/{order_id}` | Get order by ID |
| PATCH | `/food/orders/{order_id}/status` | Update order status |

## Weather Alerts
| Method | Path | Description |
|---|---|---|
| POST | `/weather` | Issue a weather alert |
| GET | `/weather` | List alerts (optional `active_only`) |
| GET | `/weather/{alert_id}` | Get alert by ID |
| POST | `/weather/{alert_id}/deactivate` | Deactivate an alert |

## Emergency SOS
| Method | Path | Description |
|---|---|---|
| POST | `/sos` | Raise an emergency SOS request |
| GET | `/sos` | List SOS requests (optional `status`) |
| GET | `/sos/{sos_id}` | Get SOS request by ID |
| PATCH | `/sos/{sos_id}/status` | Update status (open → acknowledged → resolved) |

## Lost & Found
| Method | Path | Description |
|---|---|---|
| POST | `/lost-found` | Report a lost or found item |
| GET | `/lost-found` | List items (filter by `item_type`, `status`) |
| GET | `/lost-found/search?keyword=` | Search items by keyword |
| GET | `/lost-found/{item_id}` | Get item by ID |
| PATCH | `/lost-found/{item_id}/status` | Update item status |

## Notifications
| Method | Path | Description |
|---|---|---|
| POST | `/notifications` | Broadcast a notification |
| GET | `/notifications` | List notifications (filter by `category`, `unread_only`) |
| POST | `/notifications/{notification_id}/read` | Mark as read |

## Seat Finder
| Method | Path | Description |
|---|---|---|
| POST | `/seats` | Register a seat |
| GET | `/seats` | List/find seats (filter by `section`, `available_only`, `accessible_only`) |
| GET | `/seats/{seat_number}` | Find a seat by number |
| PATCH | `/seats/{seat_number}/occupancy?occupied=` | Update occupancy |

## Stadium Information
| Method | Path | Description |
|---|---|---|
| POST | `/stadium-info` | Create an info entry |
| GET | `/stadium-info` | List all info entries |
| GET | `/stadium-info/amenities` | List amenities (optional `category`) |
| POST | `/stadium-info/amenities` | Add an amenity |
| GET | `/stadium-info/{key}` | Get info entry by key |
| PUT | `/stadium-info/{key}` | Update info entry |

## Feedback
| Method | Path | Description |
|---|---|---|
| POST | `/feedback` | Submit feedback (1-5 rating) |
| GET | `/feedback` | List feedback (optional `category`) |
| GET | `/feedback/summary` | Average rating summary |

## Analytics
| Method | Path | Description |
|---|---|---|
| GET | `/analytics/dashboard` | Full cross-module dashboard |
| GET | `/analytics/tickets` | Ticket analytics |
| GET | `/analytics/matches` | Match analytics |
| GET | `/analytics/parking` | Parking analytics |
| GET | `/analytics/food` | Food & beverage analytics |
| GET | `/analytics/crowd` | Crowd density analytics |
| GET | `/analytics/safety` | SOS & lost-found analytics |
| GET | `/analytics/feedback` | Feedback analytics |

## Admin APIs
All routes below require header `X-Admin-Key: <ADMIN_API_KEY>`.

| Method | Path | Description |
|---|---|---|
| GET | `/admin/overview` | System-wide counts snapshot |
| GET | `/admin/dashboard` | Full analytics dashboard |
| DELETE | `/admin/reset-database` | Wipe transactional data (tickets, bookings, orders, SOS, lost & found, notifications, feedback) |

## Error Format

All errors share the same envelope:

```json
{
  "success": false,
  "message": "Ticket with id '42' was not found.",
  "data": null
}
```

Validation errors additionally populate `data` with a list of `{"field": ..., "message": ...}` objects.
