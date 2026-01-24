from pygls.server import LanguageServer

# Inicijalizacija najjednostavnijeg mogućeg servera
server = LanguageServer("test-server", "v1.0")

if __name__ == "__main__":
    print("Test LSP Server pokrenut... (Ceka na IO)")
    # start_io() koristi standardni ulaz/izlaz za komunikaciju
    server.start_io()