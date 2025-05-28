import tkinter as tk
from tkinter import ttk, messagebox
import os
import sys
import tempfile
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
import ctypes

class UniversalTraducoesApp:
    def __init__(self, root):
        self.root = root
        self.root.title("UNIVERSAL TRADUÇÕES")
        self.root.geometry("1000x700")
        self.root.configure(bg="#f0f2f5")
        
        self.pasta_dados = self.definir_pasta_dados()
        os.chdir(self.pasta_dados)
        
        self.criar_icone()
        self.inicializar_arquivos()
        self.carregar_dados()
        
        self.configurar_estilos()
        self.tela_inicial()

    def definir_pasta_dados(self):
        locais = [
            os.path.join(os.getenv('LOCALAPPDATA'), 'Universal_Traducoes'),
            os.path.join(tempfile.gettempdir(), 'Universal_Traducoes'),
            os.path.expanduser('~/Universal_Traducoes')
        ]
        
        for pasta in locais:
            try:
                os.makedirs(pasta, exist_ok=True)
                with open(os.path.join(pasta, 'teste.tmp'), 'w') as f:
                    f.write('teste')
                os.remove(os.path.join(pasta, 'teste.tmp'))
                return pasta
            except:
                continue
        
        messagebox.showerror("Erro", "Não foi possível acessar nenhuma pasta segura")
        sys.exit(1)

    def criar_icone(self):
        self.icone_path = os.path.join(self.pasta_dados, "universal_icon.ico")
        if not os.path.exists(self.icone_path):
            try:
                img = Image.new('RGBA', (256, 256), (44, 62, 80, 255))
                d = ImageDraw.Draw(img)
                d.text((78, 60), "UT", fill=(255, 255, 255, 255))
                img.save(self.icone_path, format='ICO')
            except:
                self.icone_path = None
        
        if self.icone_path:
            try:
                self.root.iconbitmap(self.icone_path)
            except:
                pass

    def inicializar_arquivos(self):
        arquivos = ['tradutores.txt', 'clientes.txt', 'protocolos.txt']
        for arquivo in arquivos:
            caminho = os.path.join(self.pasta_dados, arquivo)
            if not os.path.exists(caminho):
                try:
                    with open(caminho, 'w', encoding='utf-8') as f:
                        f.write("")
                except:
                    self.tratar_erro_arquivos()

    def tratar_erro_arquivos(self):
        resposta = messagebox.askretrycancel(
            "Erro de Permissão",
            "Não foi possível criar arquivos necessários.\nDeseja tentar como Administrador?"
        )
        
        if resposta:
            try:
                if sys.platform == 'win32':
                    ctypes.windll.shell32.ShellExecuteW(
                        None, "runas", sys.executable, " ".join(sys.argv), None, 1
                    )
                sys.exit(0)
            except:
                messagebox.showerror("Erro", "Falha ao executar como administrador")
                sys.exit(1)
        else:
            sys.exit(0)

    def carregar_dados(self):
        self.dados = {
            'tradutores': [],
            'clientes': [],
            'protocolos': []
        }
        
        for tipo in self.dados.keys():
            caminho = os.path.join(self.pasta_dados, f"{tipo}.txt")
            if os.path.exists(caminho):
                try:
                    with open(caminho, 'r', encoding='utf-8') as f:
                        self.dados[tipo] = [linha.strip() for linha in f if linha.strip()]
                except:
                    messagebox.showwarning("Aviso", f"Erro ao ler {tipo}.txt")

    def configurar_estilos(self):
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure('TFrame', background='#f0f2f5')
        self.style.configure('TButton', font=('Helvetica', 10), padding=6)
        self.style.configure('TLabel', background='#f0f2f5', font=('Helvetica', 10))
        self.style.configure('Header.TLabel', font=('Helvetica', 16, 'bold'))
        self.style.configure('Small.TLabel', font=('Helvetica', 7))
        self.cor_primaria = "#2c3e50"
        self.cor_secundaria = "#3498db"
        self.cor_sucesso = "#27ae60"
        self.cor_info = "#2980b9"

    def limpar_tela(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def tela_inicial(self):
        self.limpar_tela()
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        header_frame = ttk.Frame(main_frame)
        header_frame.pack(pady=(0, 30))
        logo_label = ttk.Label(header_frame, text="UNIVERSAL TRADUÇÕES", 
                             style='Header.TLabel', foreground=self.cor_primaria)
        logo_label.pack()
        slogan_label = ttk.Label(header_frame, text="Traduções Juramentadas e Certificadas", 
                               foreground=self.cor_secundaria)
        slogan_label.pack()
        
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(pady=20)
        botoes = [
            ("TRADUTORES", self.tela_tradutores),
            ("CLIENTES", self.tela_clientes),
            ("PROTOCOLOS", self.tela_protocolos),
            ("PESQUISAR", self.tela_pesquisa)
        ]
        
        for i, (texto, comando) in enumerate(botoes):
            btn = ttk.Button(btn_frame, text=texto, command=comando,
                           style='TButton', width=20)
            btn.grid(row=i//3, column=i%3, padx=10, pady=10)
        
        footer_frame = ttk.Frame(main_frame)
        footer_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=(30, 0))
        ttk.Label(footer_frame, text="© 2024 UNIVERSAL TRADUÇÕES - Todos os direitos reservados",
                 foreground="#7f8c8d").pack(side=tk.BOTTOM)
        
        dev_frame = ttk.Frame(footer_frame)
        dev_frame.pack(side=tk.RIGHT, padx=10)
        ttk.Label(dev_frame, text="Desenvolvido Por Lucas Cobra", 
                 style='Small.TLabel', foreground="#7f8c8d").pack()

    def tela_tradutores(self):
        self.mostrar_tela_secundaria(
            "Tradutores",
            ["Nome", "Idioma", "Contato"],
            self.dados['tradutores'],
            self.salvar_tradutor
        )

    def tela_clientes(self):
        self.mostrar_tela_secundaria(
            "Clientes",
            ["Nome", "CNPJ/CPF", "Email", "Telefone", "Endereço"],
            self.dados['clientes'],
            self.salvar_cliente
        )

    def tela_protocolos(self):
        clientes = [c.split('|')[0] for c in self.dados['clientes']]
        self.mostrar_tela_secundaria(
            "Protocolos",
            ["Número", "Cliente", "Contato", "Telefone", "Email", 
             "Valor", "Idioma", "Custo Adicional", "Valor Total", "Colaborador"],
            self.dados['protocolos'],
            self.salvar_protocolo,
            campos_especiais={'Cliente': clientes}
        )

    def mostrar_tela_secundaria(self, titulo, colunas, dados, callback_salvar, campos_especiais=None):
        janela = tk.Toplevel(self.root)
        janela.title(titulo)
        janela.geometry("1200x800")
        
        form_frame = ttk.Frame(janela)
        form_frame.pack(fill=tk.X, padx=10, pady=10)
        
        entries = []
        for i, coluna in enumerate(colunas):
            ttk.Label(form_frame, text=f"{coluna}:").grid(row=i, column=0, padx=5, pady=5, sticky=tk.W)
            
            if campos_especiais and coluna in campos_especiais:
                combo = ttk.Combobox(form_frame)
                combo['values'] = campos_especiais[coluna]
                combo.grid(row=i, column=1, padx=5, pady=5, sticky=tk.EW)
                entries.append(combo)
            else:
                entry = ttk.Entry(form_frame)
                entry.grid(row=i, column=1, padx=5, pady=5, sticky=tk.EW)
                entries.append(entry)
        
        ttk.Button(form_frame, text="Salvar", 
                  command=lambda: self.salvar_dados(entries, callback_salvar))\
                  .grid(row=len(colunas), columnspan=2, pady=10)
        
        tree_frame = ttk.Frame(janela)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        tree = ttk.Treeview(tree_frame, columns=colunas, show="headings")
        for col in colunas:
            tree.heading(col, text=col)
            tree.column(col, width=100, anchor=tk.W)
        
        scroll = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscrollcommand=scroll.set)
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        for item in dados:
            tree.insert("", tk.END, values=item.split("|") if isinstance(item, str) else item)

    def salvar_dados(self, entries, callback):
        dados = [entry.get() for entry in entries]
        if all(dados):
            callback(dados)
            self.salvar_arquivos()
            messagebox.showinfo("Sucesso", "Dados salvos com sucesso!")
        else:
            messagebox.showwarning("Aviso", "Preencha todos os campos!")

    def salvar_tradutor(self, dados):
        self.dados['tradutores'].append("|".join(dados))

    def salvar_cliente(self, dados):
        self.dados['clientes'].append("|".join(dados))

    def salvar_protocolo(self, dados):
        clientes = [c.split('|')[0] for c in self.dados['clientes']]
        if dados[1] not in clientes:
            messagebox.showerror("Erro", "Cliente não cadastrado!")
            return
        
        dados.append(datetime.now().strftime("%d/%m/%Y %H:%M"))
        self.dados['protocolos'].append("|".join(dados))
        self.salvar_arquivos()

    def salvar_arquivos(self):
        for tipo in self.dados.keys():
            caminho = os.path.join(self.pasta_dados, f"{tipo}.txt")
            try:
                with open(caminho, 'w', encoding='utf-8') as f:
                    f.write("\n".join(self.dados[tipo]))
            except:
                messagebox.showerror("Erro", f"Falha ao salvar {tipo}.txt")

    def tela_pesquisa(self):
        janela = tk.Toplevel(self.root)
        janela.title("Pesquisa Integrada")
        janela.geometry("1400x900")
        
        main_frame = ttk.Frame(janela)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        control_frame = ttk.Frame(main_frame)
        control_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(control_frame, text="Tipo de Dados:").pack(side=tk.LEFT, padx=5)
        self.tipo_pesquisa = ttk.Combobox(control_frame, values=["Clientes", "Protocolos"], state="readonly")
        self.tipo_pesquisa.pack(side=tk.LEFT, padx=5)
        
        ttk.Label(control_frame, text="Termo de Busca:").pack(side=tk.LEFT, padx=5)
        self.termo_pesquisa = ttk.Entry(control_frame, width=40)
        self.termo_pesquisa.pack(side=tk.LEFT, padx=5)
        
        btn_pesquisar = ttk.Button(control_frame, text="Pesquisar", command=self.executar_pesquisa)
        btn_pesquisar.pack(side=tk.LEFT, padx=10)
        
        self.resultados_frame = ttk.Frame(main_frame)
        self.resultados_frame.pack(fill=tk.BOTH, expand=True, pady=10)

    def executar_pesquisa(self):
        for widget in self.resultados_frame.winfo_children():
            widget.destroy()
            
        termo = self.termo_pesquisa.get().lower()
        tipo = self.tipo_pesquisa.get()
        
        if tipo == "Clientes":
            colunas = ["Nome", "CNPJ/CPF", "Email", "Telefone", "Endereço", "Protocolos"]
            tree = ttk.Treeview(self.resultados_frame, columns=colunas, show="headings")
            
            for col in colunas:
                tree.heading(col, text=col)
                tree.column(col, width=150)
            
            for cliente in self.dados['clientes']:
                campos = cliente.split('|')
                if termo in cliente.lower():
                    num_protocolos = sum(1 for p in self.dados['protocolos'] if p.split('|')[1] == campos[0])
                    tree.insert("", tk.END, values=campos + [num_protocolos])
            
            tree.bind("<Double-1>", self.mostrar_detalhes_cliente)
            
        elif tipo == "Protocolos":
            colunas = ["Número", "Cliente", "Contato", "Telefone", "Email",
                      "Valor", "Idioma", "Custo Adicional", "Valor Total", 
                      "Colaborador", "Data"]
            tree = ttk.Treeview(self.resultados_frame, columns=colunas, show="headings")
            
            for col in colunas:
                tree.heading(col, text=col)
                tree.column(col, width=120)
            
            for protocolo in self.dados['protocolos']:
                campos = protocolo.split('|')
                if termo in protocolo.lower():
                    tree.insert("", tk.END, values=campos)
        
        vsb = ttk.Scrollbar(self.resultados_frame, orient="vertical", command=tree.yview)
        hsb = ttk.Scrollbar(self.resultados_frame, orient="horizontal", command=tree.xview)
        tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        
        tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")
        self.resultados_frame.grid_rowconfigure(0, weight=1)
        self.resultados_frame.grid_columnconfigure(0, weight=1)

    def mostrar_detalhes_cliente(self, event):
        item = event.widget.selection()[0]
        valores = event.widget.item(item, 'values')
        
        detalhes_janela = tk.Toplevel(self.root)
        detalhes_janela.title(f"Detalhes do Cliente: {valores[0]}")
        
        info_frame = ttk.Frame(detalhes_janela)
        info_frame.pack(padx=10, pady=10, fill=tk.X)
        
        labels = ["Nome:", "CNPJ/CPF:", "Email:", "Telefone:", "Endereço:"]
        for i, label in enumerate(labels):
            ttk.Label(info_frame, text=label, font=('Helvetica', 10, 'bold')).grid(row=i, column=0, sticky=tk.W)
            ttk.Label(info_frame, text=valores[i]).grid(row=i, column=1, sticky=tk.W)
        
        protocolos_frame = ttk.Frame(detalhes_janela)
        protocolos_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        
        colunas = ["Número", "Data", "Valor Total", "Descrição"]
        tree = ttk.Treeview(protocolos_frame, columns=colunas, show="headings")
        
        for col in colunas:
            tree.heading(col, text=col)
            tree.column(col, width=150)
        
        for protocolo in self.dados['protocolos']:
            campos = protocolo.split('|')
            if campos[1] == valores[0]:
                tree.insert("", tk.END, values=[
                    campos[0],  # Número
                    campos[-1],  # Data
                    campos[8],  # Valor Total
                    campos[2]   # Descrição (Contato)
                ])
        
        vsb = ttk.Scrollbar(protocolos_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=vsb.set)
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        vsb.pack(side=tk.RIGHT, fill=tk.Y)

if __name__ == "__main__":
    try:
        root = tk.Tk()
        app = UniversalTraducoesApp(root)
        root.mainloop()
    except Exception as e:
        messagebox.showerror(
            "Erro Inicial", 
            f"Falha crítica ao iniciar o aplicativo:\n{str(e)}\n\n"
            "Recomendações:\n"
            "1. Execute como Administrador\n"
            "2. Verifique o espaço em disco\n"
            "3. Reinstale o aplicativo"
        )
        sys.exit(1)