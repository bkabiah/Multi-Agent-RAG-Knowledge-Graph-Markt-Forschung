from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from src.models.state import ResearchState, MarketQuery
from src.agents.manager import orchestrate_workflow

console = Console()

def main():
    console.print(Panel.fit("[bold blue]E-Commerce Market Researcher (Multi-Agent RAG + KG)[/bold blue]", border_style="blue"))
    
    # Beispiel-Query (kann später durch input() ersetzt werden)
    target_market = "Nachhaltige Sportbekleidung Marktanalyse"
    focus_companies = ["Adidas", "Zalando"]
    
    console.print(f"[yellow]Starte Recherche für:[/yellow] {target_market}")
    console.print(f"[yellow]Fokus-Unternehmen:[/yellow] {', '.join(focus_companies)}\n")
    
    # State initialisieren
    initial_state = ResearchState(
        query=MarketQuery(
            target_market=target_market,
            focus_companies=focus_companies
        )
    )
    
    # Workflow ausführen
    final_state = orchestrate_workflow(initial_state)
    
    # Ergebnis anzeigen
    console.print(Panel(Markdown(final_state.final_summary), title="[bold green]Finale Berater-Zusammenfassung[/bold green]", border_style="green"))
    
    if final_state.errors:
        console.print("\n[bold red]Aufgetretene Fehler:[/bold red]")
        for err in final_state.errors:
            console.print(f"- {err}")

if __name__ == "__main__":
    main()
