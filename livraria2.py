import tkinter as tk
from tkinter import Frame, ttk
from datetime import datetime
import random
 
catalogo = []
contador_id = 1
 
# Classe para ToolTips
class ToolTip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tooltip = None
        self.widget.bind("<Enter>", self.enter)
        self.widget.bind("<Leave>", self.leave)
 
    def enter(self, event=None):
        x, y, _, _ = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 25
       
        self.tooltip = tk.Toplevel(self.widget)
        self.tooltip.wm_overrideredirect(True)
        self.tooltip.wm_geometry(f"+{x}+{y}")
       
        label = tk.Label(self.tooltip, text=self.text, background="lightyellow",
                        relief="solid", borderwidth=1, font=("Arial", 10))
        label.pack()
 
    def leave(self, event=None):
        if self.tooltip:
            self.tooltip.destroy()
            self.tooltip = None
 
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
 
def mostrar_mensagem_temporaria(texto, cor="green", duracao=4000):
    label_mensagem.config(text=texto, fg=cor)
    janela.after(duracao, lambda: label_mensagem.config(text=""))
 
def validar_campo_titulo(event):
    texto = entry_titulo.get().strip()
    if not texto:
        entry_titulo.config(fg="black")
    elif any(char.isdigit() for char in texto):
        entry_titulo.config(fg="red")
    else:
        entry_titulo.config(fg="green")
 
def validar_campo_autor(event):
    texto = entry_autor.get().strip()
    if not texto:
        entry_autor.config(fg="black")
    elif any(char.isdigit() for char in texto):
        entry_autor.config(fg="red")
    else:
        entry_autor.config(fg="green")
 
def validar_campo_ano(event):
    texto = entry_ano.get().strip()
    ano_atual = datetime.now().year
 
    if not texto:
        entry_ano.config(fg="black")
    elif not texto.isdigit():
        entry_ano.config(fg="red")
    else:
        ano = int(texto)
        if 1000 <= ano <= ano_atual:
            entry_ano.config(fg="green")
        else:
            entry_ano.config(fg="red")
 
def calcular_digito_verificador_isbn10(isbn):
    """Calcula o dígito verificador para ISBN-10"""
    isbn_limpo = isbn.replace("-", "").replace(" ", "")
    if len(isbn_limpo) != 9 or not isbn_limpo.isdigit():
        return None
   
    soma = 0
    for i, digito in enumerate(isbn_limpo):
        soma += int(digito) * (10 - i)
   
    resto = soma % 11
    digito_verificador = 11 - resto
    if digito_verificador == 10:
        return 'X'
    elif digito_verificador == 11:
        return '0'
    else:
        return str(digito_verificador)
 
def calcular_digito_verificador_isbn13(isbn):
    """Calcula o dígito verificador para ISBN-13"""
    isbn_limpo = isbn.replace("-", "").replace(" ", "")
    if len(isbn_limpo) != 12 or not isbn_limpo.isdigit():
        return None
   
    soma = 0
    for i, digito in enumerate(isbn_limpo):
        if i % 2 == 0:
            soma += int(digito) * 1
        else:
            soma += int(digito) * 3
   
    resto = soma % 10
    digito_verificador = 10 - resto if resto != 0 else 0
    return str(digito_verificador)
 
def validar_isbn(isbn):
    """Valida o formato e dígito verificador do ISBN"""
    isbn_limpo = isbn.replace("-", "").replace(" ", "")
   
    if len(isbn_limpo) == 10:
        # Validar ISBN-10
        if not isbn_limpo[:-1].isdigit():
            return False
       
        digito_calculado = calcular_digito_verificador_isbn10(isbn_limpo[:-1])
        ultimo_digito = isbn_limpo[-1].upper()
       
        return digito_calculado == ultimo_digito
   
    elif len(isbn_limpo) == 13:
        # Validar ISBN-13
        if not isbn_limpo.isdigit():
            return False
       
        digito_calculado = calcular_digito_verificador_isbn13(isbn_limpo[:-1])
        return digito_calculado == isbn_limpo[-1]
   
    else:
        return False
 
