# Architecture

## Components
- `backend-api/` - Laravel 12 + Inertia React
- `feedback-extension/` - Chrome MV3

## Model
- `Client` -> `User`, `Project`
- `Tester` bez kont
- `FeedbackReport` ma `user_id` albo `tester_id`

## Flow
- invite -> join -> token
- feedback -> check -> send

## API
- `GET /api/v1/tester/check`
- `POST /api/v1/tester/feedback`
- `GET /api/v1/projects/check`
- `POST /api/v1/feedback`

## Security
- tokeny hashuj
- invite ma limit / expiry
- waliduj pliki
- signed routes dla jednorazowych linków
