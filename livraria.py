import tkinter as tk
from tkinter import ttk

catalogo = []
contador_id = 1

def limpar_placeholder(event, entry, placeholder_text):
    if entry.get() == placeholder_text:
        entry.delete(0, tk.END)
        entry.config(fg="black")

def limpar_placeholder_combobox(event, combobox, placeholder_text):
    if combobox.get() == placeholder_text:
        combobox.set("")
        combobox.configure(foreground="black")

def mostrar_erro_entry(entry, mensagem):
    entry.delete(0, tk.END)
    entry.insert(0, mensagem)
    entry.config(fg="red")

def mostrar_erro_combobox(combobox, mensagem):
    combobox.set(mensagem)
    combobox.configure(foreground="red")

def validar_e_adicionar_livro():
    global contador_id

    titulo = entry_titulo.get()
    autor = entry_autor.get()
    ano = entry_ano.get()
    genero = entry_genero.get()

    # Validar campos
    if not titulo:
        mostrar_erro_entry(entry_titulo, "Preencha o título")
        return
    if not autor:
        mostrar_erro_entry(entry_autor, "Preencha o autor")
        return
    if not ano:
        mostrar_erro_entry(entry_ano, "Preencha o ano")
        return
    if not ano.isdigit() or not (1000 <= int(ano) <= 2025):
        mostrar_erro_entry(entry_ano, "Ano inválido (1000-2025)")
        return
    if not genero or genero == "Escolha um gênero":
        mostrar_erro_combobox(entry_genero, "Escolha um gênero")
        return

    # Verificar duplicidade
    for livro in catalogo:
        if livro["titulo"].lower() == titulo.lower() and livro["autor"].lower() == autor.lower():
            mostrar_erro_entry(entry_titulo, "Livro já existe")
            return

    novo_livro = {
        "ID": contador_id,
        "titulo": titulo,
        "autor": autor,
        "ano": ano,
        "genero": genero
    }
    catalogo.append(novo_livro)
    contador_id += 1
    atualizar_treeview(catalogo)

    # Limpar campos
    entry_titulo.delete(0, tk.END)
    entry_autor.delete(0, tk.END)
    entry_ano.delete(0, tk.END)
    entry_genero.set("")

    # Resetar cor dos campos
    entry_titulo.config(fg="black")
    entry_autor.config(fg="black")
    entry_ano.config(fg="black")
    entry_genero.configure(foreground="black")

    entry_titulo.focus_set()

def atualizar_treeview(lista_livros):
    treeview.delete(*treeview.get_children())
    for livro in lista_livros:
        treeview.insert("", "end", values=(livro["ID"], livro["titulo"], livro["autor"], livro["ano"], livro["genero"]))

def buscar_livro():
    termo_busca = entry_busca.get().lower().strip()
    resultados = []

    for livro in catalogo:
        if (termo_busca in livro["titulo"].lower() or
            termo_busca in livro["autor"].lower() or
            termo_busca in livro["ano"].lower() or
            termo_busca in livro["genero"].lower()):
            resultados.append(livro)

    atualizar_treeview(resultados)

def ordenar_livros():
    catalogo.sort(key=lambda livro: livro["autor"].lower())
    atualizar_treeview(catalogo)

def remover_livro():
    item_selecionado = treeview.selection()
    if not item_selecionado:
        return

    livro_valores = treeview.item(item_selecionado, "values")
    id_selecionado = int(livro_valores[0])

    for livro in catalogo:
        if livro["ID"] == id_selecionado:
            catalogo.remove(livro)
            atualizar_treeview(catalogo)
            return

# --- Interface Gráfica ---
janela = tk.Tk()
janela.title("Sistema de Livraria")
janela.configure(bg="gray")
janela.geometry("800x600")

# Entradas de dados
tk.Label(janela, text="Título:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
entry_titulo = tk.Entry(janela, width=30)
entry_titulo.grid(row=0, column=1, padx=5, pady=5)
entry_titulo.bind("<FocusIn>", lambda e: limpar_placeholder(e, entry_titulo, "Preencha o título"))

tk.Label(janela, text="Autor:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
entry_autor = tk.Entry(janela, width=30)
entry_autor.grid(row=1, column=1, padx=5, pady=5)
entry_autor.bind("<FocusIn>", lambda e: limpar_placeholder(e, entry_autor, "Preencha o autor"))

tk.Label(janela, text="Ano:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
entry_ano = tk.Entry(janela, width=30)
entry_ano.grid(row=2, column=1, padx=5, pady=5)
entry_ano.bind("<FocusIn>", lambda e: limpar_placeholder(e, entry_ano, "Preencha o ano"))
entry_ano.bind("<FocusIn>", lambda e: limpar_placeholder(e, entry_ano, "Ano inválido (1000-2025)"))

tk.Label(janela, text="Gênero:").grid(row=3, column=0, padx=5, pady=5, sticky="e")
entry_genero_var = tk.StringVar()
entry_genero = ttk.Combobox(janela, textvariable=entry_genero_var,
                            values=["Ação", "Suspense", "Terror", "Romance", "Ficção", "Outro"],
                            state="readonly")
entry_genero.grid(row=3, column=1, sticky=tk.W, pady=5, padx=5)
entry_genero.set("")
entry_genero.bind("<FocusIn>", lambda e: limpar_placeholder_combobox(e, entry_genero, "Escolha um gênero"))

botao_adicionar = tk.Button(janela, text="Adicionar Livro", command=validar_e_adicionar_livro)
botao_adicionar.grid(row=2, column=2, padx=5, pady=10)

# Busca e ações
tk.Label(janela, text="Buscar:").grid(row=0, column=2, padx=10, pady=5, sticky="e")
entry_busca = tk.Entry(janela, width=30)
entry_busca.grid(row=0, column=3, padx=5, pady=5)

botao_buscar = tk.Button(janela, text="Buscar Livro", command=buscar_livro)
botao_buscar.grid(row=1, column=3, padx=5, pady=5)

botao_ordenar = tk.Button(janela, text="Ordenar por Autor", command=ordenar_livros)
botao_ordenar.grid(row=2, column=3, padx=5, pady=5)

botao_remover = tk.Button(janela, text="Remover Livro", command=remover_livro)
botao_remover.grid(row=3, column=3, padx=5, pady=5)

# Tabela de livros
colunas = ("ID", "titulo", "autor", "ano", "gênero")
treeview = ttk.Treeview(janela, columns=colunas, show="headings")
treeview.heading("ID", text="ID")
treeview.heading("titulo", text="Título")
treeview.heading("autor", text="Autor")
treeview.heading("ano", text="Ano")
treeview.heading("gênero", text="Gênero")
treeview.column("ID", width=25)
treeview.column("titulo", width=250)
treeview.column("autor", width=150)
treeview.column("ano", width=80)
treeview.column("gênero", width=100)
treeview.grid(row=4, column=0, columnspan=4, padx=10, pady=10, sticky="nsew")

# Redimensionamento
janela.grid_rowconfigure(4, weight=1)
janela.grid_columnconfigure(1, weight=1)
janela.grid_columnconfigure(3, weight=1)

janela.mainloop()
