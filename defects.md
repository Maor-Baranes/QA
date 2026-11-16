# SauceDemo — Defect Report

Baseline: `standard_user`. Each defect below was found by differentiating another account's behavior against the baseline, then confirmed with an automated Playwright test.
This was due to seeing that standard_user as the only at least seemingly error-free reference.

| ID | User | Title | Severity | Test |
|---|---|---|---|---|
| PD-01 | problem_user | All inventory products show the same broken image | High | `test_problem_user_images_are_unique` |
| PD-02 | problem_user | Not all products can be added to cart | High | `test_problem_user_cannot_add_all_products` |
| ED-01 | error_user | Price (low to high) sort does not sort | Medium | `test_error_user_price_sort_is_broken` |
| ED-02 | error_user | Removing an item from cart does not update the badge | High | `test_error_user_cannot_remove_item` |
| ED-03 | error_user | Last Name field at checkout rejects input | High | `test_error_user_last_name_rejects_input` |
| VD-01 | visual_user | Product image swaps to a broken image after sorting | Medium | `test_visual_user_image_follows_product_after_sort` |
| GD-01 | performance_glitch_user | Login is significantly slower than baseline | Low | `test_performance_glitch_user_login_is_fast` |

---

## PD-01: All inventory products show the same broken image

**User:** problem_user
**Severity:** High
**Test:** `test_problem_user_images_are_unique`

**Steps to reproduce**
1. Log in as `problem_user`
2. View the Inventory page

**Expected**
Each product displays its own distinct image.

**Actual**
All 6 products display `/assets/sl-404-Cq1a9k9X.jpg`.

```
assert 1 == 6
 +  where 1 = len({'/assets/sl-404-Cq1a9k9X.jpg'})
```

---

## PD-02: Not all products can be added to cart

**User:** problem_user
**Severity:** High
**Test:** `test_problem_user_cannot_add_all_products`

**Steps to reproduce**
1. Log in as `problem_user`
2. Click "Add to cart" on every product in order

**Expected**
All 6 buttons respond and the product is added to the cart.

**Actual**
The 4th "Add to cart" button does not respond (click times out).

```
playwright._impl._errors.TimeoutError: Locator.click: Timeout 5000ms exceeded.
waiting for get_by_role("button", name="Add to cart").nth(4)
```

---

## ED-01: Price (low to high) sort does not sort

**User:** error_user
**Severity:** Medium
**Test:** `test_error_user_price_sort_is_broken`

**Steps to reproduce**
1. Log in as `error_user`
2. Select "Price (low to high)" from the sort dropdown

**Expected**
Prices appear in ascending order.

**Actual**
Prices appear in this order: `[29.99, 9.99, 15.99, 49.99, 7.99, 15.99]`.

```
AssertionError: not sorted low to high: [29.99, 9.99, 15.99, 49.99, 7.99, 15.99]
```

---

## ED-02: Removing an item from cart does not update the badge

**User:** error_user
**Severity:** High
**Test:** `test_error_user_cannot_remove_item`

**Steps to reproduce**
1. Log in as `error_user`
2. Add a product to the cart (badge shows 1)
3. Click "Remove" on that product

**Expected**
The badge disappears or shows 0.

**Actual**
The badge still shows 1.

```
AssertionError: Locator expected to have count '0'
Actual value: 1
```

---

## ED-03: Last Name field at checkout rejects input

**User:** error_user
**Severity:** High
**Test:** `test_error_user_last_name_rejects_input`

**Steps to reproduce**
1. Log in as `error_user`
2. Add a product, go to cart, click Checkout
3. Fill the Last Name field

**Expected**
The field holds the entered text.

**Actual**
The field remains empty.