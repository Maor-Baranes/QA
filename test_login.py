import time

import pytest
from playwright.sync_api import Browser, Page, expect

INVENTORY = "https://www.saucedemo.com/inventory.html"
USERS = ["problem_user", "error_user", "visual_user", "performance_glitch_user"]


def login(page: Page, user: str):
    page.goto("https://www.saucedemo.com")
    page.get_by_placeholder("Username").fill(user)
    page.get_by_placeholder("Password").fill("secret_sauce")
    page.get_by_role("button", name="Login").click()
    expect(page).to_have_url(INVENTORY)
    expect(page.locator(".inventory_item").first).to_be_visible()

def products(page: Page) -> dict:
    """Maps product name to (price, image src)."""
    expect(page.locator(".inventory_item")).to_have_count(6)  # wait for full render
    result = {}
    for item in page.locator(".inventory_item").all():
        name = item.locator(".inventory_item_name").inner_text()
        price = item.locator(".inventory_item_price").inner_text()
        image = item.locator("img").get_attribute("src")
        result[name] = (price, image)
    return result


@pytest.fixture(scope="session")
def standard(browser: Browser) -> dict:
    page = browser.new_page()
    login(page, "standard_user")
    data = products(page)
    page.context.close()
    assert data, "standard_user: no products found, selectors are wrong"
    return data


# Step 1: diff every user against standard_user.
@pytest.mark.parametrize("user", USERS)
def test_diff_from_standard_user(page: Page, standard: dict, user: str):
    login(page, user)
    actual = products(page)
    differences = [name for name in standard if actual.get(name) != standard[name]]
    print(f"\n{user}: {differences or 'no differences'}")


# Step 2: each difference becomes a named defect test.

def test_problem_user_images_are_unique(page: Page):
    login(page, "problem_user")
    images = [image for _, image in products(page).values()]
    assert len(set(images)) == len(images), "products share images"


def test_problem_user_cannot_add_all_products(page: Page):
    login(page, "problem_user")
    while page.get_by_role("button", name="Add to cart").count() > 0:
        page.get_by_role("button", name="Add to cart").first.click()
    expect(page.get_by_role("button", name="Remove")).to_have_count(6)

@pytest.mark.xfail(reason="Known error_user defect: price sort broken", strict=True)
def test_error_user_price_sort_is_broken(page: Page):
    login(page, "error_user")
    page.locator(".product_sort_container").select_option("lohi")
    prices = [float(p.replace("$", "")) for p in page.locator(".inventory_item_price").all_inner_texts()]
    assert prices == sorted(prices), f"not sorted low to high: {prices}"

@pytest.mark.xfail(reason="Known error_user defect: cannot remove item", strict=True)
def test_error_user_cannot_remove_item(page: Page):
    login(page, "error_user")
    page.get_by_role("button", name="Add to cart").first.click()
    expect(page.locator(".shopping_cart_badge")).to_have_text("1")
    page.get_by_role("button", name="Remove").first.click()
    expect(page.locator(".shopping_cart_badge")).to_have_count(0)

@pytest.mark.xfail(reason="Known error_user defect", strict=True)
def test_error_user_last_name_rejects_input(page: Page):
    login(page, "error_user")
    page.get_by_role("button", name="Add to cart").first.click()
    page.locator(".shopping_cart_link").click()
    page.get_by_role("button", name="Checkout").click()
    page.get_by_placeholder("Last Name").fill("User")
    expect(page.get_by_placeholder("Last Name")).to_have_value("User")


def test_visual_user_image_follows_product_after_sort(page: Page, standard: dict):
    login(page, "visual_user")
    page.locator(".product_sort_container").select_option("lohi")
    first = page.locator(".inventory_item").first
    name = first.locator(".inventory_item_name").inner_text()
    image = first.locator("img").get_attribute("src")
    assert image == standard[name][1], f"{name} shows the wrong image after sorting"


def test_performance_glitch_user_login_is_fast(page: Page):
    page.goto("https://www.saucedemo.com")
    page.get_by_placeholder("Username").fill("performance_glitch_user")
    page.get_by_placeholder("Password").fill("secret_sauce")
    start = time.perf_counter()
    page.get_by_role("button", name="Login").click()
    expect(page).to_have_url(INVENTORY)
    elapsed = time.perf_counter() - start
    assert elapsed < 3, f"login took {elapsed:.1f}s"
