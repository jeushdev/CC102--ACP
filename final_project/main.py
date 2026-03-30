import os
from collections import Counter

import flet as ft

import data_manager
import engine as engine


def _format_amount(value):
    try:
        number = float(value)
    except (TypeError, ValueError):
        return str(value)

    return str(int(number)) if number.is_integer() else f"{number:.2f}"


def main(page: ft.Page):
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    BG_COLOR = "#0B1220"
    SURFACE_COLOR = "#121C2E"
    SURFACE_ALT = "#17243A"
    ACCENT_COLOR = "#21C48D"
    ACCENT_DARK = "#129A6C"
    TEXT_PRIMARY = "#E8EEF8"
    TEXT_SECONDARY = "#9FB0CA"
    BORDER_COLOR = "#233551"
    COOKABLE_CARD = "#1D5A48"
    LOCKED_CARD = "#6D3E2D"
    TAB_STRIP_BG = "#1B2B45"
    HEADER_GRADIENT_START = "#223A5E"
    HEADER_GRADIENT_END = "#14263F"

    page.title = "Kusina Tavern"
    page.window_width = 1100
    page.window_height = 820
    page.padding = 0
    page.bgcolor = BG_COLOR
    page.fonts = {
        "Inter": "assets/fonts/Inter/Inter.ttf",
        "Metamorphous": "assets/fonts/Metamorphous/Metamorphous-Regular.ttf",
    }
    page.theme_mode = ft.ThemeMode.DARK

    base_text_style = ft.TextStyle(color=TEXT_PRIMARY, font_family="Inter")
    app_text_theme = ft.TextTheme(
        body_large=base_text_style,
        body_medium=base_text_style,
        body_small=base_text_style,
        display_large=base_text_style,
        display_medium=base_text_style,
        display_small=base_text_style,
        headline_large=base_text_style,
        headline_medium=base_text_style,
        headline_small=base_text_style,
        label_large=base_text_style,
        label_medium=base_text_style,
        label_small=base_text_style,
        title_large=base_text_style,
        title_medium=base_text_style,
        title_small=base_text_style,
    )
    app_button_style = ft.ButtonStyle(
        color=TEXT_PRIMARY,
        bgcolor={"": ACCENT_COLOR, ft.ControlState.HOVERED: ACCENT_DARK},
        shape=ft.RoundedRectangleBorder(radius=12),
        padding=ft.padding.symmetric(horizontal=18, vertical=12),
    )

    page.theme = ft.Theme(
        font_family="Inter",
        text_theme=app_text_theme,
        primary_text_theme=app_text_theme,
        button_theme=ft.ButtonTheme(style=app_button_style),
        text_button_theme=ft.TextButtonTheme(style=app_button_style),
        filled_button_theme=ft.FilledButtonTheme(style=app_button_style),
        tab_bar_theme=ft.TabBarTheme(
            label_color=TEXT_PRIMARY,
            unselected_label_color=TEXT_SECONDARY,
            indicator_color=ACCENT_COLOR,
        ),
        hint_color=TEXT_SECONDARY,
    )

    def make_button(label: str, on_click=None):
        return ft.FilledButton(label, on_click=on_click, style=app_button_style, height=42)

    pantry_list = ft.Column(spacing=10, scroll=ft.ScrollMode.AUTO, expand=True)
    available_recipes_list = ft.ResponsiveRow(spacing=12, run_spacing=12)
    locked_recipes_list = ft.ResponsiveRow(spacing=12, run_spacing=12)
    search_results_list = ft.ResponsiveRow(spacing=12, run_spacing=12)
    history_list = ft.Column(spacing=8)
    achievements_list = ft.Column(spacing=6)

    item_name_input = ft.TextField(
        label="Item name",
        hint_text="e.g., egg",
        autofocus=True,
        text_style=base_text_style,
        label_style=base_text_style,
        hint_style=base_text_style,
    )
    item_amount_input = ft.TextField(
        label="Amount",
        hint_text="e.g., 2",
        keyboard_type=ft.KeyboardType.NUMBER,
        text_style=base_text_style,
        label_style=base_text_style,
        hint_style=base_text_style,
    )
    item_unit_input = ft.TextField(
        label="Unit",
        hint_text="e.g., pc, g, ml",
        text_style=base_text_style,
        label_style=base_text_style,
        hint_style=base_text_style,
    )
    all_recipe_search_input = ft.TextField(
        label="Search recipe",
        hint_text="e.g., adobo, egg, tortang",
        on_submit=lambda e: search_all_recipes(),
        text_style=base_text_style,
        label_style=base_text_style,
        hint_style=base_text_style,
    )
    all_recipe_search_status = ft.Text("Showing all recipes.", color=TEXT_SECONDARY)

    status_text = ft.Text("", color=TEXT_SECONDARY)

    pantry_total_items = ft.Text("0", size=24, weight=ft.FontWeight.BOLD, color=TEXT_PRIMARY)
    recipe_ready_count = ft.Text("0", size=18, weight=ft.FontWeight.BOLD, color=TEXT_PRIMARY)
    recipe_locked_count = ft.Text("0", size=18, weight=ft.FontWeight.BOLD, color=TEXT_PRIMARY)
    history_total_cooks = ft.Text("0", size=18, weight=ft.FontWeight.BOLD, color=TEXT_PRIMARY)
    history_unique_recipes = ft.Text("0", size=18, weight=ft.FontWeight.BOLD, color=TEXT_PRIMARY)
    history_top_recipe = ft.Text("-", size=18, weight=ft.FontWeight.BOLD, color=TEXT_PRIMARY)

    def stat_tile(label: str, value_control: ft.Text, icon):
        return ft.Container(
            col={"sm": 6, "md": 3},
            content=ft.Container(
                content=ft.Row(
                    [
                        ft.Container(
                            content=ft.Icon(icon, color=ACCENT_COLOR, size=20),
                            bgcolor=SURFACE_ALT,
                            border_radius=10,
                            padding=10,
                        ),
                        ft.Column(
                            [
                                ft.Text(label, size=12, color=TEXT_SECONDARY),
                                value_control,
                            ],
                            spacing=2,
                        ),
                    ],
                    spacing=10,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                bgcolor=SURFACE_ALT,
                border=ft.Border.all(1, BORDER_COLOR),
                border_radius=14,
                padding=12,
            ),
        )

    pantry_stats_row = ft.ResponsiveRow(
        [
            stat_tile("Different Ingredients", pantry_total_items, ft.Icons.INVENTORY_2),
        ],
        spacing=10,
        run_spacing=10,
    )

    def show_status(message: str, ok: bool = True):
        status_text.value = message
        status_text.color = ACCENT_COLOR if ok else ft.Colors.RED_300

    def load_pantry():
        return data_manager.load_data(data_manager.PANTRY_FILE) or {}

    def load_history():
        history = data_manager.load_data(data_manager.HISTORY_FILE)
        return history if isinstance(history, list) else []

    def load_cookbook():
        return data_manager.load_data(data_manager.RECIPES_FILE) or {}

    def refresh_pantry_view():
        pantry = load_pantry()
        pantry_list.controls.clear()

        def amount_as_float(info: dict) -> float:
            try:
                return float(info.get("amount", 0))
            except (TypeError, ValueError):
                return 0.0

        pantry_total_items.value = str(len(pantry))

        if not pantry:
            pantry_list.controls.append(ft.Text("Your pantry is empty. Add loot to begin.", color=TEXT_SECONDARY))
            return

        for item_name in sorted(pantry.keys()):
            info = pantry[item_name]
            pantry_list.controls.append(
                ft.Container(
                    content=ft.Row(
                        [
                            ft.Row(
                                [
                                    ft.Container(
                                        content=ft.Icon(ft.Icons.KITCHEN, color=ACCENT_COLOR, size=18),
                                        bgcolor=SURFACE_ALT,
                                        border_radius=8,
                                        padding=8,
                                    ),
                                    ft.Column(
                                        [
                                            ft.Text(item_name.capitalize(), color=TEXT_PRIMARY, weight=ft.FontWeight.W_600),
                                        ],
                                        spacing=2,
                                    ),
                                ],
                                spacing=10,
                            ),
                            ft.Text(
                                f"{_format_amount(info.get('amount', 0))} {info.get('unit', '')}".strip(),
                                color=TEXT_PRIMARY,
                                size=18,
                                weight=ft.FontWeight.BOLD,
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                    padding=12,
                    bgcolor=SURFACE_ALT,
                    border=ft.Border.all(1, BORDER_COLOR),
                    border_radius=12,
                )
            )

    def cook_recipe(recipe_id: str, recipe_name: str):
        success = engine.cook_recipe_gui(recipe_id)
        if not success:
            show_status("Unable to cook recipe. Recipe ID not found.", ok=False)
            page.update()
            return

        show_status(f"Cooked {recipe_name}. Pantry and history updated.")
        refresh_all_sections()
        page.update()

    def close_dialog(dialog: ft.AlertDialog):
        page.pop_dialog()
        page.update()

    def confirm_cook_from_dialog(dialog: ft.AlertDialog, recipe_id: str, recipe_name: str):
        page.pop_dialog()
        page.update()
        cook_recipe(recipe_id, recipe_name)

    def show_recipe_steps_and_confirm(recipe: dict):
        recipe_id = recipe.get("id", "")
        recipe_name = recipe.get("name", "Recipe")
        steps = recipe.get("steps") or []

        step_controls = [ft.Text(f"{index + 1}. {step}") for index, step in enumerate(steps)]
        if not step_controls:
            step_controls = [ft.Text("No steps listed for this recipe.")]

        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text(f"{recipe_name} - Cooking Steps"),
            content=ft.Container(
                content=ft.Column(step_controls, spacing=8, scroll=ft.ScrollMode.AUTO),
                width=560,
                height=320 if len(step_controls) > 6 else None,
            ),
            actions=[
                make_button("Cancel", on_click=lambda e: close_dialog(dialog)),
                make_button(
                    "Cook Now",
                    on_click=lambda e, rid=recipe_id, rname=recipe_name: confirm_cook_from_dialog(dialog, rid, rname),
                ),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )

        page.show_dialog(dialog)

    def show_recipe_steps_only(recipe: dict):
        recipe_name = recipe.get("name", "Recipe")
        steps = recipe.get("steps") or []

        step_controls = [ft.Text(f"{index + 1}. {step}") for index, step in enumerate(steps)]
        if not step_controls:
            step_controls = [ft.Text("No steps listed for this recipe.")]

        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text(f"{recipe_name} - Steps"),
            content=ft.Container(
                content=ft.Column(step_controls, spacing=8, scroll=ft.ScrollMode.AUTO),
                width=560,
                height=320 if len(step_controls) > 6 else None,
            ),
            actions=[
                make_button("Close", on_click=lambda e: close_dialog(dialog)),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )

        page.show_dialog(dialog)

    def show_missing_ingredients(recipe: dict):
        recipe_name = recipe.get("name", "Recipe")
        ingredients = recipe.get("ingredients", {})
        pantry = load_pantry()
        missing = engine.get_missing(ingredients, pantry)

        if missing:
            missing_controls = [
                ft.Text(
                    f"- {name}: {_format_amount(data['amount'])} {data['unit']}"
                )
                for name, data in missing.items()
            ]
        else:
            missing_controls = [ft.Text("You have all the ingredients for this recipe!")]

        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text(f"{recipe_name} - Shopping List"),
            content=ft.Container(
                content=ft.Column(missing_controls, spacing=6, scroll=ft.ScrollMode.AUTO),
                width=400,
                height=280 if len(missing_controls) > 5 else None,
            ),
            actions=[
                make_button("Close", on_click=lambda e: close_dialog(dialog)),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )

        page.show_dialog(dialog)

    def make_recipe_card(recipe: dict, pantry: dict, cookable: bool):
        ingredients = recipe.get("ingredients", {})
        ingredient_lines = [
            f"- {name}: {_format_amount(req['amount'])} {req['unit']}"
            for name, req in ingredients.items()
        ]
        card_bgcolor = COOKABLE_CARD if cookable else LOCKED_CARD

        details_controls = [
            ft.Text(recipe.get("name", "Unknown Recipe"), size=18, weight=ft.FontWeight.BOLD, color=TEXT_PRIMARY),
            ft.Text("Ingredients:", color=TEXT_SECONDARY),
            ft.Text("\n".join(ingredient_lines) if ingredient_lines else "No ingredients listed", color=TEXT_PRIMARY),
        ]

        if cookable:
            details_controls.append(
                make_button(
                    "Cook",
                    on_click=lambda e, current_recipe=recipe: show_recipe_steps_and_confirm(current_recipe),
                )
            )
        else:
            missing = engine.get_missing(ingredients, pantry)
            missing_text = "\n".join(
                [f"- {name}: {_format_amount(data['amount'])} {data['unit']}" for name, data in missing.items()]
            )
            details_controls.append(ft.Text("Missing ingredients:", weight=ft.FontWeight.W_600, color=TEXT_SECONDARY))
            details_controls.append(ft.Text(missing_text if missing_text else "No missing ingredients", color=TEXT_PRIMARY))

        return ft.Container(
            col={"sm": 6, "lg": 4, "xl": 3},
            content=ft.Card(
                content=ft.Container(
                    content=ft.Column(details_controls, spacing=8, scroll=ft.ScrollMode.AUTO),
                    padding=12,
                    height=320,
                    bgcolor=card_bgcolor,
                    border_radius=14,
                    border=ft.Border.all(1, BORDER_COLOR),
                )
            ),
        )

    def recipe_matches_query(recipe: dict, query: str):
        if not query:
            return True

        lookup = query.lower()
        recipe_name = recipe.get("name", "").lower()
        recipe_id = recipe.get("id", "").lower()
        ingredient_text = " ".join(recipe.get("ingredients", {}).keys()).lower()
        return lookup in recipe_name or lookup in recipe_id or lookup in ingredient_text

    def refresh_recipe_view():
        available_recipes_list.controls.clear()
        locked_recipes_list.controls.clear()

        pantry = load_pantry()
        available, locked = engine.find_recipes()
        recipe_ready_count.value = str(len(available))
        recipe_locked_count.value = str(len(locked))

        if not available:
            available_recipes_list.controls.append(ft.Text("No recipes are currently cookable."))
        else:
            for recipe in available:
                available_recipes_list.controls.append(make_recipe_card(recipe, pantry, cookable=True))

        if not locked:
            locked_recipes_list.controls.append(ft.Text("No nearly-complete recipes right now."))
        else:
            for recipe in locked:
                locked_recipes_list.controls.append(make_recipe_card(recipe, pantry, cookable=False))

    def make_search_recipe_card(recipe: dict):
        ingredients = recipe.get("ingredients", {})
        ingredient_lines = [
            f"- {name}: {_format_amount(req['amount'])} {req['unit']}"
            for name, req in ingredients.items()
        ]

        controls = [
            ft.Text(recipe.get("name", "Unknown Recipe"), size=18, weight=ft.FontWeight.BOLD),
            ft.Text(f"Recipe ID: {recipe.get('id', 'n/a')}", color=TEXT_SECONDARY),
            ft.Text("Ingredients:", color=TEXT_SECONDARY),
            ft.Text("\n".join(ingredient_lines) if ingredient_lines else "No ingredients listed", color=TEXT_PRIMARY),
            ft.Row(
                [
                    make_button("View Steps", on_click=lambda e, current_recipe=recipe: show_recipe_steps_only(current_recipe)),
                    make_button("Missing Ingredients", on_click=lambda e, current_recipe=recipe: show_missing_ingredients(current_recipe)),
                ],
                wrap=True,
                spacing=6,
            ),
        ]

        return ft.Container(
            col={"sm": 6, "lg": 4, "xl": 3},
            content=ft.Card(
                content=ft.Container(
                    content=ft.Column(controls, spacing=8, scroll=ft.ScrollMode.AUTO),
                    padding=12,
                    height=320,
                    bgcolor=SURFACE_ALT,
                    border_radius=14,
                    border=ft.Border.all(1, BORDER_COLOR),
                )
            ),
        )

    def refresh_search_view():
        search_results_list.controls.clear()

        query = (all_recipe_search_input.value or "").strip().lower()

        cookbook = load_cookbook()
        recipes = []
        for recipe_id, recipe_data in cookbook.items():
            recipe = dict(recipe_data)
            recipe["id"] = recipe_id
            recipes.append(recipe)

        recipes.sort(key=lambda recipe: recipe.get("name", "").lower())

        if query:
            recipes = [recipe for recipe in recipes if recipe_matches_query(recipe, query)]
            all_recipe_search_status.value = f"Search results for '{query}': {len(recipes)}"
        else:
            all_recipe_search_status.value = f"Showing all recipes: {len(recipes)}"

        if not recipes:
            search_results_list.controls.append(ft.Text("No recipes found for your search."))
            return

        for recipe in recipes:
            search_results_list.controls.append(make_search_recipe_card(recipe))

    def search_all_recipes(e=None):
        refresh_search_view()
        page.update()

    def refresh_history_view():
        history = load_history()
        history_list.controls.clear()
        achievements_list.controls.clear()

        history_total_cooks.value = str(len(history))

        if not history:
            history_unique_recipes.value = "0"
            history_top_recipe.value = "-"
            history_list.controls.append(ft.Text("No cooking history yet."))
            achievements_list.controls.append(ft.Text("No achievements yet."))
            return

        counts = Counter(entry.get("recipe_name", "Unknown Recipe") for entry in history)
        history_unique_recipes.value = str(len(counts))
        history_top_recipe.value = counts.most_common(1)[0][0]

        for entry in reversed(history):
            recipe_name = entry.get("recipe_name", "Unknown Recipe")
            cooked_at = entry.get("date", "Unknown Date")
            history_list.controls.append(
                ft.Container(
                    content=ft.ListTile(
                        leading=ft.Icon(ft.Icons.RESTAURANT, color=ACCENT_COLOR),
                        title=ft.Text(recipe_name, color=TEXT_PRIMARY, weight=ft.FontWeight.W_600),
                        subtitle=ft.Text(cooked_at, color=TEXT_SECONDARY),
                    ),
                    bgcolor=SURFACE_ALT,
                    border=ft.Border.all(1, BORDER_COLOR),
                    border_radius=12,
                    padding=6,
                )
            )

        for recipe_name, total in counts.items():
            rank = "Novice"
            if total >= 10:
                rank = "Master"
            elif total >= 5:
                rank = "Expert"

            achievements_list.controls.append(
                ft.Container(
                    content=ft.Row(
                        [
                            ft.Column(
                                [
                                    ft.Text(recipe_name, color=TEXT_PRIMARY, weight=ft.FontWeight.W_600),
                                    ft.Text(f"Cooked {total}x", color=TEXT_SECONDARY, size=12),
                                ],
                                spacing=2,
                            ),
                            ft.Container(
                                content=ft.Text(rank, color=TEXT_PRIMARY, weight=ft.FontWeight.W_600),
                                bgcolor=SURFACE_ALT,
                                border=ft.Border.all(1, BORDER_COLOR),
                                border_radius=999,
                                padding=ft.padding.symmetric(horizontal=10, vertical=4),
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                    bgcolor=SURFACE_ALT,
                    border=ft.Border.all(1, BORDER_COLOR),
                    border_radius=12,
                    padding=10,
                )
            )

    def add_loot(e):
        name = (item_name_input.value or "").strip().lower()
        amount_raw = (item_amount_input.value or "").strip()
        unit = (item_unit_input.value or "").strip().lower()

        if not name:
            show_status("Item name is required.", ok=False)
            page.update()
            return

        if not unit:
            show_status("Unit is required.", ok=False)
            page.update()
            return

        try:
            amount = float(amount_raw)
            if amount <= 0:
                raise ValueError
        except ValueError:
            show_status("Amount must be a positive number.", ok=False)
            page.update()
            return

        pantry = load_pantry()
        if name in pantry:
            pantry[name]["amount"] += amount
        else:
            pantry[name] = {"amount": amount, "unit": unit}

        data_manager.save_data(data_manager.PANTRY_FILE, pantry)

        item_name_input.value = ""
        item_amount_input.value = ""
        item_unit_input.value = ""

        show_status(f"Added {_format_amount(amount)} {unit} of {name}.")
        refresh_all_sections()
        page.update()

    def clear_add_loot_form(e=None):
        item_name_input.value = ""
        item_amount_input.value = ""
        item_unit_input.value = ""
        status_text.value = ""
        page.update()

    def refresh_all_sections(e=None):
        refresh_pantry_view()
        refresh_recipe_view()
        refresh_search_view()
        refresh_history_view()

    pantry_view = ft.Container(
        ft.Column(
            [
                ft.Row(
                    [
                        ft.Column(
                            [
                                ft.Text("Pantry", size=24, weight=ft.FontWeight.BOLD, color=TEXT_PRIMARY),
                                ft.Text("Track what you currently have on hand.", color=TEXT_SECONDARY, size=13),
                            ],
                            spacing=2,
                        ),
                        make_button("Refresh", on_click=refresh_all_sections),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                pantry_stats_row,
                ft.Divider(color=BORDER_COLOR),
                ft.Text("Current Inventory", size=16, weight=ft.FontWeight.W_600, color=TEXT_PRIMARY),
                ft.Container(
                    content=pantry_list,
                    bgcolor=SURFACE_COLOR,
                    border=ft.Border.all(1, BORDER_COLOR),
                    border_radius=12,
                    padding=10,
                    expand=True,
                ),
            ],
            spacing=12,
            expand=True,
        ),
        padding=16,
        bgcolor=SURFACE_COLOR,
        border_radius=18,
        border=ft.Border.all(1, BORDER_COLOR),
    )

    add_loot_view = ft.Container(
        ft.Column(
            [
                ft.Column(
                    [
                        ft.Text("Add Loot", size=24, weight=ft.FontWeight.BOLD, color=TEXT_PRIMARY),
                        ft.Text("Register new pantry ingredients quickly.", color=TEXT_SECONDARY, size=13),
                    ],
                    spacing=2,
                ),
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Text("Ingredient Details", size=16, weight=ft.FontWeight.W_600, color=TEXT_PRIMARY),
                            ft.ResponsiveRow(
                                [
                                    ft.Container(item_name_input, col={"sm": 12, "md": 12}),
                                    ft.Container(item_amount_input, col={"sm": 12, "md": 6}),
                                    ft.Container(item_unit_input, col={"sm": 12, "md": 6}),
                                ],
                                spacing=10,
                                run_spacing=10,
                            ),
                            ft.Row(
                                [
                                    make_button("Add Item", on_click=add_loot),
                                    ft.OutlinedButton(
                                        "Clear",
                                        on_click=clear_add_loot_form,
                                        style=ft.ButtonStyle(
                                            color=TEXT_SECONDARY,
                                            side=ft.BorderSide(1, BORDER_COLOR),
                                            shape=ft.RoundedRectangleBorder(radius=12),
                                        ),
                                        height=42,
                                    ),
                                ],
                                spacing=10,
                            ),
                            ft.Container(
                                content=status_text,
                                bgcolor=SURFACE_COLOR,
                                border=ft.Border.all(1, BORDER_COLOR),
                                border_radius=10,
                                padding=10,
                            ),
                        ],
                        spacing=12,
                    ),
                    padding=14,
                    bgcolor=SURFACE_ALT,
                    border_radius=14,
                    border=ft.Border.all(1, BORDER_COLOR),
                ),
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Text("Quick Format", size=14, weight=ft.FontWeight.W_600, color=TEXT_PRIMARY),
                            ft.Text("Examples: egg | 6 | pcs, rice | 2 | kg, milk | 500 | ml", color=TEXT_SECONDARY, size=12),
                        ],
                        spacing=4,
                    ),
                    padding=12,
                    bgcolor=SURFACE_ALT,
                    border=ft.Border.all(1, BORDER_COLOR),
                    border_radius=12,
                ),
            ],
            spacing=14,
            scroll=ft.ScrollMode.AUTO,
            expand=True,
        ),
        padding=16,
        bgcolor=SURFACE_COLOR,
        border_radius=18,
        border=ft.Border.all(1, BORDER_COLOR),
    )

    recipes_view = ft.Container(
        ft.Column(
            [
                ft.Row(
                    [
                        ft.Column(
                            [
                                ft.Text("Find Recipes / Cook", size=24, weight=ft.FontWeight.BOLD, color=TEXT_PRIMARY),
                                ft.Text("See what you can cook right now and what you still need.", color=TEXT_SECONDARY, size=13),
                            ],
                            spacing=2,
                        ),
                        make_button("Refresh", on_click=refresh_all_sections),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Row(
                                [
                                    ft.Text("Cookable Recipes", size=18, weight=ft.FontWeight.W_700, color=TEXT_PRIMARY),
                                    ft.Container(
                                        content=recipe_ready_count,
                                        bgcolor=SURFACE_ALT,
                                        border=ft.Border.all(1, BORDER_COLOR),
                                        border_radius=999,
                                        padding=ft.padding.symmetric(horizontal=10, vertical=4),
                                    ),
                                ],
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            ),
                            available_recipes_list,
                        ],
                        spacing=10,
                    ),
                    padding=12,
                    bgcolor=SURFACE_ALT,
                    border_radius=14,
                    border=ft.Border.all(1, BORDER_COLOR),
                ),
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Row(
                                [
                                    ft.Text("Almost There (Missing 1-3 items)", size=18, weight=ft.FontWeight.W_700, color=TEXT_PRIMARY),
                                    ft.Container(
                                        content=recipe_locked_count,
                                        bgcolor=SURFACE_ALT,
                                        border=ft.Border.all(1, BORDER_COLOR),
                                        border_radius=999,
                                        padding=ft.padding.symmetric(horizontal=10, vertical=4),
                                    ),
                                ],
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            ),
                            locked_recipes_list,
                        ],
                        spacing=10,
                    ),
                    padding=12,
                    bgcolor=SURFACE_ALT,
                    border_radius=14,
                    border=ft.Border.all(1, BORDER_COLOR),
                ),
            ],
            spacing=14,
            scroll=ft.ScrollMode.AUTO,
            expand=True,
        ),
        padding=16,
        bgcolor=SURFACE_COLOR,
        border_radius=18,
        border=ft.Border.all(1, BORDER_COLOR),
    )

    search_view = ft.Container(
        ft.Column(
            [
                ft.Row(
                    [
                        ft.Container(all_recipe_search_input, expand=True),
                        make_button("Search", on_click=search_all_recipes),
                    ]
                ),
                all_recipe_search_status,
                search_results_list,
            ],
            spacing=10,
            scroll=ft.ScrollMode.AUTO,
            expand=True,
        ),
        padding=16,
        bgcolor=SURFACE_COLOR,
        border_radius=18,
        border=ft.Border.all(1, BORDER_COLOR),
    )

    history_view = ft.Container(
        ft.Column(
            [
                ft.Row(
                    [
                        ft.Column(
                            [
                                ft.Text("Cooking History", size=24, weight=ft.FontWeight.BOLD, color=TEXT_PRIMARY),
                                ft.Text("Review every cooked meal and your rank progress.", color=TEXT_SECONDARY, size=13),
                            ],
                            spacing=2,
                        ),
                        make_button("Refresh", on_click=refresh_all_sections),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                ft.ResponsiveRow(
                    [
                        stat_tile("Total Cooks", history_total_cooks, ft.Icons.HISTORY),
                        stat_tile("Unique Recipes", history_unique_recipes, ft.Icons.MENU_BOOK),
                        stat_tile("Top Recipe", history_top_recipe, ft.Icons.STAR),
                    ],
                    spacing=10,
                    run_spacing=10,
                ),
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Text("History Log", size=18, weight=ft.FontWeight.W_700, color=TEXT_PRIMARY),
                            history_list,
                        ],
                        spacing=10,
                        expand=True,
                    ),
                    padding=12,
                    bgcolor=SURFACE_ALT,
                    border_radius=14,
                    border=ft.Border.all(1, BORDER_COLOR),
                    expand=True,
                ),
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Text("Achievements", size=18, weight=ft.FontWeight.W_700, color=TEXT_PRIMARY),
                            achievements_list,
                        ],
                        spacing=10,
                    ),
                    padding=12,
                    bgcolor=SURFACE_ALT,
                    border_radius=14,
                    border=ft.Border.all(1, BORDER_COLOR),
                ),
            ],
            spacing=14,
            expand=True,
        ),
        padding=16,
        bgcolor=SURFACE_COLOR,
        border_radius=18,
        border=ft.Border.all(1, BORDER_COLOR),
    )

    page.add(
        ft.Container(
            content=ft.Container(
                content=ft.Row(
                    [
                        ft.Row(
                            [
                                ft.Container(
                                    content=ft.Icon(ft.Icons.LOCAL_DINING, size=20, color=ACCENT_COLOR),
                                    bgcolor="#1C3150",
                                    border=ft.Border.all(1, BORDER_COLOR),
                                    border_radius=12,
                                    padding=10,
                                ),
                                ft.Column(
                                    [
                                        ft.Text(
                                            "KUSINA TAVERN",
                                            size=30,
                                            weight=ft.FontWeight.W_700,
                                            font_family="Metamorphous",
                                            color=TEXT_PRIMARY,
                                        ),
                                        ft.Text(
                                            "Smart pantry, recipe matcher, and cooking log",
                                            size=13,
                                            color=TEXT_SECONDARY,
                                        ),
                                    ],
                                    spacing=2,
                                ),
                            ],
                            spacing=12,
                            vertical_alignment=ft.CrossAxisAlignment.CENTER,
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.START,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                gradient=ft.LinearGradient(
                    begin=ft.Alignment.TOP_LEFT,
                    end=ft.Alignment.BOTTOM_RIGHT,
                    colors=[HEADER_GRADIENT_START, HEADER_GRADIENT_END],
                ),
                border=ft.Border.all(1, BORDER_COLOR),
                border_radius=18,
                padding=ft.padding.only(left=18, top=14, right=18, bottom=14),
            ),
            padding=ft.padding.only(left=22, top=24, right=22, bottom=12),
        ),
        ft.Container(
            content=ft.Tabs(
                length=5,
                expand=True,
                animation_duration=200,
                content=ft.Column(
                    expand=True,
                    controls=[
                        ft.Container(
                            content=ft.TabBar(
                                tabs=[
                                    ft.Tab(label="View Pantry", icon=ft.Icons.INVENTORY_2),
                                    ft.Tab(label="Add Loot", icon=ft.Icons.ADD_BOX),
                                    ft.Tab(label="Find Recipes / Cook", icon=ft.Icons.RESTAURANT_MENU),
                                    ft.Tab(label="Search Recipes", icon=ft.Icons.SEARCH),
                                    ft.Tab(label="Cooking History", icon=ft.Icons.HISTORY),
                                ]
                            ),
                            bgcolor=TAB_STRIP_BG,
                            border=ft.Border.all(1, BORDER_COLOR),
                            border_radius=12,
                            padding=8,
                        ),
                        ft.TabBarView(
                            expand=True,
                            controls=[
                                pantry_view,
                                add_loot_view,
                                recipes_view,
                                search_view,
                                history_view,
                            ],
                        ),
                    ],
                ),
            ),
            padding=ft.padding.only(left=22, top=0, right=22, bottom=22),
            expand=True,
        ),
    )

    refresh_all_sections()
    page.update()


if __name__ == "__main__":
    ft.run(main)