def gerar_isbn_fake():
    """Gera um ISBN fake válido para testes"""
    tipo = random.choice([10, 13])
   
    if tipo == 10:
        # Gerar ISBN-10
        base = ''.join([str(random.randint(0, 9)) for _ in range(9)])
        digito_verificador = calcular_digito_verificador_isbn10(base)
        isbn_fake = base + digito_verificador
        # Formatar com hífens
        isbn_formatado = f"{isbn_fake[0]}-{isbn_fake[1:5]}-{isbn_fake[5:9]}-{isbn_fake[9]}"
    else:
        # Gerar ISBN-13
        base = ''.join([str(random.randint(0, 9)) for _ in range(12)])
        digito_verificador = calcular_digito_verificador_isbn13(base)
        isbn_fake = base + digito_verificador
        # Formatar com hífens (formato comum: 978-...)
        isbn_formatado = f"978-{isbn_fake[3:5]}-{isbn_fake[5:9]}-{isbn_fake[9:12]}-{isbn_fake[12]}"
   
    entry_isbn.delete(0, tk.END)
    entry_isbn.insert(0, isbn_formatado)
    entry_isbn.config(fg="blue")
    mostrar_mensagem_temporaria("ISBN fake gerado com sucesso!", "blue")
 
def limpar_campos():
    """Limpa todos os campos do formulário"""
    entry_titulo.delete(0, tk.END)
    entry_autor.delete(0, tk.END)
    entry_ano.delete(0, tk.END)
    entry_genero.set("Escolha um gênero")
    entry_genero.configure(foreground="gray")
    entry_isbn.delete(0, tk.END)
   
    # Resetar cores
    entry_titulo.config(fg="black")
    entry_autor.config(fg="black")
    entry_ano.config(fg="black")
    entry_isbn.config(fg="black")
   
    entry_titulo.focus_set()
    mostrar_mensagem_temporaria("Campos limpos!", "blue")
 
def validar_e_adicionar_livro():
    global contador_id
 
    titulo = entry_titulo.get().strip()
    autor = entry_autor.get().strip()
    ano = entry_ano.get().strip()
    genero = entry_genero.get().strip()
    isbn = entry_isbn.get().strip()
 
    # Validar campos
    if not titulo:
        mostrar_erro_entry(entry_titulo, "Preencha o título")
        mostrar_mensagem_temporaria("Preencha o título", "red")
        return
    if not autor:
        mostrar_erro_entry(entry_autor, "Preencha o autor")
        mostrar_mensagem_temporaria("Preencha o autor", "red")
        return
    if not ano:
        mostrar_erro_entry(entry_ano, "Preencha o ano")
        mostrar_mensagem_temporaria("Preencha o ano", "red")
        return
    if not ano.isdigit() or not (1000 <= int(ano) <= datetime.now().year):
        mostrar_erro_entry(entry_ano, f"Ano inválido (1000-{datetime.now().year})")
        mostrar_mensagem_temporaria(f"Ano inválido (1000-{datetime.now().year})", "red")
        return
    if not genero or genero == "Escolha um gênero":
        mostrar_erro_combobox(entry_genero, "Escolha um gênero")
        mostrar_mensagem_temporaria("Escolha um gênero", "red")
        return
    if not isbn:
        mostrar_erro_entry(entry_isbn, "Preencha o ISBN")
        mostrar_mensagem_temporaria("Preencha o ISBN", "red")
        return
    if not validar_isbn(isbn):
        mostrar_erro_entry(entry_isbn, "ISBN inválido")
        mostrar_mensagem_temporaria("ISBN inválido - verifique o dígito verificador", "red")
        return
 
    # Verificar duplicidade
    for livro in catalogo:
        if (livro["titulo"].lower() == titulo.lower() and
            livro["autor"].lower() == autor.lower() and
            livro["isbn"] == isbn):
            mostrar_erro_entry(entry_titulo, "Livro já existe")
            mostrar_mensagem_temporaria("Livro já existe", "red")
            return
 
    novo_livro = {
        "ID": contador_id,
        "titulo": titulo,
        "autor": autor,
        "ano": ano,
        "genero": genero,
        "isbn": isbn
    }
    catalogo.append(novo_livro)
    contador_id += 1
    atualizar_treeview(catalogo)
 
    mostrar_mensagem_temporaria("Livro adicionado com sucesso!", "green")
    limpar_campos()
 
def atualizar_treeview(lista_livros):
    treeview.delete(*treeview.get_children())
    for livro in lista_livros:
        treeview.insert("", "end", values=(
            livro["ID"],
            livro["titulo"],
            livro["autor"],
            livro["ano"],
            livro["genero"],
            livro["isbn"]
        ))
 
def buscar_livro():
    termo_busca = entry_busca.get().lower().strip()
    resultados = []
 
    for livro in catalogo:
        if (termo_busca in livro["titulo"].lower() or
            termo_busca in livro["autor"].lower() or
            termo_busca in str(livro["ano"]).lower() or
            termo_busca in livro["genero"].lower() or
            termo_busca in livro["isbn"].lower()):
            resultados.append(livro)
 
    if resultados:
        atualizar_treeview(resultados)
        mostrar_mensagem_temporaria(f"{len(resultados)} resultado(s) encontrado(s).", "blue")
    else:
        atualizar_treeview(resultados)
        mostrar_mensagem_temporaria("Nenhum livro encontrado com esse termo.", "orange")
 
