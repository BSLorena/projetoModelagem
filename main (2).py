import tkinter as tk
from tkinter import messagebox
import sqlite3
import re

# Classe para gerenciar o banco de dados
class Database:
    def __init__(self, db_name):
        self.db_name = db_name

    def connect(self):
        """Conecta ao banco de dados e cria as tabelas se não existirem."""
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                email TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            )
        ''')
        c.execute('''
            CREATE TABLE IF NOT EXISTS profiles (
                user_id INTEGER PRIMARY KEY,
                name TEXT,
                weight REAL,
                height REAL,
                age INTEGER,
                sport TEXT,
                experience_level TEXT,
                achievements TEXT,
                goals TEXT,
                FOREIGN KEY(user_id) REFERENCES users(id)
            )
        ''')
        conn.commit()
        return conn

    def check_email_exists(self, email):
        """Verifica se o e-mail já está registrado no banco de dados."""
        conn = self.connect()
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE email=?", (email,))
        result = c.fetchone()
        conn.close()
        return result is not None

    def create_user(self, email, password):
        """Cria um novo usuário no banco de dados."""
        conn = self.connect()
        c = conn.cursor()
        try:
            c.execute("INSERT INTO users (email, password) VALUES (?, ?)", (email, password))
            conn.commit()
        except sqlite3.IntegrityError:
            pass
        finally:
            conn.close()

    def get_user_id(self, email):
        """Obtém o ID do usuário pelo e-mail."""
        conn = self.connect()
        c = conn.cursor()
        c.execute("SELECT id FROM users WHERE email=?", (email,))
        result = c.fetchone()
        conn.close()
        return result[0] if result else None

    def save_profile(self, user_id, name, weight, height, age, sport, experience_level, achievements, goals):
        """Salva ou atualiza o perfil do usuário com esportes e objetivos."""
        conn = self.connect()
        c = conn.cursor()
        try:
            c.execute('''
                INSERT INTO profiles (user_id, name, weight, height, age, sport, experience_level, achievements, goals)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(user_id) DO UPDATE SET
                    name=excluded.name,
                    weight=excluded.weight,
                    height=excluded.height,
                    age=excluded.age,
                    sport=excluded.sport,
                    experience_level=excluded.experience_level,
                    achievements=excluded.achievements,
                    goals=excluded.goals
            ''', (user_id, name, weight, height, age, sport, experience_level, achievements, goals))
            conn.commit()
        finally:
            conn.close()

# Classe para gerenciar a interface gráfica
class Application:
    def __init__(self, root, db):
        self.root = root
        self.db = db
        self.root.title("BSI SPORTS")
        self.frame = tk.Frame(root)
        self.frame.pack(padx=10, pady=10)
        self.create_register_screen()

    def create_register_screen(self):
        """Cria a tela de registro de usuários."""
        for widget in self.frame.winfo_children():
            widget.destroy()

        # Email
        self.label_email = tk.Label(self.frame, text="E-mail")
        self.label_email.grid(row=0, column=0, pady=5)
        self.entry_email = tk.Entry(self.frame)
        self.entry_email.grid(row=0, column=1, pady=5)

        # Senha
        self.label_password = tk.Label(self.frame, text="Senha")
        self.label_password.grid(row=1, column=0, pady=5)
        self.entry_password = tk.Entry(self.frame, show="*")
        self.entry_password.grid(row=1, column=1, pady=5)

        # Confirmar senha
        self.label_password_confirmation = tk.Label(self.frame, text="Confirmar Senha")
        self.label_password_confirmation.grid(row=2, column=0, pady=5)
        self.entry_password_confirmation = tk.Entry(self.frame, show="*")
        self.entry_password_confirmation.grid(row=2, column=1, pady=5)

        # Botões
        self.button_create_account = tk.Button(self.frame, text="Criar Conta", command=self.create_account)
        self.button_create_account.grid(row=3, column=0, columnspan=2, pady=10)

        self.button_account = tk.Button(self.frame, text="Já tenho uma conta", command=self.account)
        self.button_account.grid(row=4, column=0, columnspan=2, pady=10)

    def is_valid_password(self, password):
        """Verifica se a senha é válida."""
        return len(password) >= 8 and re.search(r'\d', password) and re.search(r'[A-Za-z]', password)

    def create_account(self):
        """Cria a conta do usuário e abre a tela de configuração."""
        email = self.entry_email.get()
        password = self.entry_password.get()

        if not email or not password:
            messagebox.showerror("Erro", "Todos os campos devem ser preenchidos!")
            return

        if password != self.entry_password_confirmation.get():
            messagebox.showerror("Erro", "Confirmação de senha incorreta!")
            return

        if not self.is_valid_password(password):
            messagebox.showerror("Erro", "Senha inválida. A senha deve ter pelo menos 8 caracteres e incluir números e letras.")
            return

        if self.db.check_email_exists(email):
            messagebox.showerror("Erro", "Este email já está registrado.")
            return

        self.db.create_user(email, password)
        messagebox.showinfo("Sucesso", "Conta criada com sucesso!")
        user_id = self.db.get_user_id(email)
        self.open_profile_config(user_id)

    def open_profile_config(self, user_id):
        """Abre a tela de configuração de perfil, incluindo esportes e objetivos."""
        for widget in self.frame.winfo_children():
            widget.destroy()

        tk.Label(self.frame, text="Nome:").grid(row=0, column=0)
        self.entry_name = tk.Entry(self.frame)
        self.entry_name.grid(row=0, column=1)

        tk.Label(self.frame, text="Peso:").grid(row=1, column=0)
        self.entry_weight = tk.Entry(self.frame)
        self.entry_weight.grid(row=1, column=1)

        tk.Label(self.frame, text="Altura:").grid(row=2, column=0)
        self.entry_height = tk.Entry(self.frame)
        self.entry_height.grid(row=2, column=1)

        tk.Label(self.frame, text="Idade:").grid(row=3, column=0)
        self.entry_age = tk.Entry(self.frame)
        self.entry_age.grid(row=3, column=1)

        # Campos para o caso de uso 003
        tk.Label(self.frame, text="Esporte Praticado:").grid(row=4, column=0)
        self.entry_sport = tk.Entry(self.frame)
        self.entry_sport.grid(row=4, column=1)

        tk.Label(self.frame, text="Nível de Experiência:").grid(row=5, column=0)
        self.entry_experience = tk.Entry(self.frame)
        self.entry_experience.grid(row=5, column=1)

        tk.Label(self.frame, text="Conquistas:").grid(row=6, column=0)
        self.entry_achievements = tk.Entry(self.frame)
        self.entry_achievements.grid(row=6, column=1)

        tk.Label(self.frame, text="Objetivos:").grid(row=7, column=0)
        self.entry_goals = tk.Entry(self.frame)
        self.entry_goals.grid(row=7, column=1)

        # Botão para salvar perfil
        tk.Button(self.frame, text="Salvar", command=lambda: self.save_profile(user_id)).grid(row=8, column=0, columnspan=2)

        # Botão de Voltar
        self.button_back = tk.Button(self.frame, text="Voltar", command=self.create_register_screen)
        self.button_back.grid(row=9, column=0, columnspan=2, pady=10)

    def save_profile(self, user_id):
        """Salva as configurações de perfil no banco de dados, incluindo esportes e objetivos."""
        name = self.entry_name.get()
        weight = self.entry_weight.get()
        height = self.entry_height.get()
        age = self.entry_age.get()
        sport = self.entry_sport.get()
        experience_level = self.entry_experience.get()
        achievements = self.entry_achievements.get()
        goals = self.entry_goals.get()

        try:
            self.db.save_profile(user_id, name, weight, height, age, sport, experience_level, achievements, goals)
            messagebox.showinfo("Sucesso", "Perfil salvo com sucesso!")
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao salvar perfil: {str(e)}")

    def account(self):
        messagebox.showerror("Erro", "Ops! Outro caso de uso.")

# Função principal para rodar a aplicação
def main():
    # Inicializa o banco de dados
    db = Database('users.db')

    # Inicializa a interface gráfica
    root = tk.Tk()
    app = Application(root, db)

    # Inicia o loop da interface gráfica
    root.mainloop()

# Executa a função principal
if __name__ == "__main__":
    main()

