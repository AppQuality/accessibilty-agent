import asyncio
from typing import Any
import sys
import os
import re

from agents import Agent, Runner, gen_trace_id, trace,LocalShellTool
from agents.mcp import MCPServer, MCPServerSse, MCPServerStdio
from agents.model_settings import ModelSettings


async def run(fsserver: MCPServer,mcp_server: MCPServer,url,cp_id):
    
    await fsserver.connect()
    await mcp_server.connect()
    
    if os.path.exists("src/tasks/links.md"):
        os.unlink("src/tasks/links.md")
        with open("src/tasks/links.md", "w") as file:
            file.write("")
    if os.path.exists("src/tasks/accessibility_results.md"):
        os.unlink("src/tasks/accessibility_results.md")
        with open("src/tasks/accessibility_results.md", "w") as file:
            file.write("")
            
            
    upload_agent = Agent(
        name="Upload Agent",
            instructions = """
    Quando vieni chiamato devi:
    1. Aprire il file `src/tasks/accessibility_results.md`.
    2. Il file è strutturato in blocchi, ciascuno così:
    ```
    ## <scraped-link>
    [ ] <accessibility-issue-json>
    [x] <accessibility-issue-json>
    [ ] <accessibility-issue-json>
    ```
    3. Per ogni riga `[ ] <accessibility-issue-json>`:
    a. Estrai `<scraped-link>` dal blocco corrente (la riga `##` più vicina sopra).
    b. Estrai `<accessibility-issue-json>` e decodificalo in JSON.
    c. Usa il tool `upload_bug` con il seguente formato JSON:
    ```json
    {
        "cp": <the campaign id to upload the issue to>,
        "title": "[<scraped-link>] - <Short Description>",
        "bugType": "<PERCEIVABLE|OPERABLE|UNDERSTANDABLE|ROBUST>",
        "severity": "<LOW|MEDIUM|HIGH|CRITICAL>",
        "description": "<Element> - <Long and Descriptive Description>",
        "url": "<scraped-link>",
        "element": "<Element>",
        "notes": "<The suggested resolution>",
        "criteria": "<WCAG criteria, e.g., '1.1.1 Non-text Content'>",
        "level": "<A|AA|AAA>"
    }
    ```
    d. Dopo l’invio riuscito, sovrascrivi `src/tasks/accessibility_results.md`, marcando la riga come `[x] <accessibility-issue-json>`.

    4. Continua fino a che tutte le righe `[ ] <accessibility-issue-json>` sono marcate `[x]`.

    Vincoli:
    - Esegui tutto in ordine di apparizione nel file.
    - Aggiorna il file dopo ogni invio.
    - Non modificare né dedurre i contenuti del JSON.
    - Non eseguire nulla se tutte le voci sono già marcate `[x]`.
    - Assicurati che il JSON sia formattato correttamente e che i campi siano compilati come richiesto.
    - `Element` è il tag HTML o il selector dell'issue.
    - `Short Description` è una breve descrizione dell'issue, ad esempio "Missing Alt Text".
    - `Long and Descriptive Description` è un descrizione dettagliata dell'issue, scritta per non esperti, con una spiegazione del problema e perché è importante risolverlo
    - `bugType` è esattamente uno tra: PERCEIVABLE, OPERABLE, UNDERSTANDABLE, ROBUST. Non dedurre o alterare questi valori.
    - `Gravity` è mappato da `impactLevel` come segue:
        - "minor" → LOW
        - "moderate" → MEDIUM
        - "serious" → HIGH
        - "critical" → CRITICAL
    - Usa SOLAMENTE LOW, MEDIUM, HIGH, CRITICAL come valori per `severity`. NON INVENTARE NUOVI VALORI.
    - `criteria` deve essere uno dei criteri WCAG, come "1.1.1 - Non-text Content", "2.1.1 - Keyboard", "3.3.2 - Labels or Instructions", etc.  
""",
        mcp_servers=[mcp_server,fsserver],
        model_settings=ModelSettings(tool_choice="required"),
        model="gpt-4o-mini",
    )

    scan_agent = Agent(
        name="Scan Agent",
            instructions = """
            Quando vieni chiamato devi:
    1. Aprire il file `src/tasks/links.md`.
    2. Per ogni riga che inizia con `[ ] <scraped-link>`:
    a. Estrai `<scraped-link>` e usa `scan_accessibility` su di esso.
    b. Se `src/tasks/accessibility_results.md` esiste, leggilo per assicurarti di non sovrascrivere i risultati esistenti e aggiungi i risultati della scansione corrente come segue:
        ```
        ## <scraped-link>
        [ ] <accessibility-issue-json>
        [ ] <accessibility-issue-json>
        ...
        ```
    c. Sovrascrivi `src/tasks/links.md`, marcando quella riga come `[x] <scraped-link>`.

    3. Dopo ogni scansione, aggiorna entrambi i file prima di passare al link successivo.
    4. Termina quando tutti i link sono marcati `[x]`.

    Vincoli:
    - Esegui una scansione per volta, in ordine, attendendo ogni risultato prima di passare al successivo.
    - Non avviare `scan_accessibility` in parallelo.
    - Scrivi  <accessibility-issue-json> in una sola riga, senza andare a capo. Non troncare o modificare il JSON.
    - Usa `append` per scrivere in `accessibility_results.md`, assicurati che i risultati precedenti non vengano sovrascritti.
    - Se esiste già un blocco per quel link (`## <scraped-link>`), non duplicarlo né cancellarlo.
    - Non modificare i risultati precedenti.
    - Non dedurre o alterare i link.
    - Non eseguire nulla se tutti i link sono già marcati `[x]`.

""",
        mcp_servers=[mcp_server,fsserver],
        model_settings=ModelSettings(tool_choice="required"),
        model="gpt-4o-mini",
        handoffs=[upload_agent]
    )
    
    
    scrape_agent = Agent(
        name="Scrape Agent",
            instructions = """
    Quando vieni chiamato devi:

    1. Estrarre i link da quell'URL usando `scrape` con `max depth = 1`.

    2. Salvare i link in `src/tasks/links.md` in questo formato:
    ```
    [ ] <scraped-link>
    ```
""",
        mcp_servers=[mcp_server,fsserver],
        model_settings=ModelSettings(tool_choice="required"),
        model="gpt-4o-mini",
    )
    
    
    triage_agent = Agent(
        name="Triage Agent",
        instructions="You determine which agent to use based on the user's input. If the input starts with 'Scrape', use the Scrape Agent. If it starts with 'Scan', use the Scan Agent. If it starts with 'Upload', use the Upload Agent.",
        handoffs=[scrape_agent,scan_agent,upload_agent],
    )
    # Use the `add` tool to add two numbers
    print(f"Working on: {url}")
    result = await Runner.run(starting_agent=triage_agent, input=f"Scrape {url}",max_turns=100)
    result = await Runner.run(starting_agent=triage_agent, input=f"Scan",max_turns=100)
    result = await Runner.run(starting_agent=triage_agent, input=f"Upload on campaign {cp_id}",max_turns=100)
    print(result.final_output)                  

    with open("output.md", "w") as f:
        f.write(result.final_output)


