# Assumptions used to build the domain models

This records the decisions applied to all nine Mermaid models. The authoritative input is the revised workbook `Gold&Silver Standard.xlsx`, with the sheets `Class - Gold Standard`, `Association - Gold Standard`, and `Class Non-Punish List`. It replaces the original `Gold standard - Classes.xlsx` and `Gold standard - Associations.xlsx` workbooks from the Bragilovski2025 research appendix as the source of the models. Class labels remain exactly as listed in the class sheet. Every association comment includes its workbook wording and cell.

## Workbook legend

The revised workbook marks changes with colors. The models apply them as follows:

| Workbook marking | Meaning | Mermaid representation |
|---|---|---|
| Red fill | Removed | Omitted from the diagram; listed in the `%%` header comments of the model |
| Green fill | Optional | Class: `<<optional>>` stereotype. Association: dashed `..` line instead of `--` |
| Blue text | Added | Included like any other element; marked in a `%%` comment |

Blue text with a green fill means an element that was added as optional. Elements without a marking are required.

## Rules applied to all models

- The association sheet stores endpoints as truncated word stems, such as `('employe', 'schedul')`. Each stem is completed to the class label it abbreviates, and every completion is noted beside the association.
- Singular and plural forms are assumed interchangeable. This is a modeling assumption, not a claim about multiplicity.
- Exact class labels take precedence over association wording, including capitalization.
- Each association row becomes one undirected edge in workbook order. No direction, relationship name, multiplicity, inheritance, attributes, or methods are inferred. Classes without associations are retained.
- Class IDs are internal diagram identifiers. Interpret associations by their displayed class labels and comments.
- With the revised class lists, every association endpoint maps to a class. No `associationOnly` nodes are needed any more.

## Interpretive mappings beyond stems and singular/plural

| Project | Workbook term → class label | Assumption and evidence |
|---|---|---|
| Planningpoker | `estim` → `estimate` (G4, second term of G7) and `estimators` (G6, first term of G7) | The stem fits both classes. The reading of the previous models is kept: estimate–item, game–estimators, estimators–estimate. |
| Recycling | `recyclable wast` → `waste type` (I6) | `recyclable waste` is no longer in the class list, while `waste type` is new. The stories speak of "types of recyclable waste" ([recycling.txt line 6](../1_user_stories/recycling.txt)). |
| Recycling | `event` → `safe disposal events` (I10) | The only event class in the list. Omitted qualifier and singular/plural. |
| Sports | `membership` → `family membership` (M6, M7) | The only membership class in the list. The stories refer to a Family Membership ([sports.txt lines 12–14](../1_user_stories/sports.txt)). |
| Sports | `book` → `booking` (M11–M14) | Verb-like endpoint read as the booking concept, unchanged from the previous models. |
| Supermarket | `discount` → `personal discount` (O18) | The only discount class in the list. Omitted qualifier. |
| Supermarket | `prodcut` → `products` (O18) | Spelling error and singular/plural. |

## Workbook irregularities

- **Grocery E5** repeats E4, `('employe', 'working hour')`. The previous models had employee–complaint in this row; the revised workbook adds manager–complaint in E13 instead. E4 and E5 are drawn as a single association whose comment cites both cells.
- **Supermarket row 13** has two cells: O13 `('custom', 'delivery ')` and P13 `('custom', 'delivery servic')`. O13 is used, giving customer–delivery, because `delivery service` is not in the class list. P13 is documented as an alternative wording.
- **Recycling I11–I13** use the format `user - reward` instead of tuples. They are parsed the same way.
- **Sports M15** (`gym`–`book`) is a new row that is also marked removed, consistent with the removal of the `gym` class. It is omitted.

## Changes from the previous models

| Project | Classes | Associations |
|---|---|---|
| Camperplus | `parentguardians` → `guardians`; `camp group` → `groups`; added `behavior`, `repair` | Added group–facilities, camper–behavior, guardians–forms |
| Fish&Chips | `customer`, `coupons`, `delivery person`, `cash` are now classes; `cashier` is now an optional class; `payment methods` is no longer listed | cashier–payment is optional |
| Grocery | Added `manager` | employee–complaint replaced by a duplicate of E4 (see above); added employee–payments (optional), manager–employee (optional), manager–complaint, manager–message |
| Planningpoker | None | None |
| Recycling | Removed `questions`; `recyclable waste` → `waste type`; `recycling facilities` → `recycling facility`; added `reward`, `activity` | Removed user–questions; added employees–user, employees–safe disposal events (optional), user–reward, user–activity, activity–waste type (optional) |
| School | Added `attendance` | Added class–teacher |
| Sports | Removed `gym`; `payment` is no longer listed; `membership` → `family membership`; `spots` → `spot`; `Payment information` is now a class; added `timeslot` (optional) | Endpoints remapped only |
| Supermarket | `special personal discounts` → `personal discount`; added `payment` (optional); `delivery service` is no longer a node | customer–delivery service → customer–delivery; added order–delivery (optional), payment–order (optional), personal discount–products |
| Ticket | `order` is now a class (previously an `associationOnly` node `orders`) | Endpoints remapped only |

## Non-punish list

The `Class Non-Punish List` sheet names subclasses that should not count as false positives during class evaluation. The guideline used for class identification does not cover subclasses. If a model identifies any concept in a group, the remaining concepts in that group are not treated as false positives. For example, if a model finds medical form, consent form, and registration form, one is labeled correct and the other two are not counted as incorrect.

| Project | Concept | Accepted subclasses and synonyms |
|---|---|---|
| Camperplus | form | medicalForm, consentform, registrationForm, consent form, medical form, registration form |
| Sports | room | practicearea, practice area, free practice area |
| School | material | text, video, picture |
| School | question | open question, multiple-choice question |

Each group is also listed in the header comments of the corresponding Mermaid file.

## Expected model counts

| Project | Classes (optional) | Associations (optional) |
|---|---:|---:|
| Camperplus | 19 (0) | 26 (0) |
| Fish&Chips | 9 (1) | 8 (1) |
| Grocery | 10 (0) | 11 (2) |
| Planningpoker | 6 (0) | 6 (0) |
| Recycling | 10 (0) | 10 (2) |
| School | 18 (0) | 24 (0) |
| Sports | 13 (1) | 12 (0) |
| Supermarket | 12 (1) | 16 (2) |
| Ticket | 10 (0) | 13 (0) |
| **Total** | **107 (3)** | **126 (7)** |

## Review questions

- Confirm that `waste type` replaces `recyclable waste` in Recycling I6.
- Confirm that Grocery E5 is an intentional duplicate rather than a mistyped employee–complaint row.
- Confirm that O13 rather than P13 is the intended Supermarket row 13 association.
