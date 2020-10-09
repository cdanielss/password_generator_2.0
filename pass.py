import random
import PySimpleGUI as sg
import os
import sqlite3

class PassGen:
    def __init__(self):
        sg.theme('BlueMono')
        layout = [
            [sg.Text('Site/Software:', size=(15,1)), 
            sg.Input(key='site', size=(30,10))],
            [sg.Text('Email/Usuario:', size=(15,1)), 
            sg.Input(key='usuario', size=(30,1))],
            [sg.Text('Quantidade de Caracteres:'), sg.Combo(values=list(range(30)), key='total_chars',
            default_value=7, size=(3,1) )],
            [sg.Text('Caracteres Especiais:'), sg.Combo(values=('sim', 'não'), key='esp_chars',
            default_value='sim', size=(5,1) )],
            [sg.Output(size=(82, 8))],
            [sg.Button('Gerar Senha'), sg.Button('Salvar'), sg.Button('Ver Senhas'), sg.Button('Exportar')],
        ]

        
        self.janela = sg.Window('Password Generator', layout, grab_anywhere=True, size=(650,450))

    def Iniciar(self):
        conn = sqlite3.connect('senhas.db')
        cursor = conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        site TEXT NOT NULL, 
        usuario TEXT NOT NULL, 
        senha TEXT NOT NULL
        );
        """)
        conn.close()
        while True:
            evento, valores = self.janela.read() 
            if evento == sg.WINDOW_CLOSED: 
                break
            if evento == 'Gerar Senha':
                if valores['esp_chars'] == 'sim':
                    nova_senha = self.gerar_senha(valores)
                    print(nova_senha) 
                if valores['esp_chars'] == 'não':
                    nova_senha = self.gerar_senhaEsp(valores)
                    print(nova_senha) 
            if evento == 'Salvar':
                if valores['site'] == '' or valores['usuario'] == '' or nova_senha == '':
                    print('Complete todos os campos')
                else:                    
                    self.salvar_senha(nova_senha, valores)
            if evento == 'Ver Senhas':
                self.ver()
            if evento == 'Exportar':
                self.exportar()
    
    def gerar_senha(self, valores):
        char_list = 'QWERTYUIOPASDFGHJKLZXCVBNMqwertyuiopasdfghjklzxcvbnm0123456789!#%$&*@'
        chars = random.choices(char_list, k=int(valores['total_chars'])) 
        new_pass = ''.join(chars)
        return new_pass

    def gerar_senhaEsp(self, valores):
        char_list = 'QWERTYUIOPASDFGHJKLZXCVBNMqwertyuiopasdfghjklzxcvbnm0123456789'
        chars = random.choices(char_list, k=int(valores['total_chars'])) 
        new_pass = ''.join(chars)
        return new_pass

    def salvar_senha(self, nova_senha, valores):
        site = valores['site']
        usuario = valores['usuario']
        senha = nova_senha
        conn = sqlite3.connect('senhas.db')
        cursor = conn.cursor()
        cursor.execute("""
        INSERT INTO users (site, usuario, senha)
        VALUES (?,?,?)
        """, (site, usuario, senha))
        print('Informacoes Salvas')
        conn.commit()
        conn.close()

    def ver(self):
        conn = sqlite3.connect('senhas.db')
        cursor = conn.cursor()
        cursor.execute("""
        SELECT site, usuario, senha FROM users;
        """)
        for linha in cursor.fetchall():
            print('SITE:', linha[0], '  USUARIO:', linha[1], '  SENHA:', linha[2])
        conn.commit()
        conn.close()
    
    def exportar(self):
        conn = sqlite3.connect('senhas.db')
        cursor = conn.cursor()
        cursor.execute("""
        SELECT site, usuario, senha FROM users;
        """)
        with open('senhas.txt','a',newline='') as arquivo:
            for linha in cursor.fetchall():
                arquivo.write(f"SITE:, {linha[0]}, USUARIO:, {linha[1]}, SENHA:, {linha[2]}\n")
        print('Arquivo Salvo')

gen = PassGen()
gen.Iniciar()