def livro_aleatorio():
    if not catalogo:
        mostrar_mensagem_temporaria("O catálogo está vazio.", "orange")
        return
 
    livro = random.choice(catalogo)
    mensagem = (
        f"📚 Livro Aleatório:\n"
        f"Título: {livro['titulo']}\n"
        f"Autor: {livro['autor']}\n"
        f"Ano: {livro['ano']}\n"
        f"Gênero: {livro['genero']}\n"
        f"ISBN: {livro['isbn']}"
    )
    mostrar_mensagem_temporaria(mensagem, "blue")
 
def ordenar_livros():
    catalogo.sort(key=lambda livro: livro["autor"].lower())
    atualizar_treeview(catalogo)
    mostrar_mensagem_temporaria("Livros ordenados por autor.", "blue")
 
def remover_livro():
    item_selecionado = treeview.selection()
    if not item_selecionado:
        mostrar_mensagem_temporaria("Selecione um livro para remover.", "red")
        return
 
    livro_valores = treeview.item(item_selecionado, "values")
    id_selecionado = int(livro_valores[0])
 
    for livro in catalogo:
        if livro["ID"] == id_selecionado:
            catalogo.remove(livro)
            atualizar_treeview(catalogo)
            mostrar_mensagem_temporaria("Livro removido com sucesso.", "green")
            return
 
def tratar_tecla_pressionada(event):
    """Gerencia atalhos de teclado"""
    if event.keysym == "Return" and event.widget in [entry_titulo, entry_autor, entry_ano, entry_genero, entry_isbn]:
        validar_e_adicionar_livro()
    elif event.keysym == "Escape":
        limpar_campos()
 
# --- Interface Gráfica ---
janela = tk.Tk()
janela.title("Sistema de Livraria")
janela.configure(bg="lightgray")
janela.geometry("800x600")
 
# Vincular atalhos de teclado
janela.bind("<KeyPress>", tratar_tecla_pressionada)
 
# Frame de cadastro
frame_cadastro = Frame(janela, borderwidth=1, relief="solid", bg="white")
frame_cadastro.place(x=10, y=10, width=390, height=150)
 
# Título
tk.Label(frame_cadastro, text="Título:", bg="white").place(x=5, y=5)
entry_titulo = tk.Entry(frame_cadastro, width=30)
entry_titulo.place(x=55, y=5, width=120, height=23)
entry_titulo.bind("<FocusIn>", lambda e: limpar_placeholder(e, entry_titulo, "Preencha o título"))
entry_titulo.bind("<KeyRelease>", validar_campo_titulo)
ToolTip(entry_titulo, "Digite o título do livro (sem números)\nAtalhos: Enter=Adicionar, Esc=Limpar")
 
# Autor
tk.Label(frame_cadastro, text="Autor:", bg="white").place(x=185, y=5)
entry_autor = tk.Entry(frame_cadastro, width=30)
entry_autor.place(x=225, y=5, width=120, height=23)
entry_autor.bind("<FocusIn>", lambda e: limpar_placeholder(e, entry_autor, "Preencha o autor"))
entry_autor.bind("<KeyRelease>", validar_campo_autor)
ToolTip(entry_autor, "Digite o nome do autor (sem números)")
 
# Ano
tk.Label(frame_cadastro, text="Ano:", bg="white").place(x=5, y=40)
entry_ano = tk.Entry(frame_cadastro, width=30)
entry_ano.place(x=55, y=40, width=120, height=23)
entry_ano.bind("<FocusIn>", lambda e: limpar_placeholder(e, entry_ano, "Preencha o ano"))
entry_ano.bind("<KeyRelease>", validar_campo_ano)
ToolTip(entry_ano, "Digite o ano de publicação (1000-ano atual)")
 
# ISBN
tk.Label(frame_cadastro, text="ISBN:", bg="white").place(x=185, y=40)
entry_isbn = tk.Entry(frame_cadastro, width=30)
entry_isbn.place(x=225, y=40, width=120, height=23)
entry_isbn.bind("<FocusIn>", lambda e: limpar_placeholder(e, entry_isbn, "Preencha o ISBN"))
ToolTip(entry_isbn, "Digite o ISBN (10 ou 13 dígitos)\nInclui validação de dígito verificador")
 