async def main(url,cp_id):
      current_dir = os.path.dirname(os.path.abspath(__file__))
      mcp_server_url = os.getenv("MCP_SERVER_URL", "http://localhost:3000/sse")
      
      print(f"Using MCP server URL: {mcp_server_url}")

      fsserver = MCPServerStdio(
        name="Filesystem Server, via npx",
        params={
            "command": "npx",
            "args": ["-y", "@modelcontextprotocol/server-filesystem", current_dir],
        },
      )
      server = MCPServerSse(
        name="SSE Python Server",               
        params={
            "url": mcp_server_url,
        },
        client_session_timeout_seconds=1000
       ) 
      trace_id = gen_trace_id()
      with trace(workflow_name="SSE Example", trace_id=trace_id):
        trace_url = f"https://platform.openai.com/traces/trace?trace_id={trace_id}"
        print(f"Trace URL: {trace_url}\n")
        asyncio.create_task(run(fsserver,server,url,cp_id))
        return trace_url

def is_valid_url(url):
    return re.match(r'^https?://[^\s]+$', url) is not None


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Errore: Devi passare un URL come argomento.")
        sys.exit(1)

    arg = sys.argv[1]
    cp = sys.argv[2]
    if not is_valid_url(arg):
        print(f"Errore: '{arg}' non è un URL valido.")
        sys.exit(1)

    asyncio.run(main(arg,cp))