import flet as ft

def test_app(page: ft.Page):
    page.bgcolor = "#0f0f0f"
    page.title = "TEST"
    
    # Componente super simples
    txt = ft.Text("AAAAAAA", size=64, color="#ff0000")
    container = ft.Container(content=txt, bgcolor="#ffffff", padding=20, height=200)
    
    page.add(container)
    page.update()

if __name__ == "__main__":
    ft.app(target=test_app)