# Gênero
tk.Label(frame_cadastro, text="Gênero:", bg="white").place(x=5, y=75)
entry_genero_var = tk.StringVar()
entry_genero = ttk.Combobox(frame_cadastro, textvariable=entry_genero_var,
                            values=["Ação", "Suspense", "Terror", "Romance", "Ficção", "Outro"],
                            state="readonly")
entry_genero.place(x=55, y=75, width=120, height=23)
entry_genero.set("Escolha um gênero")
entry_genero.configure(foreground="gray")
entry_genero.bind("<FocusIn>", lambda e: limpar_placeholder_combobox(e, entry_genero, "Escolha um gênero"))
ToolTip(entry_genero, "Selecione o gênero do livro")
 
# Botão adicionar
botao_adicionar = tk.Button(frame_cadastro, text="Adicionar Livro (Enter)", command=validar_e_adicionar_livro)
botao_adicionar.place(x=55, y=110, width=120)
ToolTip(botao_adicionar, "Adiciona o livro ao catálogo\nAtalho: Tecla Enter")
 
# Botão limpar
botao_limpar = tk.Button(frame_cadastro, text="Limpar Campos (Esc)", command=limpar_campos)
botao_limpar.place(x=185, y=110, width=120)
ToolTip(botao_limpar, "Limpa todos os campos do formulário\nAtalho: Tecla Esc")
 
# Botão gerar ISBN fake
botao_isbn_fake = tk.Button(frame_cadastro, text="Gerar ISBN Fake", command=gerar_isbn_fake)
botao_isbn_fake.place(x=315, y=110, width=65)
ToolTip(botao_isbn_fake, "Gera um ISBN válido para testes")
 
# Frame de busca
frame_busca = Frame(janela, borderwidth=1, relief="solid", bg="white")
frame_busca.place(x=410, y=10, width=380, height=150)
 
# Busca
tk.Label(frame_busca, text="Buscar:", bg="white").place(x=10, y=10)
entry_busca = tk.Entry(frame_busca, width=30)
entry_busca.place(x=60, y=10, width=200, height=23)
ToolTip(entry_busca, "Busca livros por título, autor, ano, gênero ou ISBN")
 
# Botões de ação
botao_buscar = tk.Button(frame_busca, text="Buscar Livro", command=buscar_livro)
botao_buscar.place(x=270, y=10, width=100, height=25)
ToolTip(botao_buscar, "Realiza a busca pelos termos digitados")
 
botao_ordenar = tk.Button(frame_busca, text="Ordenar por Autor", command=ordenar_livros)
botao_ordenar.place(x=270, y=40, width=100, height=25)
ToolTip(botao_ordenar, "Ordena os livros por ordem alfabética de autor")
 
botao_remover = tk.Button(frame_busca, text="Remover Livro", command=remover_livro)
botao_remover.place(x=270, y=70, width=100, height=25)
ToolTip(botao_remover, "Remove o livro selecionado na lista")
 
botao_livro_aleatorio = tk.Button(frame_busca, text="Livro Aleatório", command=livro_aleatorio)
botao_livro_aleatorio.place(x=270, y=100, width=100, height=25)
ToolTip(botao_livro_aleatorio, "Seleciona um livro aleatório do catálogo")
 
# Frame da lista
frame_lista = Frame(janela, borderwidth=1, relief="solid", bg="white")
frame_lista.place(x=10, y=170, width=780, height=380)
 
# Tabela de livros
colunas = ("ID", "titulo", "autor", "ano", "genero", "isbn")
treeview = ttk.Treeview(frame_lista, columns=colunas, show="headings")
treeview.heading("ID", text="ID")
treeview.heading("titulo", text="Título")
treeview.heading("autor", text="Autor")
treeview.heading("ano", text="Ano")
treeview.heading("genero", text="Gênero")
treeview.heading("isbn", text="ISBN")
 
treeview.column("ID", width=30)
treeview.column("titulo", width=250)
treeview.column("autor", width=150)
treeview.column("ano", width=80)
treeview.column("genero", width=100)
treeview.column("isbn", width=120)
 
# Scrollbar para a treeview
scrollbar = ttk.Scrollbar(frame_lista, orient="vertical", command=treeview.yview)
treeview.configure(yscrollcommand=scrollbar.set)
scrollbar.place(x=760, y=5, width=15, height=350)
treeview.place(x=5, y=5, width=755, height=350)
ToolTip(treeview, "Lista de livros do catálogo\nClique em um livro para selecionar")
 
# Label para mensagens
label_mensagem = tk.Label(janela, text="", fg="green", bg="lightgray", font=("Arial", 10))
label_mensagem.place(x=10, y=560, width=780)
 
janela.mainloop()