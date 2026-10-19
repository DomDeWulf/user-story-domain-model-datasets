# Assumptions used to reconcile the domain-model workbooks

This records the normalization decisions applied to all nine Mermaid models. The authoritative inputs are `Gold standard - Classes.xlsx` and `Gold standard - Associations.xlsx`, both `Sheet1`, from the Bragilovski2025 research appendix. Class labels remain exactly as listed in the Classes workbook. Every association comment includes its original wording and workbook cell range.

## Rules applied to all models

- Singular and plural forms are assumed interchangeable. This is a modeling assumption, not a change to the original workbooks or a claim about multiplicity. Every occurrence of a changed endpoint is annotated in its Mermaid source.
- Exact class terms take precedence over association wording, including capitalization. No global stemming, case folding, synonym replacement, or abbreviation expansion is applied.
- Each source association row remains one undirected `--` edge in its original order. No direction, relationship name, multiplicity, inheritance, attributes, or methods are inferred. Classes without associations are retained.
- If no justified equivalent class exists, the endpoint remains an `associationOnly` node. These are diagram scaffolding and must be excluded from gold-standard class evaluation.
- Class IDs are internal diagram identifiers. Interpret associations using their displayed class labels and comments.

## Interpretive mappings beyond singular/plural

| Project | Association term → class term | Assumption and evidence |
|---|---|---|
| Camperplus | `group` → `camp group` | Explicitly requested equivalence with camper group. The Classes workbook says `camp group`. The user also mentioned `grou`, but that spelling does not occur in the source workbooks. |
| Sports | `book` → `booking` | Treat the verb-like endpoint as the reservation concept, rather than a separate entity. Stories describe booking a lesson, training session, and spot, and refer to a canceled booking: [sports.txt lines 18, 21, 23, 56–57](https://github.com/DomDeWulf/user-story-domain-model-datasets/blob/main/1_user_stories/sports.txt#L18). This is an interpretation, not an explicit equivalence in the workbooks. |
| Supermarket | `personal discount` → `special personal discounts` | Assume the omitted qualifier refers to the same personalized discount concept. Stories explicitly name a special personal discount and special personal discounts: [supermarket.txt lines 11–12](https://github.com/DomDeWulf/user-story-domain-model-datasets/blob/main/1_user_stories/supermarket.txt#L11). This includes both qualifier expansion and singular/plural normalization. |

## Ambiguities deliberately retained

- **Sports:** `Payment information` is absent from the class list and remains `associationOnly`. It is not assumed equivalent to `payment`: banking/payment details may differ from a payment. See [sports.txt lines 3 and 11](https://github.com/DomDeWulf/user-story-domain-model-datasets/blob/main/1_user_stories/sports.txt#L3). Its original capitalization is retained.
- **Supermarket:** `delivery service` remains `associationOnly`. The stories distinguish a subscription-based service from individual deliveries, so equivalence to `delivery` is not established. See [supermarket.txt lines 13 and 33–36](https://github.com/DomDeWulf/user-story-domain-model-datasets/blob/main/1_user_stories/supermarket.txt#L13).
- **Fish & Chips:** `customer`, `coupons`, `delivery person`, `cash`, and `cashier` have no matching Classes workbook entries. All five remain `associationOnly`. In particular, `cash` is not merged into the broader `payment methods` class.
- **Ticket:** neither `order` nor `orders` appears in the Classes workbook. Apply the same singular/plural assumption to these endpoints and use `orders`, the first encountered source form, for one shared `associationOnly` node. This joins the user–orders, ticket–orders, and order–payment rows without inventing a gold-standard class.

## Complete mapping inventory

Rows below refer to `Sheet1` in the Associations workbook. Each mapping is also documented beside every affected association in the Mermaid file.

| Project | Source term | Diagram term | Source rows | Basis |
|---|---|---|---|---|
| Camperplus (A:B) | `parentguardian` | `parentguardians` | 3, 8 | Singular/plural |
| Camperplus (A:B) | `form` | `forms` | 4 | Singular/plural |
| Camperplus (A:B) | `group` | `camp group` | 6, 9, 11, 13, 17 | Shortened term; user-specified equivalence |
| Camperplus (A:B) | `rule` | `rules` | 7 | Singular/plural |
| Camperplus (A:B) | `schedule` | `schedules` | 9, 18 | Singular/plural |
| Camperplus (A:B) | `photo` | `photos` | 10 | Singular/plural |
| Camperplus (A:B) | `facility` | `facilities` | 12, 15 | Singular/plural |
| Camperplus (A:B) | `activity` | `activities` | 12, 13, 18, 21 | Singular/plural |
| Camperplus (A:B) | `payment` | `payments` | 22 | Singular/plural |
| Fish&Chips (C:D) | `order` | `orders` | 3, 5, 6, 9 | Singular/plural |
| Fish&Chips (C:D) | `product` | `products` | 4 | Singular/plural |
| Grocery (E:F) | `contract` | `contracts` | 8 | Singular/plural |
| Grocery (E:F) | `certificate` | `certificates` | 9 | Singular/plural |
| Grocery (E:F) | `payment` | `payments` | 10 | Singular/plural |
| Planningpoker (G:H) | `estimator` | `estimators` | 6, 7 | Singular/plural |
| Recycling (I:J) | `question` | `questions` | 3 | Singular/plural |
| Recycling (I:J) | `complaint` | `complaints` | 5 | Singular/plural |
| Recycling (I:J) | `recycling facility` | `recycling facilities` | 6, 7 | Singular/plural |
| School | — | — | — | All endpoint terms match exactly. |
| Sports (M:N) | `room` | `rooms` | 3 | Singular/plural |
| Sports (M:N) | `lesson` | `lessons` | 3, 4, 13 | Singular/plural |
| Sports (M:N) | `training session` | `training sessions` | 10, 14 | Singular/plural |
| Sports (M:N) | `book` | `booking` | 11, 12, 13, 14 | Verb/noun interpretation |
| Sports (M:N) | `spot` | `spots` | 12 | Singular/plural |
| Supermarket (O:P) | `product` | `products` | 6, 8, 9, 10, 12 | Singular/plural |
| Supermarket (O:P) | `recipe` | `recipes` | 12 | Singular/plural |
| Supermarket (O:P) | `personal discount` | `special personal discounts` | 14 | Omitted qualifier and singular/plural |
| Ticket (Q:R) | `order` | `orders` | 7 | Singular/plural; shared associationOnly label |
| Ticket (Q:R) | `event` | `events` | 8, 9, 10, 11 | Singular/plural |
| Ticket (Q:R) | `artist` | `artists` | 10 | Singular/plural |
| Ticket (Q:R) | `resellers` | `reseller` | 13 | Singular/plural |
| Ticket (Q:R) | `tickets` | `ticket` | 13 | Singular/plural |

## Expected model counts

| Project | Gold-standard classes | associationOnly nodes | Associations |
|---|---:|---:|---:|
| Camperplus | 17 | 0 | 23 |
| Fish&Chips | 5 | 5 | 8 |
| Grocery | 9 | 0 | 8 |
| Planningpoker | 6 | 0 | 6 |
| Recycling | 9 | 0 | 6 |
| School | 17 | 0 | 23 |
| Sports | 13 | 1 | 12 |
| Supermarket | 11 | 1 | 13 |
| Ticket | 9 | 1 | 13 |
| **Total** | **96** | **8** | **112** |

## Review questions

- Confirm the interpretive mappings `book` → `booking` and `personal discount` → `special personal discounts` if strict replication of the authors’ intended semantics is required.
- Decide whether `Payment information` and `delivery service` should eventually map to existing classes or remain distinct; the current models retain them explicitly.
- Confirm that merging Ticket’s `order`/`orders` into a shared association-only node matches the intended evaluation protocol.

The original workbooks remain authoritative. These curated diagrams document their reconciliation decisions so that reviewers can reverse individual assumptions without losing the source associations.
