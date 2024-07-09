import flet as ft
from logic_generator import TruthTable

#https://flet.dev/gallery/
# https://m3.material.io/styles/icons/overview

def main(page: ft.Page) -> None:     
    # Basic Settings
    page.title = "Propositional Logic Truth Table Generator"    
    page.theme_mode = ft.ThemeMode.LIGHT
    page.window_height = 600
    page.window_width = 1400
    page.window_resizable = True

    # TT Event
    def btn_wff_click(e, style="plain"):
        if not wff_input.value:
            wff_input.error_text = "Please enter a formula"
            page.update()
        else:
            table = TruthTable(wff_input.value)
            wff_input.error_text = ""
            output_str = table.print_table(tablefmt=table_format.value)
            truth_table.value = output_str
            page.update()   

    wff_input = ft.TextField(
    label="Propositional Logic Wff", 
    width=500,
    autofocus=True,
    expand=True,
    icon=ft.icons.FORMAT_SIZE,
    on_submit=btn_wff_click,
    )

    # Submit Button
    page.add(ft.Row(controls=[
    wff_input, ft.ElevatedButton(text="create", icon="star", on_click=btn_wff_click)
    ]))

    # Radio Buttons
    table_format = ft.RadioGroup(content=ft.Row([
        ft.Radio(value="plain", label="Plain"),
        ft.Radio(value="simple", label="Simple"),
        ft.Radio(value="github", label="Github"),
        ft.Radio(value="grid", label="Grid"),   
        ft.Radio(value="outline", label="Outline"),   
        ft.Radio(value="rounded_outline", label="Rounded Outline"),  
        ft.Radio(value="rst", label="RST"),
        ft.Radio(value="pretty", label="Pretty"),   
        ft.Radio(value="pipe", label="Pipe"),
        ft.Radio(value="html", label="HTML"),
        ft.Radio(value="latex", label="LaTeX"),
        ft.Radio(value="latex_raw", label="LaTeX Raw"),
        ft.Radio(value="latex_longtable", label="LaTeX Longtable"),
    ]), on_change=btn_wff_click)
    page.add(ft.Row(controls=[
        table_format
    ]
    ))

# Displays TT
    truth_table = ft.Text(value=" ", italic=False, selectable=True, size=24, expand=True)
    md_test = ft.Markdown(value=" ", expand=True)
    page.add(truth_table)

    def theme_change(e):
        page.theme_mode = (
            ft.ThemeMode.DARK
            if page.theme_mode == ft.ThemeMode.LIGHT
            else ft.ThemeMode.LIGHT
        )
        theme_switch.label = (
            "Light theme" if page.theme_mode == ft.ThemeMode.LIGHT else "Dark theme"
        )
        page.update()
    
    def reset(e):
        wff_input.value = ""
        truth_table.value = ""
        page.update()   

    async def open_website(e):
        await e.control.page.launch_url_async("https://www.davidagler.com")

    # Copy button. Copies truth_table value
    def copy_table(e):
        page.set_clipboard(truth_table.value)

    # bottom app bar
    page.bottom_appbar = ft.BottomAppBar(
        #title=ft.Text("AppBar Example"),        
        shadow_color="green",
        shape=ft.NotchShape.CIRCULAR,
        content=ft.Row(
            controls=[
            ft.IconButton(ft.icons.WB_SUNNY_OUTLINED, on_click=theme_change),
            ft.Container(expand=True),
            ft.ElevatedButton(
            content=ft.Text("Reset", color="red"), 
            on_click=reset, expand=1),
            ft.ElevatedButton(
            content=ft.Text("Copy", color="blue"),
            on_click=copy_table, expand=1),
            ft.Container(expand=True),
            ft.IconButton(icon=ft.icons.WEB, on_click=open_website), #icon_color=ft.colors.WHITE
        ],
    ))
    page.update()

    theme_switch = ft.Switch(label="Light theme", on_change=theme_change)
    #page.add(theme_switch)


if __name__ == "__main__":
    ft.app(main, assets_dir="assets")