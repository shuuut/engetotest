#!/usr/bin/env pytest

from playwright.sync_api import Page, expect
import re

def test_requests_cookies(page: Page):
    page.goto("https://engeto.cz")

    # konec nazvu stranky obsahuje "ENGETO"
    expect(page).to_have_title(re.compile("ENGETO$"))

    expect(page.get_by_text("Používáme cookies – web funguje, jak potřebuješ, a zastaví reklamu, která tě nezajímá ")).to_be_visible()

def test_contact_page(page: Page):
    page.goto("https://engeto.cz")
    
    page.get_by_role("button", name = "Souhlasím jen s nezbytnými").click(timeout=1000)
    page.get_by_text("Kontakt", exact=True).first.click(timeout=3000)
    expect(page).to_have_url("https://engeto.cz/kontakt/")
    #mail = page.get_by_text("info@engeto.com")
    #expect(mail).to_have_attribute("href","mailto:info@engeto.com")
    for mail in page.get_by_text("info@engeto.com").all():
        for mail_parent in page.locator("a").filter(has=mail).all():
            expect(mail_parent).to_have_attribute("href", "mailto:info@engeto.com")
def test_terminy(page:Page):
    page.goto("https://engeto.cz")
    page.get_by_role("button", name ="Chápu a přijímám!").click(timeout = 1000)
    page.get_by_text("Termíny").first.click(timeout = 2000)
    expect(page).to_have_url("https://engeto.cz/terminy/")
    page.get_by_role("checkbox", name = "Python").click(timeout = 1000)
    for termin in page.get_by_text("Detail termínu").all():
        if termin.is_visible():
            termin.click(timeout=1000)
            break
    expect(page).to_have_url(re.compile(r"^https://engeto\.cz/product/detail-terminu-python-akademie-\d+-\d+-\d+-\d+-\d+(-\d+)?"))
    page.get_by_text("Přihlas se na termín").first.click(timeout=3000)
    expect(page).to_have_url("https://engeto.cz/cart/")